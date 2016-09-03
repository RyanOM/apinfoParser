import io
import json
from bs4 import BeautifulSoup
import os, re, rake

JOB_PLATFORM = 'ceviu'
JSON_FOLDER = "./json/ceviu"


def jobdescriptions_to_text(limit=None):
    myfile = open('abc.txt', 'w')
    counter = 0
    for f in os.listdir(JSON_FOLDER):
        if limit and counter > limit:
            break
        if f.endswith(".json"):
            json_path = "%s/%s" % (JSON_FOLDER, f)
            json_data = open(json_path).read()
            print json_path
            data = json.loads(json_data)
            myfile.writelines("%s " % data['job_description'])
        counter += 1
    myfile.close()


def get_keywords(text):
    rake_object = rake.Rake("PortugueseStoplist.txt", 3, 2, 10)
    text = ""
    with open('abc.txt', 'r') as myfile:
        text = myfile.read().replace("/", " ")
    keywords = rake_object.run(text)

    for kw in keywords:
        print kw


def main():
    print "starting main"
    jobdescriptions_to_text()
    get_keywords('bob')

if __name__ == '__main__':
    main()
