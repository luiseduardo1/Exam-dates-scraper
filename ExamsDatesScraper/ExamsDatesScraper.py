#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script that connect to your pixel account and recuperate the date of your exams/homeworks

import Homework
import Exam
import Course
import Calendar

from bs4 import BeautifulSoup
import mechanize
import cookielib
import getpass
import re

import xlwt
import itertools

def evaluationsScraper():
    EXAMS = re.compile('Examens :')
    HOMEWORKS = re.compile('Travaux \w+')
    EXAM_HOMEWORK = re.compile('[Ii]ntra|Final|Mini \w+|Examen \S+|'
                               'T[pP] ?[0-9]|Rapport|Devoir|Livrable|'
                               'Projet|Participation|Travail|Évaluation')

    myCalendar = Calendar.Calendar()
    USERNAME = raw_input("Enter your IDUL: ")
    PASSWORD = getpass.getpass()

    # Emulating a web browser
    browser = mechanize.Browser()

    # Storing the cookies
    cookieJar = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookieJar)

    # Logging to your Pixel account
    print ("Logging into your account ...")
    browser.open('https://pixel.fsg.ulaval.ca/')
    browser.select_form(name="form_login")
    browser['code_utilisateur'] = USERNAME 
    browser['password'] = PASSWORD 
    browser.submit()

    # Once logged, connecting to the page "Sommaire des cours"
    url = browser.open('https://pixel.fsg.ulaval.ca/liste_cours/sommaire_cours_etudiant.pl?seq_menu_application=258')
    response = url.read()
    soup = BeautifulSoup(response, "lxml")

    # Recuperating all the page links for each course
    classLinkList = []
    for link in soup.find_all("a"):
        javascriptLinks = link.get("href")
        if "javascript: centerPopUp(" in javascriptLinks:
            param, value = javascriptLinks.split("'",1)
            classLink = value.split("'",1)[0]
            classLinkList.append(classLink)


    # Iterating through each course and collecting all exams/homeworks dates
    courseCounter = 0
    for classLink in classLinkList:
        classurl = browser.open(classLink)
        soup = BeautifulSoup(classurl, "lxml")

        courseName = soup.find('td', {"class":"Boite_Entete_Popup_Texte"}).text
        myCourse = Course.Course(courseName)

        examCounter = 0
        homeworkCounter = 0
        examsInfos = []
        homeworksInfos = []

        titleSections = soup.body.find_all('td', {"class":"Form_Libelle"})
        for title in titleSections:

            # Exams dates
            if re.match(EXAMS, title.text) is not None:
                examsRows = title.next_sibling.next_sibling.find_all('tr')
                for row in examsRows:
                    columns = row.find_all('td')
                    for column in columns:
                       # Text is encoded in utf-8 so that the regex can work
                        if re.match(EXAM_HOMEWORK, (column.text).encode('utf-8')):
                            examCounter += 1
                        if re.match('Local',(column.text).encode('utf-8')):
                            localInfo = (column.get_text().encode('utf-8')).split(": ")
                            columnInfo = localInfo[1]
                            examsInfos.append(columnInfo)
                        else:
                            columnInfo = column.get_text(strip=True)
                            examsInfos.append(columnInfo)

                # Getting name, date, period, value
                for nbExam in range(examCounter):
                    exam = Exam.Exam(examsInfos[0+(nbExam)*16], 
                                     examsInfos[2+(nbExam)*16], 
                                     examsInfos[3+(nbExam)*16],
                                     examsInfos[5+(nbExam)*16],
                                     examsInfos[10+(nbExam)*16])
                    myCourse.examsList.append(exam) 

            # Homeworks dates
            elif re.match(HOMEWORKS, title.text) is not None:
                homeworksRows = title.next_sibling.next_sibling.find_all('tr')
                for row in homeworksRows:
                    columns = row.find_all('td')
                    for column in columns:                            
                       # Text is encoded in utf-8 so that the regex can work
                        if re.match(EXAM_HOMEWORK, (column.text).encode('utf-8')):
                            homeworkCounter +=1
                        columnInfo = column.get_text(strip=True)
                        homeworksInfos.append(columnInfo)

                # Getting name, date, period, value
                for nbHomework in range(homeworkCounter):
                    homework = Homework.Homework(homeworksInfos[0+(nbHomework)*16], 
                                                 homeworksInfos[2+(nbHomework)*16], 
                                                 homeworksInfos[3+(nbHomework)*16],
                                                 homeworksInfos[11+(nbHomework)*16])
                    myCourse.homeworksList.append(homework) 
        
        # Adding each course with the dates in the calendar
        myCalendar.coursesList.append(myCourse)
        courseCounter += 1

    print "The dates of your exams and homeworks have been well recuperated!"
    return myCalendar


