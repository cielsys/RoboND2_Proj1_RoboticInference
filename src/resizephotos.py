from PIL import Image
import os
import sys
import glob
import random


#============= globals
g_doCreateFiles = False

#--------------------------------- CreateDataSetFromImageFiles
def GetgArgs():
    gArgs = type("GlobalArgsContainer", (object,), {})

    # For debug testing only
    gArgs.truncatedTrainingSetSize = 0 # Default: 0 (Use full training sets). Truncation is for speedup of debug cycle

    gArgs.newImageSize = (256, 256)

    # I/O Directories
    gArgs.trainingFilesDirIn = "../../Assets/raw/"
    gArgs.trainingFilesDirOut = "../../Assets/raw_resized_256x256/"

    return gArgs


#--------------------------------- GetAllInputFileNames
def FindAllInputFileNames(dirIn, fileExt, truncatedTrainingSetSize=0):
    dirInFQ = os.path.abspath(dirIn) + "/"
    fileSpec =  dirInFQ + "**/" + fileExt

    print("Finding input files: {}... ".format(fileSpec), flush=True)
    fileNamesInFQ = glob.glob(fileSpec, recursive=True)
    print("Found {} image files. ".format(len(list(fileNamesInFQ))), end ='')

    if truncatedTrainingSetSize > 0 :
        print("Truncating to {} image files.".format(truncatedTrainingSetSize), end ='')
        fileNamesInFQ = random.sample(fileNamesInFQ, truncatedTrainingSetSize)

    print("\n")
    fileNamesInRel = []
    for fileNameIndex, fileNameInFQ in enumerate(fileNamesInFQ):
        fileNameInRel = fileNameInFQ.replace(dirInFQ, '')
        fileNamesInRel.append(fileNameInRel)
        #print("Input file: {}".format(fileNameInRel), flush=True)

    return(fileNamesInRel, fileNamesInFQ)

#--------------------------------- CreateOutputFileNames
def CreateOutputFileNames(dirOut, fileNamesInRel):
    dirOutFQ = os.path.abspath(dirOut) + "/"
    fileNamesOutFQ = []

    for fileNameIndex, fileNameOutRel in enumerate(fileNamesInRel):
        fileNameOutFQ = dirOutFQ + fileNameOutRel
        fileNamesOutFQ.append(fileNameOutFQ)

    return(fileNamesOutFQ)

#--------------------------------- SelectRandom
def CreateTestList(listAllItems, numItems):
    listSelectedItems = random.sample(listAllItems, numItems)

    print("")
    for item in listSelectedItems:
        print("{}".format(item))


#--------------------------------- EnsureDirExists
def EnsureDirExists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#--------------------------------- ResizeImageFile
def ResizeImageFile(newImageSize, fileNameInFQ, fileNameOutFQ):
    img = Image.open(fileNameInFQ)
    oldImageSize = img.size
    if g_doCreateFiles:
        strAction = "Resizing"
    else:
        strAction = "DRYRUN"

    print("{}: {}({}) ==>({}) {}".format(strAction, fileNameInFQ, oldImageSize, newImageSize, fileNameOutFQ), flush=True)
    EnsureDirExists(fileNameOutFQ)
    if (g_doCreateFiles):
        img = img.resize(newImageSize, Image.ANTIALIAS)
        img.save(fileNameOutFQ, 'JPEG', quality=90)

#--------------------------------- ResizeImageFiles
def ResizeImageFiles(newImageSize, fileNamesInFQ, fileNamesOutFQ):

    for fileNameIndex, fileNameInFQ in enumerate(fileNamesInFQ):
        fileNameOutFQ = fileNamesOutFQ[fileNameIndex]
        ResizeImageFile(newImageSize, fileNameInFQ, fileNameOutFQ)

#====================== Main() =====================
def Main(gArgs):
    fileNamesInRel, fileNamesInFQ = FindAllInputFileNames(gArgs.trainingFilesDirIn, fileExt = '*.JPG', truncatedTrainingSetSize = gArgs.truncatedTrainingSetSize)
    fileNamesOutFQ = CreateOutputFileNames(gArgs.trainingFilesDirOut, fileNamesInRel)
    ResizeImageFiles(gArgs.newImageSize, fileNamesInFQ, fileNamesOutFQ)

    numItems =  10
    CreateTestList(fileNamesInRel, numItems)

#====================== Main Invocation =====================
if ((__name__ == '__main__')):
    Main(GetgArgs())