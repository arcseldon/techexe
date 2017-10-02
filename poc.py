'''
Created on Sep 26, 2017

@author: llaird
'''
from pprint import pprint
import subprocess 
import os
from exceptions import RuntimeError

def executePatchScript(executionPath, scriptFilePath):
    '''Execute script from the specified location.
    executionPath -- run the script for this location
    scriptFilePath -- the name of the script
    returns a boolean indicating success
    '''
    proc = subprocess.Popen(['bash',scriptFilePath], cwd=executionPath)
    proc.communicate()
    if 0 == proc.returncode:
        print 'patch script successful'
        return True
    else:
        print 'patch script failed, returned', proc.returncode
        return False

def applyPatch(executionPath, patchFile):
    '''use patch to apply the patch file from the specified location.
    executionPath -- run patch from this location
    patchFile -- the patch file to apply
    returns a boolean indicating success
    '''
    patchCommand = 'patch -p 1 --verbose -i {patchFile}'.format(patchFile=patchFile)
    proc = subprocess.Popen(patchCommand, shell=True, cwd=executionPath, executable='/bin/bash')
    proc.communicate()
    if 0 == proc.returncode:
        print 'patch successful'
        return True
    else:
        print 'patch failed, patch returned', proc.returncode
        return False
    
def rollbackPatch(executionPath, patchFile):
    '''use patch to reverse the patch file from the specified location.
    executionPath -- run patch from this location
    patchFile -- the patch file to apply
    returns a boolean indicating success
    '''
    patchCommand = 'patch -R -p 1 --verbose -i {patchFile}'.format(patchFile=patchFile)
    proc = subprocess.Popen(patchCommand, shell=True, cwd=executionPath, executable='/bin/bash')
    proc.communicate()
    if 0 == proc.returncode:
        print 'patch rollback successful'
        return True
    else:
        print 'patch rollback failed, patch returned', proc.returncode
        return False

def installBundle(scriptExecutionPath, patchTargetPath, bundleLocation):
    '''install the scripts and patches in this bundle
    scriptExecutionPath -- where patch scripts are executed
    patchTargetPath -- the base path for the patch files
    bundleLocation -- the location of the bundle directory
    '''
    wasSuccesful = True
    # get the list of files in the bundle
    bundleFiles = os.listdir(bundleLocation)
    for bundleFile in bundleFiles:
        # this is assuming the patches and patch scripts order is not important
        if bundleFile.endswith('.patch'):
            # found a patch file, apply it.
            patchFile = os.path.join(bundleLocation, bundleFile)
            patchAttempt = applyPatch(patchTargetPath, patchFile)
            if not patchAttempt:
                wasSuccesful = False
                print 'patch', patchFile, 'failed'
        elif bundleFile.endswith('.sh'):
            # found a patch script, run it.
            patchScriptFile = os.path.join(bundleLocation, bundleFile)
            scriptAttempt = executePatchScript(scriptExecutionPath, patchScriptFile)
            if not scriptAttempt:
                wasSuccesful = False
                print 'patch script', patchScriptFile, 'failed'
            
                
    return wasSuccesful