def writeScheduleInExcel(calendar):

    filename = 'Calendar/ExamsCalendrier.xls'
    myCalendar = calendar

    style0 = xlwt.easyxf('font:name Arial, color-index black, bold on')
    style1 = xlwt.easyxf('font:name Arial, color-index blue, bold on')
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet("Dates d'évaluation")

    firstColWidth = 256 * 25     # 25 characters wide
    valueColWidth = 256 * 8      # 8 characters wide 
    hourColWidth = 256 * 16      # 16 characters wide 
    othersColWidth = 256 * 14    # 14 characters wide
    
    try:
        for i in itertools.count():
            if (i == 0):
                sheet.col(i).width = firstColWidth
            elif (i == 2):
                sheet.col(i).width = hourColWidth
            elif (i == 3):
                sheet.col(i).width = valueColWidth
            else:
                sheet.col(i).width = othersColWidth

    except ValueError:
        pass

    examCol1 = 'Examens:'
    examCol2 = 'Date:'
    examCol3 = 'Heure:'
    homeworkCol1 = "Travaux d'évaluation: "
    homeworkCol2 = 'Date de remise:'
    homeworkCol3 = 'Heure de remise:'
    localCol = 'Local: '
    valueCol4 = 'Valeur: ' 

    sheet.write(0,0, 'Université Laval', style0)
    sheet.write(1,0, 'Session: Automne 2015', style0) #TODO : Write automatically the actual semester

    idxRow = 3
    for course in myCalendar.coursesList:
        courseName = course.getCourseName()
        sheet.write(idxRow,0, 'Cours: '+ courseName, style1)
        idxRow += 1
        
        sheet.write(idxRow,0, examCol1,style0)
        sheet.write(idxRow,1, examCol2, style0)
        sheet.write(idxRow,2, examCol3, style0)
        sheet.write(idxRow,3, valueCol4, style0)
        sheet.write(idxRow,4, localCol, style0)
        idxRow += 1
        
        for exam in course.examsList:
            sheet.write(idxRow,0, exam.getName())
            sheet.write(idxRow,1, exam.getDate())
            sheet.write(idxRow,2, exam.getTimePeriod())
            sheet.write(idxRow,3, exam.getValue())
            sheet.write(idxRow,4, exam.getLocal())
            idxRow += 1 
        
        if course.homeworksList:
            idxRow += 1
            sheet.write(idxRow,0, homeworkCol1, style0)
            sheet.write(idxRow,1, homeworkCol2, style0)
            sheet.write(idxRow,2, homeworkCol3, style0)
            sheet.write(idxRow,3, valueCol4, style0)
            idxRow += 1


            for homework in course.homeworksList:
                sheet.write(idxRow,0, homework.getName())
                sheet.write(idxRow,1, homework.getDueDate())
                sheet.write(idxRow,2, homework.getDueHour())
                sheet.write(idxRow,3, homework.getValue())
                idxRow += 1

        idxRow += 1

    book.save(filename)

if __name__ == '__main__':
    myCalendar = evaluationsScraper()
    writeScheduleInExcel(myCalendar);

