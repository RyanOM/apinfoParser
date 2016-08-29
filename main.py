from bs4 import BeautifulSoup
import os, re
import rake

JOB_FOLDER = "./jobs"


def main():
    for html_file_path in os.listdir(JOB_FOLDER):

        htmlfile = open(JOB_FOLDER+"/"+html_file_path)
        soup = BeautifulSoup(htmlfile.read())

        job_info = soup.find("div", class_="info-data").text.strip()
        location = job_info.rsplit('-', 1)[0]
        date = job_info.rsplit('-', 1)[1]

        job_title = soup.find("div", class_="cargo m-tb").text
        job_title = re.sub('\s+', ' ', job_title).strip()
        company = re.sub('\s+', ' ', soup.find_all('p')[3].contents[2]).strip()
        job_description = re.sub('\s+', ' ', soup.find('div', class_="texto").contents[1].text).strip()

        print(job_title)
        print(company)
        print("Location: %s\nDate: %s" % (location, date))
        print(job_description)
        print("")

        rake_object = rake.Rake("PortugueseStopList.txt", 4, 1, 1)
        keywords = rake_object.run(job_description)
        bob = 42


if __name__ == '__main__':
    main()
