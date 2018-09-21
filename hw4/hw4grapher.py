# File:        hw2grapher.py
# Author:      Connor Jakubik
# Date:        3/4/18
# Email:       ducttapeismagic@tamu.edu
# Description: This program data taken from IRAF-reduced data.


import math
import datetime
import time
import astropy.coordinates
from astropy import units as u
from astropy.coordinates import Angle
import matplotlib.pyplot as plt
import numpy as np

def greeting():
    print("HW4Grapher 1.0")

class Star:
    def __init__(self):
        self.idNum = -1
        self.dateArray = []
        self.magArray = []
        self.magErrorArray = []

    @classmethod
    def appendMag(self,mag):
        magArray.append(mag)

    @classmethod
    def appendMagError(magError):
        magArray.append(magError)

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
#
# def readDatabase(inputFilename):
#
#     inputlist = []
#
#     flag = True
#
#     while flag:
#         try:
#             # reading in the initial file
#             infile = (input(str(inputFilename)))
#             inFile = open(infile , "r")
#
#             for line in inFile:
#                 linelist = []
#                 # stripping the original file
#                 line = line.strip()
#                 #line = line.split('\n')
#                 if line !="NOT_AVAILABLE":
#                     inputlist.append(line)
#
#             flag = False
#
#             # don't forget to close!
#             inFile.close()
#
#         except FileNotFoundError:
#             print("Error reading database")
#
#     return inputlist

################################################################################
def main():
    greeting()

###################################### reading ##########################
    print("Input B Magnitudes File...")
    bList = readDatabase()
    print(" Done\n")
    print(len(bList))
    print("Input V Magnitudes File...")
    vList = readDatabase()
    print(" Done\n")
    #print(vList)
###################################### put into array form #####################
#hardcoded for 30 stars
    numOfStars = 12
    starit = 0

    starMagArray = [[0 for x in range(3)] for y in range(numOfStars)]

    for bline in bList:
        bwords = bline.split()
        if starit<numOfStars:
            bmag = float(bwords[3])
            print(str(starit+1) + ' ' +  str(bmag))
            starMagArray[starit][0] = bmag
        starit +=1

    starit = 0

    for vline in vList:
        vwords = vline.split()
        if starit<numOfStars:
            vmag = float(vwords[3])
            print(str(starit+1) + ' ' + str(vmag))
            starMagArray[starit][1] = vmag
        starit +=1

    for it in range(len(starMagArray)):
        starMagArray[it][2] = starMagArray[it][0]-starMagArray[it][1]


###################################### graphing ##########################

    fig, ax = plt.subplots()
    #plt.gca().invert_yaxis()
    for snum in range(1,11):
        ax.scatter(starMagArray[snum][1],starMagArray[snum][2] , s=None)

    #plt.axis([minTime,maxTime,15.55,16.65])

    ax.set(xlabel='B-V Magnitude (units of 10 mag)', ylabel='V Magnitude (proportional)',
           title='CMD of 11 Stars in M67')
    ax.grid()

    fig.savefig("M67_CMD.png")
    plt.show()

main()
