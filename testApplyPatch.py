'''
Created on Sep 30, 2017

@author: llaird
'''
import unittest
import poc
import subprocess
import os
import filecmp

class TargetRepository:
    '''target for patch file application.
    using a git repository to simulate a regular file system
    and using hard reset to return the repository to a known state.
    '''
    def __init__(self):
        '''initialize the repository location'''
        self.path = '/modules/auth0-javascript-samples/'
    
    def reset(self):
        '''discard any local changes to return to a known state'''
        proc = subprocess.Popen('git reset --hard', shell=True, cwd=self.path, executable='/bin/bash')
        proc.communicate()
    
class TargetDirectory:
    '''target directory for execution of the pacth scripts
    specifies the location of a testing script execution directory
    and has a reset to return the execution directory to a known state
    '''
    def __init__(self):
        '''initialize the testing execution directory'''
        self.path = os.path.join(os.getcwd(),'test/patchScriptExecution')
        # create the output directory if necessary
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    
    def reset(self):
        '''remove any files created in the test execution directory'''
        files = os.listdir(self.path)
        print files
        for fileToRemove in files:
            pathToRemove = os.path.join(self.path, fileToRemove)
            print 'removing', pathToRemove
            os.remove(pathToRemove)
            
    def fileExists(self, fileName):
        '''check the test execution directory for specific file names
        fileName -- check for this filename
        returns true when the file was found
        '''
        files = os.listdir(self.path)
        return fileName in files
       
class TestCryptKeeper(unittest.TestCase):
    def setUp(self):
        self.inputsPath = os.path.join(os.getcwd(),'test')
        self.outputsPath = os.path.join(self.inputsPath, 'CryptKeeper')
        # create the output directory if necessary
        if not os.path.exists(self.outputsPath):
            os.mkdir(self.outputsPath)
            
    def inputFilePath(self, fileName):
        return os.path.join(self.inputsPath, fileName)

    def outputFilePath(self, fileName):
        return os.path.join(self.outputsPath, fileName)
        
    def testCrypteKeeperEncrypt(self):

        print ''
        print '--------------------------------------------------'
        print '-- testCrypteKeeperEncrypt'
        print '--------------------------------------------------'
        print ''
        
        fileToEncrypt = self.inputFilePath('FileToBeEncrypted.txt')

        outputFile = self.outputFilePath('testCryptKeeperEncrypt.encrypted')
        decryptedFile = self.outputFilePath('testCryptKeeperEncrypt.decrypted')
                
        print '** consruct the keeper'
        keeper = poc.CryptKeeper()
        
        print '** encrypt the test file'
        keeper.encrypt(fileToEncrypt, outputFile)

        print '** decrypt the output file to compare to the original.'
        keeper.decrypt(outputFile, decryptedFile)
        
        print '** compare the original file encrypted/decrypted file.'
        self.assertTrue(filecmp.cmp(fileToEncrypt, decryptedFile), 
                        'encrypted file does not match expected output')
        

    def testCryptKeeperDecrypt(self):

        print ''
        print '--------------------------------------------------'
        print '-- testCrypteKeeperDecrypt'
        print '--------------------------------------------------'
        print ''

        # input file created by ./test/prepareCryptKeeperExpectedFile.sh
        fileToDecrypt = self.inputFilePath('FileToBeEncrypted.txt.openssl.encrypted')
        expectedOutputFile = self.inputFilePath('FileToBeEncrypted.txt')

        outputFile = self.outputFilePath('testCryptKeeper.decrypted')

        print '** construct the keeper'
        keeper = poc.CryptKeeper()
        
        print '** decrypt the test file produced by openssl'
        keeper.decrypt(fileToDecrypt, outputFile)
        
        print '** compare the decrypted file to the expected file'
        self.assertTrue(filecmp.cmp(expectedOutputFile, outputFile), 
                        'decrypted file does not match expected output')

class TestInstallBundle(unittest.TestCase):
    def testInstallBundle(self):

        print ''
        print '--------------------------------------------------'
        print '-- testInstallBundle'
        print '--------------------------------------------------'
        print ''

        bundleLocation = '/work/patches/12345'
        bundleTarget = TargetRepository()
        scriptExecution = TargetDirectory()
        fileCreatedByPatchScript = 'patchscriptrun.log'
        
        print '** put the target repository in a known state'
        bundleTarget.reset()
        print '** clear any files from the script directory'
        scriptExecution.reset()
        
        print '** install the bundle'
        attempt = poc.installBundle(scriptExecution.path, bundleTarget.path, bundleLocation)
        self.assertTrue(attempt, 'Bundle installation failed')
        
        print '** look for expected log file'
        self.assertTrue(scriptExecution.fileExists(fileCreatedByPatchScript), 'expected log file is missing')

class TestApplyPatch(unittest.TestCase):

    def testApplyPatchScript(self):
        
        print ''
        print '--------------------------------------------------'
        print '-- testApplyPatchScript'
        print '--------------------------------------------------'
        print ''

        targetDirectory = TargetDirectory()
        patchScriptFile = '/work/patches/12345/make-fake-changes.sh'
        
        print '** clear any files from the target directory'
        targetDirectory.reset()
        
        print '** run the patch script and expect a success'
        firstAttempt = poc.executePatchScript(targetDirectory.path, patchScriptFile)
        self.assertTrue(firstAttempt, 'Patch script failed')
        
        print '** run the patch script again and expect a failure'
        secondAttempt = poc.executePatchScript(targetDirectory.path, patchScriptFile)
        self.assertFalse(secondAttempt, 'Executing patch script a second time succeded, should have failed.')
        

    def testApplyPatch(self):
 
        print ''
        print '--------------------------------------------------'
        print '-- testApplyPatch'
        print '--------------------------------------------------'
        print ''
 
        patchTarget = TargetRepository()
        patchFile = '/work/patches/12345/adds-some-text.patch'
         
        print '** put the target repository in a known state'
        patchTarget.reset()
 
        print '** apply the patch and expect a success.'
        firstAttempt = poc.applyPatch(patchTarget.path, patchFile)        
        self.assertTrue(firstAttempt, 'Patch application failed')
         
        print '** apply the patch a second time and expect a failure'
        secondAttempt = poc.applyPatch(patchTarget.path, patchFile)        
        self.assertFalse(secondAttempt, 'Applying patch a second time succeded, should have failed')
 
        print '** return the repository to a known state'
        patchTarget.reset()
 
    def testRollbackPatch(self):
 
        print ''
        print '--------------------------------------------------'
        print '-- testRollbackPatch'
        print '--------------------------------------------------'
        print ''
 
        patchTarget = TargetRepository()
        patchFile = '/work/patches/12345/adds-some-text.patch'
         
        print '** put the target repository in a known state'
        patchTarget.reset()
 
        print '** set up the repository by appplying the patch.'
        applyAttempt = poc.applyPatch(patchTarget.path, patchFile)        
        self.assertTrue(applyAttempt, 'Patch application failed')
         
        print '** reverse the patch.'
        rollbackAttempt = poc.rollbackPatch(patchTarget.path, patchFile)        
        self.assertTrue(rollbackAttempt, 'Rollback failed')
 
        print '** return the repository to a known state'
        patchTarget.reset()

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testApplyPatch']
    unittest.main()