import os
import re

path = "./"

directories = os.listdir(path)
cues = os.path.join(path, "cues")
# myRe = re.compile('FILE "(.*)"')

def writeCues(myL, name):
    cues_file = os.path.join(cues, name)
    counter = 1
    with open(cues_file, "w", encoding="utf-8") as output: 
        for i in myL:
            output.write("FILE \"{}\" WAVE\n".format(i))
            output.write("  TRACK {:02d} AUDIO\n".format(counter))
            output.write("    INDEX 01 00:00:00\n")
            counter = counter + 1

def moveCues(path, prefix, name):
    try:
        with open(path,"r", encoding="utf8") as input:
            data = input.read()
            with open(os.path.join(cues, name), "w", encoding="utf8") as output:
                output.write(re.sub('FILE "(.*)"', lambda m: "FILE \"" + os.path.join(prefix, m.group(1)) + "\"", data))
    except Exception as e:
        print(e)

def isSong(files):
    return files.endswith(".flac") or files.endswith(".mp3") or files.endswith(".wav") or files.endswith(".m4a")

def findFlac(path, prefix):
    myL = []
    if not os.path.isdir(path):
        return myL
    lst = os.listdir(path)
    lst.sort()
    for files in lst:
        if isSong(files):
            myL.append(os.path.join(prefix, files))
        elif files.endswith(".cue"):
            moveCues(os.path.join(path, files), prefix, files)
               

    for files in lst:
        if (os.path.isdir(os.path.join(path, files))):
            myL = myL + findFlac(os.path.join(path, files), os.path.join(prefix, files))
        
    return myL
if "cues" not in directories:
    os.mkdir(cues)
for cdir in directories:
    if cdir == "cues":
        continue
    if isSong(cdir):
        writeCues([os.path.join("..", cdir)], cdir[:cdir.find('.')] + ".cue")
    else:
        myL = findFlac(os.path.join(path, cdir), os.path.join("..", cdir))
        if myL:
            writeCues(myL, cdir + ".cue")
