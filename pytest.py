#### BEGIN IMPORT SECTION ####
import requests
from bs4 import BeautifulSoup as bs
from scipy.stats import chisquare
from math import log10
#### END IMPORT SECTION ####


#### BEGIN FUNCTION/CLASS DEFINITION ####
def getsource(url='https://county.milwaukee.gov/EN/County-Clerk/Off-Nav/Election-Results/Election-Results-Fall-2020'):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    r = requests.get(url,headers=headers)
    data = r.text
    soup=bs(data,"html.parser")
    return soup

def getBenfords():
    #This is a function I'm making to create a list with the expected values so I can do a chi squared test later
    expected = [log10(1+1/d) for d in range(1,10)]
    return expected

def chiTest(actual,expected):
    return chisquare(f_obs=actual,f_exp=expected)

def calcfreqs(inlist,num):
    if (num==1):
        inlist[0] = inlist[0]+1
    elif (num==2):
        inlist[1] = inlist[1]+1
    elif (num==3):
        inlist[2] = inlist[2]+1
    elif (num==4):
        inlist[3] = inlist[3]+1
    elif (num==5):
        inlist[4] = inlist[4]+1
    elif (num==6):
        inlist[5] = inlist[5]+1
    elif (num==7):
        inlist[6] = inlist[6]+1
    elif (num==8):
        inlist[7] = inlist[7]+1
    elif (num==9):
        inlist[8] = inlist[8]+1
    return inlist
#### END FUNCTION/CLASS DEFINITION ####


#### BEGIN SCRIPT EXECUTION ####
dataDict = {'Num':[],'Ward':[],'Biden':[],'Trump':[],'Blankenship':[],'Jorgensen':[],'Carroll':[],'Writein':[]}
benfords = getBenfords()
biden = [0,0,0,0,0,0,0,0,0]
trump = [0,0,0,0,0,0,0,0,0]
blankenship = [0,0,0,0,0,0,0,0,0]
jorgensen = [0,0,0,0,0,0,0,0,0]
carroll = [0,0,0,0,0,0,0,0,0]
writein = [0,0,0,0,0,0,0,0,0]
datalist = getsource().findAll('table',{'class':'precinctTable'})
count = 1
header = True
for val in datalist[1].findAll('td'):
    if (header and count != 8):
        count+=1
        continue
    elif (header and count == 8):
        count = 1
        header = False
        continue
    if count == 1:
        dataDict['Num'].append(val.text)
    elif count == 2:
        dataDict['Ward'].append(val.text)
    elif count == 3:
        dataDict['Biden'].append(val.text)
        biden = calcfreqs(biden,int(val.text[0]))
    elif count == 4:
        dataDict['Trump'].append(val.text)
        trump = calcfreqs(trump,int(val.text[0]))
    elif count == 5:
        dataDict['Blankenship'].append(val.text)
        blankenship = calcfreqs(blankenship,int(val.text[0]))
    elif count == 6:
        dataDict['Jorgensen'].append(val.text)
        jorgensen = calcfreqs(jorgensen,int(val.text[0]))
    elif count == 7:
        dataDict['Carroll'].append(val.text)
        carroll = calcfreqs(carroll,int(val.text[0]))
    elif count == 8:
        dataDict['Writein'].append(val.text)
        writein = calcfreqs(writein,int(val.text[0]))
        count = 0
    count+=1

bidenexpected = [sum(biden)*a for a in benfords]
trumpexpected = [sum(trump)*a for a in benfords]
blankenshipexpected = [sum(blankenship)*a for a in benfords]
jorgensenexpected = [sum(jorgensen)*a for a in benfords]
carrollexpected = [sum(carroll)*a for a in benfords]
writeinexpected = [sum(writein)*a for a in benfords]
bidenchival,bidenpval = chiTest(biden,bidenexpected)
trumpchival,trumppval = chiTest(trump,trumpexpected)
blankenshipchival,blankenshippval = chiTest(blankenship,blankenshipexpected)
jorgensenchival,jorgensenpval = chiTest(jorgensen,jorgensenexpected)
carrollchival,carrollpval = chiTest(carroll,carrollexpected)
writeinchival,writeinpval = chiTest(writein,writeinexpected)
print(bidenchival,trumpchival)
print(bidenpval,trumppval) #the p-value for Biden and Trump first digit frequency goodness-of-fit test against Benford's
print(biden,trump,bidenexpected,trumpexpected) #the raw counts of Biden and Trump first digit frequencies