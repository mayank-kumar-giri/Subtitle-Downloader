import os
from tkinter import filedialog
from bs4 import BeautifulSoup
import googlesearch as gs
import requests
from tkinter import *


def listallfiles(x):
    return [f for f in os.listdir(x) if os.path.isfile(os.path.join(x,f))]

def listallsubfolders(x):
    return [f for f in os.listdir(x) if not os.path.isfile(os.path.join(x,f))]

def download_for_all_files(files,x):
    for file in files:
        nn = len(file)
        t=nn
        nn = nn - 4
        #print("\nnn: ",nn,"\nt: ",t,"\n\n",file[(t-3):],"\n")
        if (file[(t-3):] == "mp4") or (file[(t-3):] =="mkv") or (file[(t-3):] =="flv") or (file[(t-3):] =="avi"):
            downloadsingle(file[:nn],x)

def download_for_subfolders(subfs,x):
    if not bool(subfs):
        return
    for sub in subfs:
        xnew = x+"/"+sub
        filestemp = listallfiles(xnew)
        subfstemp = listallsubfolders(xnew)
        download_for_all_files(filestemp,xnew)
        download_for_subfolders(subfstemp,xnew)

def askfolder(a):
    x = filedialog.askdirectory()
    folentry.insert(0,x)
    files = listallfiles(x)
    subfs = listallsubfolders(x)
    # print(files,"\n",subfs,"\n")
    status.insert(INSERT,"HELL YEAH\n")
    download_for_all_files(files,x)
    download_for_subfolders(subfs,x)
    # print(x)
    # print(os.listdir(x),"\n")
    # print([f for f in os.listdir(x) if os.path.isfile(os.path.join(x,f))])
    # print(a)

#Downloading for a single video file
def downloadsingle(q,x):
    temp = q
    q = q + " english subtitle subscene"
    tdisp = "Googling - "+q+"\n"
    status.insert(INSERT, tdisp)
    possible = []
    for j in gs.search(q, tld="com", num=10, stop=1, pause=3):
        sp = "https://subscene.com/subtitles/"
        n = len(sp)
        if j[:n] == sp:
            possible.append(j)
    fin = ""
    for p in possible:
        c = 0
        for i in p:
            if i == '/':
                c += 1
        if c == 6:
            fin = p
            break

    # print("\n\n", fin, "\n\n")
    url = fin
    tdisp = "Found URL for this movie as - " + url + "\n"
    status.insert(INSERT, tdisp)
    if not bool(url):
        tdisp = "No movie found as that of filename - " + temp + "\n\n"
        status.insert(INSERT, tdisp)
        return

    else:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        ssample = "/subtitles/english-text/"
        ssn = len(ssample)
        final = ""
        n = ssn
        for link in soup.find_all('a'):
            s = link.get('href')
            # print(s, "\n")
            if s[:n] == ssample:
                final = "https://subscene.com" + s
        # print('Beginning file download with urllib2...')
        urll = final
        if bool(urll):
            tdisp = "Downloading from URL - " + urll + "\n"
            status.insert(INSERT, tdisp)
            r = requests.get(urll, allow_redirects=True)
            location = x + "/" + temp + ".zip"
            tdisp = "Placing at location - " + location + "\n\n"
            status.insert(INSERT, tdisp)
            open(location, 'wb').write(r.content)
        else:
            tdisp = "No movie found as that of filename - " + temp + "\n\n"
            status.insert(INSERT, tdisp)
            return

#Tkinter GUI Design
root = Tk()

root.title("Subtitle Downloader - By MKG")
Label(root,text="Choose the main folder of your movie collection:").grid(row=0,column=0,sticky=W)
folentry = Entry(root,width = 85)
folentry.grid(row=1,sticky=W)
ch = Button(root,text="Select and Download")
ch.bind("<Button-1>",askfolder)
ch.grid(row=1,column=0,sticky=E)
Label(root,text="Status:").grid(row=2,column=0,sticky=W)
status = Text(root, height = 30, bd = 5)
status.grid(row=3,column=0,sticky=W)

root.mainloop()