import os, random, string
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def GenerateKey():
    ##Generates a random symmetric key that is stored in a text file in the user's computer.
    key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))    # Key in string form
    return key.encode('utf-8')
    ### Returns symmetric key.


def Encrypt(key, filename):
    print("Encrypting.......")
    chunksize = 64* 1024
    outputFile = filename +".hidn"
    filesize = str(os.path.getsize(filename)).zfill(16)     # GetS  filesize and then zfill to 16 bytes
    IV = Random.new().read(16)                              # Read 16 bytes out of that

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))         # As filesize is a string, we are going to encode it into bytes(BINARY)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:                     # Then we've run out of bytes to encrypt in the file
                    break
                elif len(chunk) % 16 != 0:
                    # If less than 16 bytes, then we'd need to pad
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

    # removing original file
    os.remove(filename)



def Decrypt(key, filename):
    print("Decrypting.......")
    chunksize = 64*1024
    outputFile = filename[:-5]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)        # removes padding added during the encryption

    # removing encrypted version cypher text file
    os.remove(filename)


def GetKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def Test():
    userInputEncryptDecrypt = input("Press 1 for Encrypt and 2 for Decrypt: ")

    if userInputEncryptDecrypt == '1':
        filename = input("Type in File that you want to encrypt: ")
        password = input("Choose a Password: ")
        Encrypt(GetKey(password), filename)
        print("Completed")

    elif userInputEncryptDecrypt == '2':
        filename = input("Type in Filename that you want to decrypt: ")
        password = input("Type in the Password: ")
        
        Decrypt(GetKey(password), filename)
        print("Completed")

    else:
        print("Either Select 1 or 2")

if __name__ == '__main__':
    Test()
