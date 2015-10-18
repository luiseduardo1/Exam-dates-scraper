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
    EXAM_HOMEWORK = re.compile('Intra|Final|Mini \w+|Examen [0-9]|'
                               'T[pP] ?[0-9]|Rapport|Devoir|Livrable|'
                               'Projet|Participation')

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
                        if re.match(EXAM_HOMEWORK, column.text):
                            examCounter += 1
                        columnInfo = column.get_text(strip=True)
                        examsInfos.append(columnInfo)

                for nbExam in range(examCounter):
                    exam = Exam.Exam(examsInfos[0+(nbExam)*16], 
                                     examsInfos[2+(nbExam)*16], 
                                     examsInfos[3+(nbExam)*16])
                    myCourse.examsList.append(exam) 

            # Homeworks dates
            elif re.match(HOMEWORKS, title.text) is not None:
                homeworksRows = title.next_sibling.next_sibling.find_all('tr')
                for row in homeworksRows:
                    columns = row.find_all('td')
                    for column in columns:
                        if re.match(EXAM_HOMEWORK, column.text):
                            homeworkCounter +=1
                        columnInfo = column.get_text(strip=True)
                        homeworksInfos.append(columnInfo)

                for nbHomework in range(homeworkCounter):
                    homework = Homework.Homework(homeworksInfos[0+(nbHomework)*16], 
                                                 homeworksInfos[2+(nbHomework)*16], 
                                                 homeworksInfos[3+(nbHomework)*16])
                    myCourse.homeworksList.append(homework) 
        
        # Adding each course with the dates in the calendar
        myCalendar.coursesList.append(myCourse)
        courseCounter += 1

    print "The dates of your exams and homeworks have been well recuperated!"
    return myCalendar


def writeScheduleInExcel(calendar):

    filename = 'ExamsCalendrier.xls'
    myCalendar = calendar

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet("Dates d'évaluation")

    col1_width = 256 * 28     # 28 characters wide
    col2_width = 256 * 15     # 15 characters wide
    
    try:
        for i in itertools.count():
            if (i == 0):
                sheet.col(i).width = col1_width
            else:
                sheet.col(i).width = col2_width

    except ValueError:
        pass

    col1_name = 'Évaluation:'
    col2_name = 'Date:'
    col3_name = 'Heure:'
    col4_name = 'Pourcentage'

    sheet.write(0,0, 'Université Laval')
    sheet.write(1,0, 'Session: Automne 2015') #TODO : Write automatically the actual semester

    idxRow = 3
    for course in myCalendar.coursesList:
        courseName = course.getCourseName()
        sheet.write(idxRow,0, 'Cours:'+ courseName)
        idxRow += 1
        sheet.write(idxRow,0, col1_name)
        sheet.write(idxRow,1, col2_name)
        sheet.write(idxRow,2, col3_name)
        sheet.write(idxRow,3, col4_name)
        idxRow += 1
        
        for exam in course.examsList:
            examName = exam.getName()
            sheet.write(idxRow,0, examName) 
            idxRow += 1    
        for homework in course.homeworksList:
            hwName = homework.getName()
            sheet.write(idxRow,0, hwName)
            idxRow += 1

        idxRow += 1

    book.save(filename)


if __name__ == '__main__':
    myCalendar = evaluationsScraper()
    writeScheduleInExcel(myCalendar);

