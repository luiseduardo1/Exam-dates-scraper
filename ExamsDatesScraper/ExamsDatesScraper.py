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

    # Login to your Pixel account
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


if __name__ == '__main__':
    evaluationsScraper()