class CryptKeeper():
    '''encrypts and decrypts files
    uses openssl to perform encryption actions.
    manages the encryption keys
    !! hard coded password ONLY for prototyping purposes !!
    !! hard coded passwords are NEVER OK !!
    !! and don't get me stared about hard coded passwords in Git repositories !!
    '''
    def __init__(self):
        '''initializes the base action string and key'''
        # HARD CODED PASSWORDS ARE NEVER OK
        # TODO load the key via a secure configuration method
        self.key = "-k 'abomination'"
        self.baseCommand = 'openssl enc {action} -aes-256-ctr -in {inputFile} -out {outputFile} {key}'
    
    def act(self, action, inputFile, outputFile):
        '''perform the specified encryption/decryption action
        action -- encryption '-e' or decryption '-d'
        inputFile -- the file on which the action will be performed
        outputFile -- the file produced by the action
        '''
        proc = subprocess.Popen(self.baseCommand.format(action=action,
                                                        inputFile=inputFile,
                                                        outputFile=outputFile,
                                                        key=self.key),
                                shell=True,
                                executable='/bin/bash')
        proc.communicate()
        return proc.returncode
    
    def encrypt(self, fileToEncrypt, outputFile):
        '''perform the encryption action
        fileToEncrypt -- the file to be encrypted
        outputFile -- where to produce the encrypted file
        '''
        action = '-e'
        returnCode = self.act(action, fileToEncrypt, outputFile,)
        if 0 == returnCode:
            print 'encryption successful'
        else:
            print 'encryption failed, openssl returned', returnCode
            raise RuntimeError('encryption failed, openssl returned code {code}'.format(code=returnCode))
    
    def decrypt(self, fileToDecrypt, outputFile):
        '''perform the decryption action
        fileToDecrypt -- the file to be decrypted
        outputFile -- where to produce the decrypted file
        '''
        action = '-d'
        returnCode = self.act(action, fileToDecrypt, outputFile)
        if 0 == returnCode:
            print 'decryption successful'
        else:
            print 'decryption failed, openssl returned', returnCode
            raise RuntimeError('decryption failed, openssl returned code {code}'.format(code=returnCode))
    

# executor
def downloadBundle(bundleId):
    # request the bundle
    
    # return the downloaded bundle path
    return './execution/downloadedBundle.enc'

    
def tarBundle(bundleId, bundleBaseDir, outputDir):
    '''create a tar file from a release directory
    the tar file will be in the outputDir and named <bundleId>.tar
    bundleId -- the name of the release directory
    bundleBaseDir -- the directory containing the release directory
    outputDir -- the location to create the release archive
    '''
    command = 'tar -cvf {outputDir}/{bundleId}.tar {bundleId}'.format(bundleId=bundleId, outputDir=outputDir)
    print 'echo', command
    proc = subprocess.Popen(command, shell=True, cwd=bundleBaseDir, executable='/bin/bash')
    proc.communicate()
    if 0 != proc.returncode:
        raise RuntimeError('tar returned code {code}'.format(code=proc.returncode))


def untarBundle(bundleTarFile, outputDir):
    '''explode the release tar file into the output directory    '''
    command = 'tar -xvf {tarFile}'.format(tarFile=bundleTarFile)
    print 'echo', command
    proc = subprocess.Popen(command, shell=True, cwd=outputDir, executable='/bin/bash')
    proc.communicate()
    if 0 != proc.returncode:
        raise RuntimeError('tar returned code {code}'.format(code=proc.returncode))


def runScript():
    pass

def rollbackBundle():
    pass

# apply instruction
def applyInstruction(instruction):
    print 'apply Instruction'
    pprint(instruction)
    
    bundleId = instruction['bundle']
    encryptedBundleFile = downloadBundle(bundleId)
    
    bundleFile = './execution/bundleFile.tar'
    keeper = CryptKeeper()
    keeper.decrypt(encryptedBundleFile, bundleFile)
    
    bundleLocation = './execution/{release}'.format(release=bundleId)
    untarBundle(bundleFile, bundleLocation)

    scriptExecutionPath = './execution/scriptEx'
    patchTargetPath = './execution/patchTarget'
    
    installBundle(scriptExecutionPath, patchTargetPath, bundleLocation)
    

# rollback instruction
def rollbackInstruction():
    pass

# scheduler
def setUpdateCheckTime():
    pass

# checker
def requestInstructions():
    # start with the assumption that there are no instructions
    instruction = {}

    try:
        # phone home for the next instruction
        # example instruction is to apply bundle 12345
        instruction = {'command':'apply',
                       'bundle':'12345'}
    
    # on request error, log the error and proceed with no instructions
    except Exception as err:
        # on request error, log the error and proceed with no instructions
        print err
    
    return instruction

def process():
    # set up a map of functions to call
    # these methods are expected to take the instruction as their single parameter
    instructionRegistry = {'apply':applyInstruction,
                           'rollback':rollbackInstruction}
    
    instruction = requestInstructions()
    
    try:
        # execute the instruction
        instructionRegistry[instruction['command']](instruction)
    except Exception as err:
        # log the error
        print err
        
        



if __name__ == '__main__':
    process()
    