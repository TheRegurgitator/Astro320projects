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
    print("HW2Grapher 1.0")

class Star:
    idNum = -1
    dateArray = []
    magArray = []
    magErrorArray = []

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
    print("Reading Mag File...")
    magList = readDatabase() #"rmaster_phot.txt"
    print(" Done\n")
    #print(magList)
    print("Reading Dates File...")
    dateList = readDatabase() #"dateobs.txt"
    print(" Done\n")
    #print(dateList)
###################################### put into array form #####################
#hardcoded for 30 stars
    numOfStars = 30
    starNum = 0

    magit = 0
    starit = 0

    starsList = [Star() for _ in range(numOfStars)]

    for it in range(numOfStars):
        editStar = starsList[it]
        editStar.idNum = it+1
        editStar.dateArray = dateList


    for star in starsList:
        print("\n########## Star " + str(star.idNum))
        #print ("Starit " + str(starit))

        newMagArray = []
        newMagErrorArray = []

        magit = 0
        for magText in magList:
            if (magit % numOfStars != starit):
                magit +=1
            else:
                #print ("Magit" + str(magit))
                mag = float(magText[len(magText)-36:len(magText)-30])
                magError = float(magText[len(magText)-28:len(magText)-23])
                newMagArray.append(mag)
                newMagErrorArray.append(magError)

                magit +=1

        star.magArray = newMagArray
        print(star.magArray)
        star.magErrorArray = newMagErrorArray
        #time.sleep(0.1)

        starit +=1


    print(starsList[1].magArray)

    # for star in starsList:
    #     print("Star "+ str(star.idNum) + " MAL " + str(len(star.magArray))+ " Mag ")
    #     starNum +=1
###################################### conversion ##########################
    newDateList = []

    for date in dateList:
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(date[11:13])
        minute = int(date[14:16])
        second = int(date[17:19])
        newDate = datetime.datetime(year, month, day, hour, minute, second)
        newDateList.append(newDate)


###################################### graphing ##########################
    snum = 0
    minTime = datetime.datetime(newDateList[0].year, newDateList[0].month, newDateList[0].day, 0, newDateList[0].minute, newDateList[0].second)
    maxTime = datetime.datetime(newDateList[52].year, newDateList[52].month, newDateList[52].day, 9, newDateList[52].minute, newDateList[52].second)

    fig, ax = plt.subplots()
    plt.gca().invert_yaxis()
    for snum in range(0,1):
        ax.scatter(newDateList, starsList[snum].magArray, s=None)

    plt.axis([minTime,maxTime,15.55,16.65])

    ax.set(xlabel='Time (UTC)', ylabel='Relative Magnitude',
       title='Relative Magnitude of Variable Star over Time')
    ax.grid()

    fig.savefig("varstar.png")
    plt.show()

main()
