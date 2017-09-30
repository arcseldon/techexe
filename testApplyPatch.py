'''
Created on Sep 30, 2017

@author: llaird
'''
import unittest
import poc
import subprocess
import os

class TargetRepository:
    def __init__(self):
        self.path = '/modules/auth0-javascript-samples/'
    
    def reset(self):
        # discard local changes in the repository
        proc = subprocess.Popen('git reset --hard', shell=True, cwd=self.path, executable='/bin/bash')
        proc.communicate()

    def status(self):
        # discard local changes in the repository
        proc = subprocess.Popen('git status -s -uno', shell=True, cwd=self.path, executable='/bin/bash')
        proc.communicate()
    
class TargetDirectory:
    def __init__(self):
        self.path = os.path.join(os.getcwd(),'test/patchScriptExecution')
    
    def reset(self):
        files = os.listdir(self.path)
        print files
        for fileToRemove in files:
            pathToRemove = os.path.join(self.path, fileToRemove)
            print 'removing', pathToRemove
            os.remove(pathToRemove)
    def fileExists(self, fileName):
        files = os.listdir(self.path)
        return fileName in files
        

class TestInstallBundle(unittest.TestCase):
    def testInstallBundle(self):
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

        print '** look for the modification to the repository'
        bundleTarget.status()

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