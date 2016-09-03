import os
import json
from collections import Counter, defaultdict

# skill -> subskill
SKILLS = {
    'java': ['play framework'],
    'cobol': [],
    'c++': [],
    '.net': ['c#', 'vb', 'asp'],

    'python': ['django'],

    'ruby': ['rails'],

    'javascript': ['angular', 'node.js', 'nodejs'],

    'databases': ['oracle', 'sql', 'postgres', 'mysql', 'DBA'],

    'cloud computing': ['AWS', 'azure'],

    'big data': ['hadoop', 'spark'],
}

# Set of all skills/subskills
ALL_SKILLS = set(sum([
    [skill]+subskills
    for skill, subskills in SKILLS.items()
], []))

def invert_skills(skills):
    skill_index = {}
    for skill, subskills in skills.items():
        for subskill in subskills:
            skill_index[subskill] = skill
    return skill_index

# So we can easily map a subskill to its parent skill
SUBSKILLS_TO_SKILLS = invert_skills(SKILLS)

##
# Word / normalization functions
##

def normalize_word(word):
    # Nornalize to lowercase
    word = word.lower()
    # Remove trailing comas or dots
    word = word.rstrip('-.,;*()/\\')
    word = word.lstrip('-,;*()/\\')
    return word

def flatten(list_of_lists):
    return sum(list_of_lists, [])

def text_to_words(paragraph):
    return [normalize_word(word) for word in paragraph.split()]

def word_to_skills(word):
    # Not a skill
    if not word in ALL_SKILLS:
        return []
    # Is a subskill
    if word in SUBSKILLS_TO_SKILLS:
        parent_skill = SUBSKILLS_TO_SKILLS[word]
        return [word, parent_skill]
    # Is a parent skill / category
    return [word]

# skills returns a list of skills and subskills that appear in a given paragraph
def skills(paragraph):
    words = text_to_words(paragraph)
    return flatten([
        word_to_skills(word)
        for word in words
    ])

##
# JSON stuff
##

JSON_FOLDER = "./json/ceviu"

def json_files():
    for filepath in os.listdir(JSON_FOLDER):
        if not filepath.endswith(".json"):
            continue
        yield "%s/%s" % (JSON_FOLDER, filepath)

def jobs():
    for file in json_files():
        yield json.loads(open(file).read())

##
# Main
##

def print_counter(counter):
    for word, freq in counter.most_common():
        print("%d %s" % (freq, word))

# "09/06/16" -> "06/16"
def job_month(job_date):
    day, month, year = job_date.split('/', 3)
    return "%s/%s" % (year, month)

def skills_histograms():
    histogram = {
        skill: defaultdict(int)
        for skill in ALL_SKILLS
    }
    for job in jobs():
        month = job_month(job['date'])
        job_skills = skills(job['job_description'])
        for skill in set(job_skills):
            histogram[skill][month] = histogram[skill][month] + 1
    return histogram

def main_java():
    histograms = skills_histograms()
    for skill, histogram in histograms.items():
        print("# %s" % skill)
        for month, count in histogram.items():
            print("%s %s" % (month, count))
        print()

def main_all_skills():
    title_skills = flatten([
        skills(job['job_description'])
        for job in jobs()
    ])
    counter = Counter(title_skills)
    print_counter(counter)

def main():
    main_java()

if __name__ == '__main__':
    main()
