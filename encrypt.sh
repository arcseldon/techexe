#!/bin/bash

SOURCE_FILE=$1
ENC_FILE=$SOURCE_FILE.openssl.encrypted
DEC_FILE=$SOURCE_FILE.openssl.decrypted

openssl enc -e -aes-256-ctr -in $SOURCE_FILE -out $ENC_FILE -k 'not a great password'

openssl enc -d -aes-256-ctr -in $ENC_FILE -out $DEC_FILE -k 'not a great password'

diff $SOURCE_FILE $DEC_FILE

