import os.path
import random
import shutil
from tkinter import Tk, Frame, BOTH, Button, Label, Entry, Radiobutton, IntVar, StringVar
from tkinter.filedialog import askdirectory
from os import walk

# Global variables
importPath = ''
exportPath = ''
availableFileList = []
importScanned = False
exportSet = False
totalFileSize = 0
sizeUnitUsed = 'o'


def testFunction():
    print('------------ Testing ------------')
    global exportSet
    global importPath
    global exportPath
    exportSet = True
    importPath = 'C:/Users/l.mallard/Documents/aTest'
    exportPath = 'C:/Users/l.mallard/Documents/aTestExport'
    setAvailablePathList()


def updateRandomizerVisibility():
    global importScanned
    global exportSet
    if importScanned and exportSet:
        copyOptionRButton1.place(x=0, y=165)
        copyOptionRButton2.place(x=120, y=165)
        CopyButton.place(x=125, y=255)
        if copyType.get() == 'number':
            fileSizeLabel.place_forget()
            fileSizeEntry.place_forget()
            fileNumberLabel.place(x=0, y=195)
            fileNumberEntry.place(x=170, y=195)
        if copyType.get() == 'size':
            fileNumberLabel.place_forget()
            fileNumberEntry.place_forget()
            fileSizeLabel.place(x=0, y=195)
            fileSizeEntry.place(x=170, y=195)
    else:
        fileNumberLabel.place_forget()
        fileNumberEntry.place_forget()
        fileSizeLabel.place_forget()
        fileSizeEntry.place_forget()
        copyOptionRButton1.place_forget()
        copyOptionRButton2.place_forget()
        CopyButton.place_forget()


def askForPath(pathType):
    if pathType == 'import':
        global importPath
        global importScanned
        importPath = askdirectory(title='Where to import from')
        importPathLabel['text'] = importPath
        importPathLabel.place(x=0, y=25)
        importScanned = False
        scanNumberLabel.place_forget()
        updateRandomizerVisibility()
    if pathType == 'export':
        global exportPath
        global exportSet
        exportPath = askdirectory(title='Where to export')
        exportPathLabel['text'] = exportPath
        exportPathLabel.place(x=0, y=120)
        if exportSet != '':
            exportSet = True
            updateRandomizerVisibility()


def getAvailablePathNumber():
    global availableFileList
    global importScanned
    global totalFileSize
    global sizeUnitUsed
    convertedSize = totalFileSize

    if convertedSize > 1000:
        convertedSize /= 1000
        sizeUnitUsed = 'Ko'
    if convertedSize > 1000:
        convertedSize /= 1000
        sizeUnitUsed = 'Mo'
    if convertedSize > 1000:
        convertedSize /= 1000
        sizeUnitUsed = 'Go'

    scanNumberLabel['text'] = str(len(availableFileList)) + ' Files found ( ' + str(
        round(convertedSize, 2)) + ' )' + sizeUnitUsed
    scanNumberLabel.place(x=45, y=55)

    fileSizeLabel['text'] = "How much " + sizeUnitUsed + " to copy"

    if len(availableFileList) > 0:
        importScanned = True
        updateRandomizerVisibility()


def setAvailablePathList():
    global importPath
    global availableFileList
    global totalFileSize

    availableFileList = []
    totalFileSize = 0

    for (dirpath, dirnames, filenames) in walk(importPath):
        for filename in filenames:
            filename = dirpath + '/' + filename
            filename = filename.replace('\\', '/')
            availableFileList.append(filename)
            totalFileSize += os.path.getsize(filename)

    getAvailablePathNumber()


def getRandomizedListByNumber():
    global availableFileList

    randomizedFileList = []
    limit = fileNumberEntry.get()

    fileNumberWarningLabel.place_forget()
    fileNumberEntry.delete(0, len(limit))
    fileNumberEntry.insert(0, '')

    if not limit.isdigit():
        fileNumberWarningLabel.place(x=0, y=220)
        return None
    if int(limit) <= 0 or int(limit) > len(availableFileList):
        fileNumberWarningLabel.place(x=0, y=220)
        return None

    alreadyUsedNumber = []
    for i in range(0, int(limit)):
        randomNumber = random.randint(0, len(availableFileList) - 1)
        while randomNumber in alreadyUsedNumber:
            randomNumber = random.randint(0, len(availableFileList) - 1)
        alreadyUsedNumber.append(randomNumber)
        randomizedFileList.append(availableFileList[randomNumber])

    return randomizedFileList


