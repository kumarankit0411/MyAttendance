'''
Author: Ankit Kumar Singh copyright©2017

This code allows students of HCST to check their attendance in almost a second
'''


import requests as rq
from bs4 import BeautifulSoup as bs
import time

Id = 'Your ID (eg. hcst12cs045)'
Pass = 'Your Password(date of birth by default)'

payload = { 'txtUserId': Id, 'txtPass': Pass, '__VIEWSTATE': '/wEPDwULLTEyNDc0MTE2NTEPZBYCAgMPFgIeBmFjdGlvbgULL2lzaW0vbG9naW4WAgIJDxYCHglpbm5lcmh0bWxlZGQYwEPNs/m+JW7x/XvzS1LupkAW6RhmRWQg7UyvtTLE1g==', '__EVENTVALIDATION': '/wEWBQLV/b7AAQKz8dy8BQLKw6LdBQLa5//eAwKC3IeGDINQsvFZbXS/QtUAPao10wOIw/hKNVmHqg5prbYXR16Z', 'btnLogin': ''}
loginPage = 'http://111.93.35.142/isim/login'
attendancePage = 'http://111.93.35.142/ISIM/Student/TodayAttendence'
profilePage = 'http://111.93.35.142/ISIM/Student/Course'

def findHiddenFormValue(r):
    view = 'id="__VIEWSTATE"'
    loc = r.find(view)
    finalLoc = loc+len(view)+8
    ch = r[finalLoc]
    viewstate = ''
    while(ch !='"'):
        viewstate+=ch
        finalLoc+=1
        ch = r[finalLoc]
    view = 'id="__EVENTVALIDATION"'
    loc = r.find(view)
    finalLoc = loc+len(view)+8
    ch = r[finalLoc]
    valid = ''
    while(ch !='"'):
        valid+=ch
        finalLoc+=1
        ch = r[finalLoc]    
    return viewstate, valid    

def prettyPrint(data):
    print '\nYour total attendance is : %s%%' % (data[-1][-1])
    longestSubject = 0
    for i in data:
        if len(i[0])>longestSubject:
            longestSubject = len(i[0])
        words = i[0].split()
        if len(words)>1:
            if words[0]=='PROJECT':
                i[0] = 'PROJECT'
            else:    
                abbr = []
                for j in words:
                    if j.upper() == 'LAB':
                        abbr.append(' '+j)
                        continue
                    if j[0] != '(':
                        abbr.append(j[0])
                i[0] = ''.join(abbr)

    flag=0
    for i in data:
        if float(i[-1])<50:
            if flag==0:
                print('\n!!!WARNING!!! 50%% or less attendance in following subjects')
                flag=1
            print(i[0]+'\t\t'+i[-1])    

    print('--'*37)               
    print 'Subject\t||\tPresent\t||\tAbsent\t||\tTotal\t||\tPercentage'
    print('--'*37)
    for i in data:
        print i[0]+'\t||\t',
        print i[1]+'\t||\t',
        print i[2]+'\t||\t',
        print i[3]+'\t||\t',
        print i[4]+'\t||\t'
    print('--'*37)    

def parseName(data):
    soup = bs(data, "lxml")
    table = soup.find('label', attrs={'id':'MCPH1_SCPH_lblName'})
    print 'Welcome Mr. '+ table.text

def parseTable(page):
    soup = bs(page, "lxml")
    data = []
    table = soup.find('table', attrs={'id':'MCPH1_SCPH_GVSubject'})

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    finalData=[]
    data = data[1:] #remove empty list at top
    for i in data:
        i = i[4:]
        finalData.append([x.encode('ascii') for x in i])
    prettyPrint(finalData)

def openPage():        
    with rq.Session() as s:
        login = s.post(loginPage, data=payload)
        home = s.get(attendancePage)
        viewState, eventValidation = findHiddenFormValue(home.text)
        anotherPayload = {'__VIEWSTATE': viewState, '__EVENTVALIDATION': eventValidation,
                          'ctl00$ctl00$MCPH1$SCPH$btnSubjectWiseAtt': 'Subject Wise Attendance'}
        selectSubjectWiseAttendance = s.post(attendancePage, data=anotherPayload)
        myName = s.get(profilePage)
        parseName(myName.text)
        parseTable(selectSubjectWiseAttendance.text)

if __name__ == '__main__':
    startTime = time.time()
    openPage()
    print('Total time elapsed: %.2f seconds ' % (time.time()-startTime))
                      
