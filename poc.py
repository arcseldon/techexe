'''
Created on Sep 26, 2017

@author: llaird
'''
from pprint import pprint
import subprocess 
import os

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



# executor
def downloadBundle(bundleId):
    # request the bundle
    
    # return the downloaded bundle path
    return './downloadedBundle.enc'

def decryptBundle(encryptedBundle):
    # decrypt the bundle
    
    # return the bundle path
    return './bundleArchive.tar'

def untarBundle(bundlePath):
    pass


    

def runScript():
    pass

def rollbackBundle():
    pass

# apply instruction
def applyInstruction(instruction):
    print 'apply Instruction'
    pprint(instruction)
    
    bundleId = instruction['bundle']
    downloadBundle(bundleId)
    
    decryptBundle()

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
    