def getRandomizedListBySize():
    global availableFileList
    global totalFileSize
    global sizeUnitUsed

    randomizedFileList = []
    limit = fileSizeEntry.get()

    fileSizeWarningLabel.place_forget()
    fileSizeEntry.delete(0, len(limit))
    fileSizeEntry.insert(0, '')

    if not limit.isdigit():
        fileSizeWarningLabel.place(x=0, y=220)
        return None

    # Converting limit into o
    limit = int(limit)
    if sizeUnitUsed == 'Ko':
        limit = limit * 1000
    if sizeUnitUsed == 'Mo':
        limit = limit * 1000000
    if sizeUnitUsed == 'Go':
        limit = limit * 1000000000

    if limit <= 0 or limit > totalFileSize:
        fileSizeWarningLabel.place(x=0, y=220)
        return None

    alreadyUsedNumber = []
    currentListSize = 0
    randomNumber = random.randint(0, len(availableFileList) - 1)
    while currentListSize + os.path.getsize(availableFileList[randomNumber]) <= limit:
        alreadyUsedNumber.append(randomNumber)
        randomizedFileList.append(availableFileList[randomNumber])
        currentListSize += os.path.getsize(availableFileList[randomNumber])

        # Safety in case the user uses the size of the whole import folder
        if len(alreadyUsedNumber) == len(availableFileList):
            return randomizedFileList

        randomNumber = random.randint(0, len(availableFileList) - 1)
        while randomNumber in alreadyUsedNumber:
            randomNumber = random.randint(0, len(availableFileList) - 1)

    return randomizedFileList


def copyRandomFiles():
    global exportPath

    randomizedFileList = []
    if importScanned and exportSet:
        if copyType.get() == 'number':
            randomizedFileList = getRandomizedListByNumber()
        if copyType.get() == 'size':
            randomizedFileList = getRandomizedListBySize()

    if randomizedFileList is None:
        return

    for filePath in randomizedFileList:
        shutil.copy(filePath, exportPath)

    copyConfirmationDisplay()


def copyConfirmationDisplay():
    copyConfirmationLabel.place(x=125, y=285)


# Window creation
tkWindow = Tk()

# Tkinter global variables
copyType = StringVar()
copyType.set('number')

tkWindow.geometry('390x350')

# tkFrame creation
tkFrame = Frame(tkWindow, relief='sunken')
tkFrame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Adding elements
importPathSelectButton = Button(tkFrame, text='Import from...', command=lambda: askForPath('import'))
exportPathSelectButton = Button(tkFrame, text='Export to...', command=lambda: askForPath('export'))
scanButton = Button(tkFrame, text='Scan', command=lambda: setAvailablePathList())
CopyButton = Button(tkFrame, text='Start to copy', command=lambda: copyRandomFiles())
# todo to remove
# testButton = Button(tkFrame, text='TEST', command=lambda: testFunction())

importPathLabel = Label(tkFrame, text=importPath, borderwidth=0)
exportPathLabel = Label(tkFrame, text=exportPath, borderwidth=0)
scanNumberLabel = Label(tkFrame, text="", borderwidth=0)
fileNumberLabel = Label(tkFrame, text="How many files to copy", borderwidth=2)
fileSizeLabel = Label(tkFrame, text="How much " + sizeUnitUsed + " to copy", borderwidth=2)
copyConfirmationLabel = Label(tkFrame, text="Files copied !", borderwidth=2, fg='green')
fileNumberWarningLabel = Label(tkFrame,
                               text="Please enter a value between 0 and the amount of files scanned",
                               borderwidth=0, fg='red')
fileSizeWarningLabel = Label(tkFrame, text="Please enter a value between 0 and the size scanned", borderwidth=0,
                             fg='red')

copyOptionRButton1 = Radiobutton(tkFrame, text="Copy by number", variable=copyType, value='number',
                                 command=lambda: updateRandomizerVisibility())
copyOptionRButton2 = Radiobutton(tkFrame, text="Copy by size", variable=copyType, value='size',
                                 command=lambda: updateRandomizerVisibility())

fileNumberEntry = Entry(tkFrame)
fileSizeEntry = Entry(tkFrame)

# Position
importPathSelectButton.place(x=0, y=0)
exportPathSelectButton.place(x=0, y=95)
scanButton.place(x=0, y=50)
# todo to remove
# testButton.place(x=0, y=0)

# Running the loop
tkWindow.mainloop()
