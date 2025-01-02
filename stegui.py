import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import os.path

root = Tk()#creating the window
leftFrame = Frame(root,relief=RIDGE,borderwidth=2,width=250,height=500)#frame1 is created
leftFrame.grid(row = 0,column =0) #frame is put at the left
rightFrame = Frame(root,relief=RIDGE,borderwidth=2,width=250,height=500)#frame2 is created
rightFrame.grid(row= 0,column=5 )#frame 2 is put at the right

global cfile,msgfile, stegfile, passwd,oFileget,bytes_to_recover

oFileg = StringVar()
passwdd = StringVar()
bytorecv = StringVar()


def opencmediafile():
    global cfile
    cfile = askopenfilename()
def openmsgfile():
    global msgfile
    msgfile = askopenfilename()

def stegmedia():
    global stegfile
    stegfile = askopenfilename()
def hide():
    global cfile,msgfile,stegfile,passwd,oFileget
    oFileget = oFileg.get()
    passwd = passwdd.get()
    ext = os.path.splitext(cfile)[1]

    if ext == '.png':
        script = 'python3 LSBSteg.py encode -i ' + cfile +' -o ' + oFileget + ' -f ' + msgfile + ' -p ' + passwd
        # print('python3 LSBSteg.py encode -i ' + cfile +' -o ' + oFileget + ' -f ' + msgfile + ' -p ' + passwd)

        os.system(script)
    elif ext == '.wav':
        script = 'python3 wav-steg.py -h -d '+ msgfile + ' -s ' + cfile + ' -o ' + oFileget + ' -p ' + passwd
        os.system(script)
    elif ext == '.mov':
        script= 'python3 videosteg.py encode -i ' + cfile + ' -o ' + oFileget + ' -f ' + msgfile + ' -p ' + passwd
        os.system(script)

    else:
        exit()

    #script = 'python3 LSBSteg.py encode -i ' + cfile +' -o ' + oFileget + ' -f ' + msgfile + ' -p ' + passwd
    #os.system(script)
def unhide():
    global stegfile,passwd,oFileget,bytes_to_recover
    oFileget = oFileg.get()
    passwd = passwdd.get()
    bytes_to_recover=bytorecv.get()
    ext = os.path.splitext(stegfile)[1]
    if ext == '.png':
        script = 'python3 LSBSteg.py decode -i ' + stegfile +' -o ' + oFileget +  ' -p ' + passwd
        os.system(script)
    elif ext == '.wav':
        script = 'python3 wav-steg.py -r -s ' + stegfile + ' -o ' + oFileget + ' -p ' + passwd + ' -b ' + bytes_to_recover
        os.system(script)
    elif ext == '.mov' :
        script= 'python3 videosteg.py decode -i ' + stegfile + ' -o ' + oFileget + ' -p ' + passwd
        os.system(script)
    else:
        exit()



##
#Encode format
Luploadmedia = Label(leftFrame,text="Upload Media")
Luploadmsg = Label(leftFrame,text="Upload message file")
Lpasswd = Label(leftFrame,text="Password")
Loutfilename = Label(leftFrame,text="Outputfilename:")

carriermedia = Button(leftFrame,text="upload",width=20,command=opencmediafile)
messagefile = Button(leftFrame,text="upload",width=20,command =openmsgfile)
oFile = Entry(leftFrame,textvariable=oFileg)
password = Entry(leftFrame,textvariable=passwdd)
hideButton = Button(leftFrame,text="HIDE",width=20,command=hide)

Luploadmedia.grid(row=1,column=1,sticky=E)#allign the label in RIGHT Rem use NESW, noth east south west for direction
Luploadmsg.grid(row=3,column=1,sticky=E)
Lpasswd.grid(row=5,column=1,sticky=E)
Loutfilename.grid(row=7,column=1,sticky=E)

carriermedia.grid(row=1,column=2)
messagefile.grid(row=3 ,column=2)
password.grid(row=5,column=2)
oFile.grid(row=7,column=2)
hideButton.grid(row=9,column=3)




#DEcode format
Luploadstegmedia = Label(rightFrame,text="Steg Media")
Lpasswd = Label(rightFrame,text="Password")
Loutfilename = Label(rightFrame,text="Outputfilen:")
Lbytestorecover = Label(rightFrame,text="Bytes to recover(for audio:)")
stegmedia =  Button(rightFrame,text="upload",width=20,command=stegmedia)
oFile = Entry(rightFrame,textvariable=oFileg)
password = Entry(rightFrame,textvariable=passwdd)
Btorecover = Entry(rightFrame,textvariable=bytorecv)
unhideButton = Button(rightFrame,text="UNHIDE",width=20,command=unhide)
Luploadstegmedia.grid(row=1,column=1,sticky=E)#allign the label in RIGHT Rem use NESW, noth east south west for direction
Lpasswd.grid(row=3,column=1,sticky=E)
Loutfilename.grid(row=5,column=1,sticky=E)
stegmedia.grid(row=1,column=2)
password.grid(row=3,column=2)
oFile.grid(row=5,column=2)
unhideButton.grid(row=9,column=3)
Btorecover.grid(row=7,column=2)
Lbytestorecover.grid(row=7,column=1,sticky=E)


root.mainloop()#looping the window
