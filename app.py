from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server
import sys
import ssl
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

app = Flask(__name__)


d=256

def getMatches(db,course,maximumNumberOfResults):

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    if maximumNumberOfResults == 0:
        maximumNumberOfResults = sys.maxsize
    commonCourseWords = ['OF','THE','A','INTRODUCTION','INTRO','FUNDAMENTALS','IN','EVERY']
    if course in commonCourseWords:
        return []
    generalMatchCount = 0
    matchCount = 0
    course = course.upper()
    course = course.replace('.','')
    matches = dict()
    generalMatches = dict()
    for school,url in db.items():
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        webtext = BeautifulSoup(html,features="html.parser").get_text().upper()
        course_without_ap = nonAP(course)
        #if webtext.find(course) != -1 or webtext.find(course_without_ap) != -1:
        #if containsSubstr(webtext,course) or containsSubstr(webtext,course_without_ap):
        if search(course,webtext,101):
            matches[school] = url
            matchCount += 1
            if matchCount == maximumNumberOfResults:
                break
        if len(matches) == 0:
            if search(course_without_ap,webtext,101):
                matches[school] = url
                matchCount += 1
                if matchCount == maximumNumberOfResults:
                    break
            else:
                words = course_without_ap.split()
                flag = False
                for word in words:
                    if word in commonCourseWords:
                        continue
                    #if webtext.find(word) != -1:
                    #if containsSubstr(webtext,word):
                    if search(word,webtext,101):
                        flag = True
                        break
                if flag:
                    generalMatches[school] = url
                    generalMatchCount += 1
                    if generalMatchCount == maximumNumberOfResults:
                        break
    if len(matches) == 0:
        return generalMatches
    return matches

def nonAP(course):
    if course[0:3] == 'AP ':
        return course[3:]
    return course

def containsSubstr(wholestr,substr):
    for index in range(len(wholestr)-len(substr)):
        if substr == wholestr[index:index+len(substr)]:
            return True
    return False

def search(pat, txt, q):
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0    # hash value for pattern
    t = 0    # hash value for txt
    h = 1
 
    # The value of h would be "pow(d, M-1)%q"
    for i in range(M-1):
        h = (h*d)%q
 
    # Calculate the hash value of pattern and first window
    # of text
    for i in range(M):
        p = (d*p + ord(pat[i]))%q
        t = (d*t + ord(txt[i]))%q
 
    # Slide the pattern over text one by one
    for i in range(N-M+1):
        # Check the hash values of current window of text and
        # pattern if the hash values match then only check
        # for characters on by one
        if p==t:
            # Check for characters one by one
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break
                else: j+=1
 
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j==M:
                return True
 
        # Calculate hash value for next window of text: Remove
        # leading digit, add trailing digit
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q
 
            # We might get negative values of t, converting it to
            # positive
            if t < 0:
                t = t+q
    return False

def run():
    put_markdown('# ***UC Match: High School Course Search***')
    courseName = ''
    put_text('High Schoolers take extra courses outside or their school to gain extra knowledge, improve their transcript, and showcase to colleges their intellectual capacity. Search up a course in this engine and visit the online/summer academies that teach the course!')
    while len(courseName) < 4:
        courseName = input("Enter Course：")
    numberOfMatches = ''
    while not numberOfMatches.isnumeric():
        numberOfMatches = input("Enter maximum number of matches you would like to view (put in 0 for all results): ")
    preferredNumberOfMatches = int(numberOfMatches)
    clear()
    put_markdown('# ***UC Match: High School Course Search***')
    put_loading()
    put_text('    This might take a while...',sep='',inline=True,scope=-1,position=-1)

    
    db = dict()
    db['UC Scouts'] = 'https://www.ucscout.org/courses/'
    db['BYU Independent Study'] = 'https://is.byu.edu/catalog?school=11'
    db['Apex Learning'] = 'https://www.apexlearning.com/catalog'
    db['Mt. Everest Academy Independent Study'] = 'https://mteverest.sandiegounified.org/academics/advanced_coursework'
    db['iUniversity Prep'] = 'https://www.iuniversityprep.org/course-descriptions'
    db['UC Berkeley ATDP'] = 'https://atdp.berkeley.edu/programs/sd/catalog/'
    db['Quarry Lane Summer Academy'] = 'https://www.quarrylane.org/summer/courselisting'
    db['Stanford Summer Session'] = 'https://summer.stanford.edu/courses'
    db['Stanford Pre-Collegiate Summer Institute'] = 'https://summerinstitutes.spcs.stanford.edu/courses/2021?time=1628217671788'
    db['UC San Diego Academic Connections'] = 'https://academicconnections.ucsd.edu/onlinecourses/index.html'
    db['UCLA Summer Sessions'] = 'https://www.summer.ucla.edu/ushsstudent'
    db['USC Summer Programs'] = 'https://summerprograms.usc.edu/program-overview/options/'
    db['COSMOS'] = 'https://cosmos-ucop.ucdavis.edu/app/main/page/campuses-and-clusters'
    db['Brandeis Precollege Online Program'] = 'https://brandeis.precollegeprograms.org/?utm_campaign=BU%3A%20Nurturing&utm_medium=email&_hsmi=133739685&_hsenc=p2ANqtz-9a2Mnvjpv6z_JxZPHBdbMYhnaeHPvcoSWQp3yLFn5Zm_njVuhc03M2uaCXlAMWfojPTiXE8fuXQlGgTWXfwiDEJvg0tA&utm_content=133739685&utm_source=hs_automation#'
    db['Syracuse University Office of Pre-College Programs'] = 'https://precollege.syr.edu/programs-courses/summer-college-online/summer-college-online-program-listing/'
    db['Columbia University Pre-college'] = 'https://precollege.sps.columbia.edu/highschool/online/courses/3-week'
    db['Illinois Tech Pre-College Program'] = 'https://www.iit.edu/academics/pre-college-programs/summer'
    db['Harvard Summer School'] = 'https://summer.harvard.edu/course-catalog/ssp-courses'
    db['University of Massachusetts Amhers'] = 'https://www.umass.edu/uww/programs/pre-college/summer'

    matches = getMatches(db,courseName,preferredNumberOfMatches)
    clear()
    put_markdown('# ***UC Match: High School Course Search***')
    if len(matches) == 0:
        put_text('No matches generated')
    else:
        put_markdown('# **Matches**')
        for key,value in matches.items():
            put_text(key+' ('+value+')')

#app.add_url_rule('/tool', 'webio_view', webio_view(run),methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(run, port=args.port)
#if __name__ == '__main__':
    #predict()

#app.run(host='localhost', port=80)

#visit http://localhost/tool to open the PyWebIO application.
