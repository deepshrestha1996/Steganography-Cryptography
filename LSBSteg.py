"""LSBSteg.py

Usage:
  LSBSteg.py encode -i <input> -o <output> -f <file> -p <password>
  LSBSteg.py decode -i <input> -o <output>  -p <password>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file=<file>          File to hide/unhide
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
  -p,--pass=<password>      Password for encryption
"""

import cv2
import docopt
import numpy as np
from simp_AES import *

class SteganographyException(Exception):
    pass


class LSBSteg():
    def __init__(self, im):
        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height

        self.maskONEValues = [1,2,4,8,16,32,64,128]
        #Mask used to put one ex:1->00000001, 2->00000010 .. associated with OR bitwise
        self.maskONE = self.maskONEValues.pop(0) #Will be used to do bitwise operations

        self.maskZEROValues = [254,253,251,247,239,223,191,127]
        #Mak used to put zero ex:254->11111110, 253->11111101 .. associated with AND bitwise
        self.maskZERO = self.maskZEROValues.pop(0)

        self.curwidth = 0  # Current width position
        self.curheight = 0 # Current height position
        self.curchan = 0   # Current channel position

    def put_binary_value(self, bits):
        '''Function to insert bits into the image (steganography process)
        bits- it represent the binary values to be inserted in sequence
        '''
        for c in bits:#Iterate over all bits
            val = list(self.image[self.curheight,self.curwidth]) #Get the pixel value as a list
            if int(c) == 1:#if  bit is set, mark it in image
                val[self.curchan] = int(val[self.curchan]) | self.maskONE #OR with maskONE
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO #AND with maskZERO
                #updating the image with new values
            self.image[self.curheight,self.curwidth] = tuple(val)
            #moving the pointer to the next space
            self.next_slot()

    def next_slot(self):
        '''
        function to move the ponter to the next location to put info
        '''
        if self.curchan == self.nbchannels-1: #Next Space is the following channel
            self.curchan = 0
            if self.curwidth == self.width-1: #Or the first channel of the next pixel of the same line
                self.curwidth = 0
                if self.curheight == self.height-1:#Or the first channel of the first pixel of the next line
                    self.curheight = 0
                    if self.maskONE == 128: #Mask 1000000, so the last mask
                        raise SteganographyException("No available slot remaining (image filled)")
                    else: #else go to next bitmask
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.curheight +=1
            else:
                self.curwidth +=1
        else:
            self.curchan +=1

    def read_bit(self):
        '''
        Function to read in a bit from the image @ certain [height,weidth and channel]
        '''
        val = self.image[self.curheight,self.curwidth][self.curchan]
        val = int(val) & self.maskONE
        self.next_slot()
        if val > 0:
            return "1"
        else:
            return "0"

    def read_byte(self):
        return self.read_bits(8)

    def read_bits(self, nb):
        '''
        Function to read the given number of bits
        '''
        bits = ""
        for i in range(nb):
            bits += self.read_bit()
        return bits
        #function to generate the byte value of an int and return it
    def byteValue(self, val):
        return self.binary_value(val, 8)
        #function that returns the binary value of an int as a byte
    def binary_value(self, val, bitsize):
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganographyException("binary value larger than the expected size")
            #making it 8bit by prefixing with zeroes
        while len(binval) < bitsize:
            binval = "0"+binval
        return binval


    def encode_binary(self, data):
        l = len(data)   # measure the length of the data
        if self.width*self.height*self.nbchannels < l+64:
            raise SteganographyException("Carrier image not big enough to hold all the datas to steganography")
        self.put_binary_value(self.binary_value(l, 64))
        for byte in data:
            byte = byte if isinstance(byte, int) else ord(byte)#ord returs the integer denoting the ascii character
            self.put_binary_value(self.byteValue(byte))
        return self.image

    def decode_binary(self):
        l = int(self.read_bits(64), 2)
        output = b""
        for i in range(l):
            output += chr(int(self.read_byte(),2)).encode("utf-8")

        return output


def main():
    args = docopt.docopt(__doc__, version="0.2")#args object is created
    in_f = args["--in"] #this represent the carrier image
    out_f = args["--out"] # this represent the encoded picture
    in_img = cv2.imread(in_f)#The function imread loads an image from the specified file and returns it.
    steg = LSBSteg(in_img)# creating the instance of the LSBSteg class and passsing the in_image

    if args['encode']:
        filename = args["--file"]
        password = args["--pass"]
        data = open(filename , "rb").read() #file that is to be hidden is read in binary format
        Encrypt(GetKey(password), filename)
        res = steg.encode_binary(data)# it call the encode binary function of the steg obeject to...
        cv2.imwrite(out_f, res)# its write the encoded binary data ont he output picture

    elif args["decode"]:
        password = args["--pass"]
        raw = steg.decode_binary()#it call the decode binary funciton of the steg object to ....
        with open(out_f, "wb") as f:# opeaning the file to write in binary format.
            f.write(raw) # it write into the file with decoded textself.

        # Decrypt(GetKey(password),out_f)


if __name__=="__main__":
    main()
