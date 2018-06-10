import os
from tkinter import filedialog
from bs4 import BeautifulSoup
import googlesearch as gs
import requests
from tkinter import *

def exitf(a):
    root.destroy()

def listallfiles(x):
    return [f for f in os.listdir(x) if os.path.isfile(os.path.join(x,f))]

def listallsubfolders(x):
    return [f for f in os.listdir(x) if not os.path.isfile(os.path.join(x,f))]

def download_for_all_files(files,x):
    for file in files:
        nn = len(file)
        t=nn
        nn = nn - 4
        # Debugging help-
        #print("\nnn: ",nn,"\nt: ",t,"\n\n",file[(t-3):],"\n")
        if (file[(t-3):] == "mp4") or (file[(t-3):] =="mkv") or (file[(t-3):] =="flv") or (file[(t-3):] =="avi") or (file[(t-3):] == "MP4") or (file[(t-3):] =="MKV") or (file[(t-3):] =="FLV") or (file[(t-3):] =="AVI"):
            downloadsingle(file[:nn],x,nn-4)

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
    # Debugging help-
    #print(files,"\n",subfs,"\n")
    status.insert(INSERT,"Hello there!\n\n")
    download_for_all_files(files,x)
    download_for_subfolders(subfs,x)
    status.insert(INSERT, "Thanks a lot for using!\n")
    input = status.get("1.0", 'end-1c')
    loc = x+"/"+"Report.txt"
    f = open(loc, 'w')
    f.write(input)
    f.close()
    ins.insert(INSERT, "Report has been saved in the main folder.\nTo download subtitles for another collection, please Restart the application.\nClick Exit to quit application.\n")
    # Debugging help-
    # print(x)
    # print(os.listdir(x),"\n")
    # print([f for f in os.listdir(x) if os.path.isfile(os.path.join(x,f))])

#Downloading for a single video file
def downloadsingle(q,x,qso):
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

    # Debugging help-
    #print("\n\n", fin, "\n\n")
    url = fin
    tdisp = "Found URL for this movie as - " + url + "\n"
    status.insert(INSERT, tdisp)
    if not bool(url):
        tdisp = "Couldn't find movie from this filename - " + temp + "\n\n"
        status.insert(INSERT, tdisp)
        nnn = len(temp)
        nnn = (3 * nnn) / 4
        nnn = int(nnn)
        if nnn >= int(qso / 2):
            tdisp = "Retrying...(With 75% of file name)\n"
            status.insert(INSERT, tdisp)
            q = temp[:nnn]
            downloadsingle(q, x, qso)
        return

    else:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        ssample = "/subtitles/english-text/"
        ssn = len(ssample)
        final = ""
        n = ssn
        for link in soup.find_all('a'):
            s = link.get('href')
            #Debugging help-
            #print(s, "\n")
            if s[:n] == ssample:
                final = "https://subscene.com" + s
        #Debugging help-
        #print('Beginning file download with urllib2...')
        urll = final
        # Debugging help-
        #print(urll,"\n")
        if bool(urll):
            tdisp = "Downloading from URL - " + urll + "\n"
            status.insert(INSERT, tdisp)
            r = requests.get(urll, allow_redirects=True)
            location = x + "/" + temp + ".zip"
            tdisp = "Placing at location - " + location + "\n\n"
            status.insert(INSERT, tdisp)
            open(location, 'wb').write(r.content)
        else:
            tdisp = "Couldn't find movie from this filename - " + temp + "\n\n"
            status.insert(INSERT, tdisp)
            nnn=len(temp)
            nnn=(3*nnn)/4
            nnn = int(nnn)
            if nnn>=int(qso/2):
                tdisp = "Retrying...(With 75% of file name)\n"
                status.insert(INSERT, tdisp)
                q = temp[:nnn]
                downloadsingle(q,x,qso)
            return

#Tkinter GUI Design
root = Tk()

root.iconbitmap(default='icon.ico')
root.title("Subtitle Downloader - By MKG")
Label(root,text="Choose the main folder of your movie collection:").grid(row=0,column=0,sticky=W)
folentry = Entry(root,width = 77)
folentry.grid(row=1,sticky=W)
ch = Button(root,text="Select and Download")
ch.bind("<Button-1>",askfolder)
ch.grid(row=1,column=0,sticky=E)
Label(root,text="Instructions:").grid(row=2,column=0,sticky=W)
ins = Text(root, height = 6, width = 72, bd = 8, font=("Times", 12))
ins.grid(row=3,column=0,sticky=W)
ins.insert(INSERT,"It'll take a while for all the subtitles to download. Do NOT close the application. Report will be generated below, once the task is completed. \nDo NOT close the application even if it's displayed 'NOT RESPONDING'.\n")
Label(root,text="Report:").grid(row=4,column=0,sticky=W)
status = Text(root, height = 18, width = 72, bd = 5, font=("Times", 12))
status.grid(row=5,column=0,sticky=W)
ch = Button(root,text="Exit",width = 8)
ch.bind("<Button-1>",exitf)
ch.grid(row=6,column=0,sticky=E)

root.mainloop()