# ExamsDatesScraper
 *By the 2016 fall semester, all courses informations won't be on Pixel anymore, but on ENA so this project won't be updated.

A simple python program that connects to your Ulaval/Pixel account and recuperate all yours exams dates and return you a one page schedule with all the dates.

The program do the scraping with Mechanize and BeautifulSoup.

## Installation
You will need [Python 2](https://www.python.org/download/) to run this program. <br/> 
[pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

To install the dependencies:
```bash
pip install -r requirements.txt
```
## How to run

Run these commands on your terminal:
```bash
python ExamsDatesScraper.py 
```
And add your idul and password:
```bash
Enter your IDUL: idul
Password: 
Logging into your account ...
The dates of your exams and homeworks have been well recuperated!
```
Once you're done, it will create a excel file "ExamsCalendrier.xls".
It will look like this:
![Example](/Doc/Example_ExamsCalendrier.png)

## TODO:
Export the dates of the exams and homeworks of each course object contained in myCalendar to a real calendar.

