# File:        gaiagrapher.py
# Author:      Connor Jakubik
# Date:        2/4/18
# Email:       ducttapeismagic@tamu.edu
# Description: This program opens up a section of plaintext Gaia data.

# greeting function

import math
import astropy.coordinates
from astropy import units as u
from astropy.coordinates import Angle
import matplotlib.pyplot as plt
import numpy as np

def greeting():
    print("GaiaGrapher 1.0")

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def readDatabase():

    inputlist = []

    flag = True

    while flag:
        try:
            # reading in the initial file
            infile = (input("Enter the name of the file: "))
            inFile = open(infile , "r")

            for line in inFile:
                linelist = []
                # stripping the original file
                line = line.strip()
                #line = line.split('\n')
                if line !="NOT_AVAILABLE":
                    inputlist.append(line)

            flag = False

            # don't forget to close!
            inFile.close()

        except FileNotFoundError:
            print("Error reading database")

    return inputlist

def main():
    greeting()

    inputList = readDatabase()
    print("Reading File...\n")
###################################### put into array form ##########################
    listLength = len(inputList)
    dataArray = [[0 for x in range(8)] for y in range(int(listLength/8))]

    dataPtNum = 0
    star = 0

    while star < int(listLength/8):

        if(dataPtNum == 8):
            dataPtNum = 0
            star+=1

        else:
            dataArray[star][dataPtNum] = float(inputList[dataPtNum+8*star])
            dataPtNum +=1

    starNum = 0
    for i in dataArray:
        starNum +=1
        print("Star "+ str(starNum) + " " + str(i))

###################################### converting ##########################
    ras = []
    rasH = []
    rasHMS = []
    decs = []
    decsH = []
    decsHMS = []
    angle = Angle('0d')
    dists = []

    for i in dataArray:
        ras.append(i[1])
        decs.append(i[3])
        dists.append(1000/i[5])

    for j in ras:
        angle = Angle(j,u.degree)
        #print(angle.hour)
        rasH.append(angle.hour)
        rasHMS.append(angle.hms)
    for j in decs:
        angle = Angle(j,u.degree)
        #print(angle.hour)
        decsH.append(angle.hour)
        decsHMS.append(angle.hms)

    print("\n\nHMS data put into text file.")
###################################### printing HMS ##########################
    k = 0
    hr = 0
    mr = 0
    sr = 0
    hd = 0
    md = 0
    sd = 0

###################################### saving HMS to text file ##########################
    with open("HMSOutput.txt", "w") as text_file:
        while k < len(ras):
            hr, mr, sr = rasHMS[k]
            hd, md, sd = decsHMS[k]
            raLine  = str(int(hr)) + ":" + str(int(mr)) + ":" + str(truncate(sr,8))
            decLine = str(int(hd)) + ":" + str(int(md)) + ":" + str(truncate(sd,8))
            line = raLine + "-" + decLine
            print("{}".format(line), file=text_file)
            k +=1


###################################### graphing ##########################
    fig, ax = plt.subplots()
    ax.scatter(rasH, decsH, s=None, c=dists)

    ax.set(xlabel='Right Ascenstion (Hours)', ylabel='Declination (Hours)',
       title='RA and Dec of stars around Pleaides, with distance coloring')
    ax.grid()

    fig.savefig("startest.png")
    plt.show()

main()
