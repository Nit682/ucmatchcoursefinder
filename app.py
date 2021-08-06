from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getMatches(db,course):
    course = course.upper()
    course = course.replace('.','')
    matches = dict()
    generalMatches = dict()
    webTexts = list()
    for school,url in db.items():
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        webtext = BeautifulSoup(html,features="html.parser").get_text().upper()
        webTexts.append(webtext)
    index = 0
    for school,url in db.items():
        webtext = webTexts[index]
        course_without_ap = nonAP(course)
        if webtext.find(course) != -1 or webtext.find(course_without_ap) != -1:
            matches[school] = url
        if len(matches) == 0:
            words = course_without_ap.split()
            flag = False
            for word in words:
                if webtext.find(word) != -1:
                    flag = True
                    break
            if flag:
                generalMatches[school] = url
        index+=1
    if len(matches) == 0:
        return generalMatches
    return matches

def nonAP(course):
    if course[0:3] == 'AP ':
        return course[3:]
    return course


db = dict()
db['UC Scouts'] = 'https://www.ucscout.org/courses/'
db['BYU Independent Study'] = 'https://is.byu.edu/catalog?school=11'
db['Apex Learning'] = 'https://www.apexlearning.com/catalog'
db['Mt. Everest Academy Independent Study'] = 'https://mteverest.sandiegounified.org/academics/advanced_coursework'
db['iUniversity Prep'] = 'https://www.iuniversityprep.org/course-descriptions'
db['UC Berkeley ATDP'] = 'https://atdp.berkeley.edu/programs/sd/catalog/'
db['Quarry Lane Summer Academy'] = 'https://www.quarrylane.org/summer/courselisting'

matches = getMatches(db,'animation speaking')
for key,value in matches.items():
    print(key+' ('+value+')')
