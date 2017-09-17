import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import filecmp

def encrypt(key, sourceFilePath, encryptedFilePath):
    chunkSize=64*1024
    filesize = str(os.path.getsize(sourceFilePath)).zfill(16)
    IV=Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)
    
    with open(sourceFilePath, 'rb') as infile:
        with open(encryptedFilePath, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            
            while True:
                chunk=infile.read(chunkSize)
                if len(chunk)==0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk+=b' ' * (16 - (len(chunk) %16))
                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, encryptedFilePath, destinationFilePath):
    chunksize = 64*1024

    with open(encryptedFilePath) as infile:
        filesize=int(infile.read(16))
        IV=infile.read(16)
        
        decryptor=AES.new(key, AES.MODE_CBC, IV)
        
        with open(destinationFilePath, 'wb') as outfile:
            while True:
                chunk=infile.read(chunksize)
                if len(chunk)==0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)
            
def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()



def testRoundTrip(password, testFilePath):
    def compare(testFilePath, dFilePath):
        if filecmp.cmp(testFilePath, dFilePath, False):
            print testFilePath, '==', dFilePath
        else:
            print testFilePath, '!=', dFilePath

    eFilePath = testFilePath+'.encrypted'
    dFilePath = testFilePath+'.decrypted'
    
    print 'generate key'
    theKey = getKey(password)
    print 'password:', password, 'theKey:', theKey
    
    print 'encrypting', testFilePath, 'to', eFilePath
    encrypt(theKey, testFilePath, eFilePath)

    compare(testFilePath, eFilePath)
    
    print 'decrypting', eFilePath, 'to', dFilePath
    decrypt(theKey, eFilePath, dFilePath)
    
    compare(testFilePath, dFilePath)
        

if __name__ == '__main__':
    # test with a text file
    testRoundTrip('lame ass password', './test/FileToBeEncrypted.txt')
    
    # test with a binary file
    testRoundTrip('!@#$ +_)( {}|<>?L:"', './test/star-trek.jpg')
    
