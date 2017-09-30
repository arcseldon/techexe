#!/bin/bash

RELEASE=12345
EXE_DIR=/work/execution
TARGET_DIR=/modules/auth0-javascript-samples


# Manual patch process
# step 1.  Download make-fake-changes.sh to ~/
cp -v /work/patches/$RELEASE/make-fake-changes.sh ~/.

# step 2. Download adds-some-text.patch to ~/
cp -v /work/patches/$RELEASE/adds-some-text.patch ~/.

# step 3. Run bash make-fake-changes.sh
cd $EXE_DIR
bash make-fake-changes.sh

# step 4. Change to the /modules/auth0-javascript-samples/
cd $TARGET_DIR

# step 5. Apply patch
patch -p 1 --verbose -i ~/adds-some-text.patch


