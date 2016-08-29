import json
from bs4 import BeautifulSoup
import os, re
import rake
import io

JOB_FOLDER = "./jobs"


def main():
    for html_file_path in os.listdir(JOB_FOLDER):

        htmlfile = open(JOB_FOLDER+"/"+html_file_path)
        soup = BeautifulSoup(htmlfile.read())

        job_platform_id = re.findall(r'\d+', html_file_path)[0]

        job_info = soup.find("div", class_="info-data").text.strip()
        date = job_info.rsplit('-', 1)[1].strip()
        location = job_info.rsplit('-', 1)[0]
        city = location.rsplit('-', 1)[0].strip()
        state = location.rsplit('-', 1)[1].strip()

        job_title = soup.find("div", class_="cargo m-tb").text
        job_title = re.sub('\s+', ' ', job_title).strip()
        company = re.sub('\s+', ' ', soup.find_all('p')[3].contents[2]).strip()
        job_description = re.sub('\s+', ' ', soup.find('div', class_="texto").contents[1].text).strip()

        print(date)
        print(job_title)
        print(company)
        print(city)
        print(state)
        print(job_description)
        print("")

        data = {
            'date': date,
            'job_title': job_title,
            'company': company,
            'location_city': city,
            'location_state': state,
            'job_description': job_description,
            'job_platform': 'apinfo',
            'job_platform_id': job_platform_id
        }

        json_file_name = "apinfo-%s.json" % job_platform_id
        save_path = "./json/apinfo/%s" % json_file_name

        with io.open(save_path, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)))

        #rake_object = rake.Rake("PortugueseStopList.txt", 4, 1, 1)
        #keywords = rake_object.run(job_description)


if __name__ == '__main__':
    main()
