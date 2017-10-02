#!/bin/bash

FILE="./patchscriptrun.log"

if [ -e $FILE ]
then
    # already executed
    exit 1
else
    echo "First bash script for release 12345 executed here" > $FILE
fi