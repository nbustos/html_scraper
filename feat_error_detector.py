#  AUTHOR   - NB
#  DATE     - 1/28/2022
#  FUNCTION - HTML scraper to check for error messages in feat reports.html
#  USAGE    - for running after a featloop to make sure none of the subs got an error

# You will probably need to install beautiful soup and requests to your environment - NB - run in base env
import requests
import re, os
from bs4 import BeautifulSoup
import csv
import sys
import urllib.request

#### CHANGE FOR STUDY - FEAT DIRECTORY - string YOU WANT TO SEARCH FOR!:
study = '/bcdlab/CHARM'  # eg: 'bcdlab/CURforDAD/AD' if I want to search through AD subjects
featfiles = 'NPU-A_prepro_sustained-only.feat'  # eg: 'R1_GT.feat'  if I want to look through the resting preprocessing called R1_GT
visit = 'V1'  # eg: 'V1' if i am interested in visit one
error_string = 'Errors occured'
listofbadsubjects = []  # List to carry all subs found to have error in feat
subswithoutthatdir = []  # List to carry all subs who didn't have the feat file at all

print("\n" * 5)
print("***********************************************************************")
print("")
print("Running Feat - HTML parser for study: ", study, "and featfiles: ", featfiles)
print("\n" * 3)
print("***********************************************************************")


# Function to parse the html for the error string
def checkfeaterrors():
    for string in body.stripped_strings:
        # print(repr(string))
        if error_string in string:
            print("***			Houston we have a problem -->  Subject-", subj)
            listofbadsubjects.append(subj)


# Go through study director as entered above and iterate over subjects:
# Currently set up for CHARM
for subj in os.listdir(study):
    if subj[0].isdigit() and subj[-1].isdigit():
        #print(subj)
        dfilelocation = os.path.join(study, subj, 'convert', featfiles)
		# print('searching through:', dfilelocation)
		# dfilelocation: is the feat directory that has the designfile
		# strtosearchfor: is the string you are looking for within the designfile
        if os.path.exists(dfilelocation):
            os.chdir(dfilelocation)
            HTMLFileToBeOpened = open("report.html", "r")
            # Reading the file and storing in a variable
            contents = HTMLFileToBeOpened.read()
            # To check the contents of the parse print(contents)
            # print(contents)
            # Creating a BeautifulSoup object and specifying the parser (can be 'lxml' or 'html.parser')
            bSoup = BeautifulSoup(contents, 'html.parser')
            # This is the specific "child" that contains the string of interest
            body = bSoup.contents[2]
            # Call function and pass the parsed body
            checkfeaterrors()
        else:
            subswithoutthatdir.append(subj)
            #print('-------------------------------------------------------------------')
            #print('-0-0-0-0-0-0 Feat dir was not found under that name-0-0-0-0-0-0')
            #print('-------------------------------------------------------------------')
            #print('')

# OUTPUT :
print("************************************************************************************************")
print("\n" * 3)
print("-----------------                OUTPUT                  -------------------")
print("\n" * 3)

listofbadsubjects.sort()
print("    There were: ", len(listofbadsubjects), "subjects found with errors in feat analysis:   \n")
print(*listofbadsubjects, sep=" ")
print("\n" * 3)


subswithoutthatdir.sort()
print("    There were: ", len(subswithoutthatdir), "subjects found without a feat analysis of given name:   ", featfiles, "\n")
print(*subswithoutthatdir, sep=" ")
print("\n" * 3)
print("DONE")
print("\n" * 3)





