"""videosteg.py

Usage:
  videosteg.py encode -i <input> -o <output> -f <file> -p <password>
  videosteg.py decode -i <input> -o <output>  -p <password>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file=<file>          File to hide/unhide
  -i,--in=<input>           Input video(carrier)
  -o,--out=<output>         Output video (or extracted file)
  -p,--pass=<password>      Password for encryption
"""
from functions import *
from subprocess import call,STDOUT
import os
import docopt
from  simp_AES import *

def main():
    args = docopt.docopt(__doc__, version="0.2")#args object is created

    file_name = args["--in"]
    password = args["--pass"]
    if args['encode']:
        #file_name = args["--in"]
        textfile = args["--file"]
        fileout = args["--out"]
        try:
            open(file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        frame_extract(str(file_name))
        print("(-) Extracting audio")
        # using system call
        #ffmpeg -i data/chef.mp4 -q:a 0 -map a temp/audio.mp3 -y
        # 2>/dev/null for supressing the output from ffmpeg
        call(["ffmpeg", "-i",str(file_name), "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        print("(-) Reading text-to-hide")
        print("(-) Encrypting & appending string into frame(s) ")
        ##add encryption here
        encode_frame("temp", textfile)
        Encrypt(GetKey(password), textfile)
        print("(-) Merging frame(s) ")
        #ffmpeg -i temp/%d.png -vcodec png data/enc-filename.mov
        call(["ffmpeg", "-i", "temp/%d.png" , "-vcodec", "png", "temp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        print("(-) Optimizing encode & Merging audio ")
        # ffmpeg -i temp/temp-video.avi -i temp/audio.mp3 -codec copy data/enc-chef.mp4 -y
        call(["ffmpeg", "-i", "temp/video.mov", "-i", "temp/audio.mp3", "-codec", "copy",str(fileout) +".mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        print(("(!) Success , output @" + str(fileout)+".mov"))

    elif args["decode"]:
        fileout = args["--out"]
        try:
            open(file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        frame_extract(str(file_name))
        print("(-) Decrypting Frame(s)")
        decode_frame("temp",fileout)
        #add decryption here Decrypt(GetKey(password), file_name)
        print("(-) Writing to recovered-text.txt")
        print("(!) Success")

    else:
        exit()
if __name__=="__main__":
    main()
