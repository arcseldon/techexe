# techexe
Technical Excercise

## Contents
### poc.py
contains a set of functions to perform the automated process.  See the file for explanations of the following methods.  

 - executePatchScript 
 - applyPatch 
 - rollbackPatch 
 - installBundle 
 - CryptKeeper class 
 -- encrypt 
 -- decrypt 
 - tarBundle 
 - untarBundle

### testApplyPatch.py 
tests for poc.py

- **TestApplyPatch** demonstrates the ability to:
 - run a patch shell script
 - apply a patch file
 - reverse a patch file
- **TestInstallBundle** demonstrates the ability to: 
 - install the patches and shell scripts contains within a release
   directory
- **TestCryptKeeper** demonstrates the ability to:
 - encrypt a file
 - decrypt a file
- **TestUntarTar** demonstrates the ability to:
 - create a tar file from a directory
 - explode a tar file into a directory