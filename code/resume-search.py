#!/usr/bin/env python3
#
# Copyright 2017 Sarah Sharp <sharp@otter.technology>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This script attempts to match skillset keywords in resumes with
# Outreachy projects. The skillset keyword lists are based on the
# Outreachy project list at:
# https://wiki.gnome.org/Outreachy/2017/MayAugust
#
# This program expects you to have created a directory with identically
# named PDF and text resume files. You can translate PDF files to text with:
# $ for i in `ls *.pdf`; do pdftotext $i; done
#
#

import argparse
import csv
import os
import re
#from fuzzywuzzy import fuzz
from collections import Counter

class outreachyProject:
    name = ''
    keywords = []

    def __init__(self, name, keywords):
        self.name = name
        self.keywords = keywords

projectsMay2017 = [
    outreachyProject('Outreachy',
                     ['open source', 'free software', 'Linux', 'Unix', 'Solaris']),
    outreachyProject('Cadasta',
                     ['Python', 'Django', 'JavaScript', 'HTML', 'OAuth', 'Selenium', 'front-end', 'back-end']),
    outreachyProject('Ceph',
                     ['Python', 'storage', 'file system', 'file systems', 'distributed system', 'distributed systems', 'C(?!\+\+)', 'C\+\+', 'Linux', 'probability', 'statistics', 'front-end', 'design', 'operating systems']),
    outreachyProject('Debian',
                     ['Debian', 'Linux', 'Greek', 'scientific', 'linear algebra', 'optimization', 'gcc', 'localization', 'documentation', 'internationalization', 'Python', 'Perl']),
    outreachyProject('Discourse',
                     ['rails', 'ember.js', 'JavaScript', 'OpenCollective', 'Slack', 'chat']),
    outreachyProject('Fedora',
                     ['design', 'graphics', 'artist', 'Fedora', 'Linux', 'storyboard', 'storyboarding', 'Inkscape', 'Scribus']),
    outreachyProject('GNOME',
                     ['GTK', 'C(?!\+\+)', 'Linux', 'Python', 'Vala', 'maps']),
    outreachyProject('Lagome',
                     ['Java', 'Scala', 'REST', 'reactive', 'microservice', 'microservices']),
    outreachyProject('Linux kernel',
                     ['Linux', 'operating systems', 'C(?!\+\+)', 'networking', 'memory']),
    outreachyProject('oVirt',
                     ['Python', 'JavaScript', 'distributed systems', 'distributed system', 'react', 'redux', 'ES6']),
    outreachyProject('QEMU',
                     ['C(?!\+\+)', 'Python', 'virtualization', 'QEMU', 'audio', 'GStreamer', 'Linux', 'PCI', 'PCIe', 'PCI Express', 'block layer', 'hypervisor', 'command-line', 'shell', 'storage']),
    outreachyProject('Sugar Labs',
                     ['JavaScript', 'documentation', 'design', 'graphics', 'music', 'audio']),
    outreachyProject('Wikimedia',
                     ['JavaScript', 'PHP', 'documentation', 'Hungarian', 'localization', 'MediaWiki', 'wiki', 'wikipedia', 'vagrant']),
    outreachyProject('Wine',
                     ['C(?!\+\+)', 'Windows programming', 'Win32', 'computer graphics', 'UI', 'Direct3D', 'OpenGL', 'DirectDraw', 'scripting', 'PPC64', 'PowerPC', 'Sparc64', 'RISC-V', 'x32', 'dll', 'PHP', 'HTML', 'MySQL']),
    outreachyProject('Yocto',
                     ['C(?!\+\+)', 'python', 'embedded', 'robotics', 'distro', 'linux', 'yocto', 'openembedded', 'beaglebone', 'beagle bone', 'minnow', 'minnowboard', 'arduino']),
]

class resumeFile:
    """Information relating to a text and pdf resume pair."""
    path = ''
    textFileName = ''
    pdfFileName = ''
    contents = ''
    emails = []
    projectMatches = []

    def searchByName(fullName):
        # Search for whole string
        # Tokenize name, if in 'first last' format, search for last name
        # If not in 'first last' format, search by longest string
        # Return true if this is a match
        return ''

    def searchByEmail(email):
        # Can we do a "smart" search that looks for similar words?
        # Maybe use FuzzyWuzzy?
        return ''

    def __init__(self, path, textFileName, contents):
        self.path = path
        self.textFileName = textFileName
        self.pdfFileName = os.path.splitext(textFileName)[0] + '.pdf'
        self.contents = contents
        self.emails = re.findall(r'[\w\.-\_\+]+@[\w\.-]+', contents)

def readResumeFiles(directory):
    resumeFiles = []
    for f in [l for l in os.listdir(directory) if l.endswith('.txt')]:
        with open(os.path.join(directory, f), 'r') as resume:
            contents = resume.read()
        resumeFiles.append(resumeFile(directory, f, contents))
    #print("Found", len(resumeFiles), "resume files")
    for r in resumeFiles:
        if len(r.emails) == 0:
            continue
        line = r.pdfFileName
        for email in r.emails:
            line = line + ' ' + email
        line = line + ' ' + str(len(r.contents))
    #print(len([r for r in resumeFiles if re.search('Linux', r.contents)]), "resumes have the word name")
    return resumeFiles

def searchForEmail(csvFile, resumeFiles):
    with open(csvFile, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        for row in freader:
            # Create a list of potential matches for the email we have.
            # Search through the list of emails in each PDF.
            # Use fuzzywuzzy to do a fuzzy search in case we misread an email.
            # No difference between pure match when I tried this, and going down to 80 only added false positives
            #m = [r for r in resumeFiles if len([email for email in r.emails if fuzz.ratio(row['Email'], email) > 90]) != 0]
            m = [r for r in resumeFiles if row['Email'] in r.emails]
            if len(m) == 0:
                continue
            files = ''
            for resume in m:
                files = files + ' ' + resume.pdfFileName
                for email in resume.emails:
                    files = files + ' <' + email +'>'
            print(row['Name'] + ' <' + row['Email'] + '> matches', files, 'with',)

def filterCadastaResumes(matches, hitcount):
    # Highest hit counts seem to be:
    # C, Java, Python, HTML, C++, JavaScript, PHP
    # REST
    # UI, design,
    # MySQL
    # Linux, operating systems, networking, Unix
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Cadasta'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'django' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'selenium' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'oauth' in project.keywords])
    print('Cadasta:', len(resumes))
    return resumes

def filterCephResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Ceph'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'storage' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'file system' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'file systems' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed system' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed systems' in project.keywords])
    print('Ceph:', len(resumes))
    return resumes

def filterDebianResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Debian'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'debian' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'optimization' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'gcc' in project.keywords])
    print('Debian:', len(resumes))
    return resumes

def filterDiscourseResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Discourse'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'rails' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'ember.js' in project.keywords])
    print('Discourse:', len(resumes))
    return resumes

def filterFedoraResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Fedora'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'inkscape' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'storyboard' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'storyboarding' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'fedora' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'artist' in project.keywords])
    print('Fedora:', len(resumes))
    return resumes

def filterGNOMEResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'GNOME'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'gtk' in project.keywords])
    print('GNOME:', len(resumes))
    return resumes

def filterLagomeResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Lagome'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'scala' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'reactive' in project.keywords])
    print('Lagome:', len(resumes))
    return resumes

def filteroVirtResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'oVirt'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'react' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'redux' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'es6' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed system' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed systems' in project.keywords])
    print('oVirt:', len(resumes))
    return resumes

def filterQEMUResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'QEMU'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'virtualization' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'pci' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'pcie' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'audio' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'command-line' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'storage' in project.keywords])
    print('QEMU: ', len(resumes))
    return resumes

def filterSugarLabsResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Sugar Labs'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'music' in project.keywords])
    print('Sugar Labs:', len(resumes))
    return resumes

def filterWikimediaResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Wikimedia'] for (resume, projectList) in matches], [])
    resumes = set()
    js = [resume for (resume, project) in cmatches if 'javascript' in project.keywords]
    docs = [resume for (resume, project) in cmatches if 'documentation' in project.keywords]
    # Look for people with both JavaScript and documentation experience
    resumes.update(list(set(js) & set(docs)))
    # PHP and vagrant experience
    php = [resume for (resume, project) in cmatches if 'php' in project.keywords]
    vagrant = [resume for (resume, project) in cmatches if 'vagrant' in project.keywords]
    resumes.update(list(set(php) & set(vagrant)))
    resumes.update([resume for (resume, project) in cmatches if 'hungarian' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'mediawiki' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'wiki' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'wikipedia' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'localization' in project.keywords])
    print('Wikimedia:', len(resumes))
    return resumes

def filterYoctoResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Yocto'] for (resume, projectList) in matches], [])
    #print('Yocto', len(cmatches))
    #for k in projectsMay2017[14].keywords:
    #    print('\t', k, len([resume for (resume, project) in cmatches
    #                        if k.lower() in project.keywords
    #                       ]))
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'embedded' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distro' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'beaglebone' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'beagle bone' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'robotics' in project.keywords])
    arduino = [resume for (resume, project) in cmatches if 'arduino' in project.keywords]
    linux = [resume for (resume, project) in cmatches if 'linux' in project.keywords]
    clanguage = [resume for (resume, project) in cmatches if 'c' in project.keywords]
    pythonlanguage = [resume for (resume, project) in cmatches if 'python' in project.keywords]
    # Look for non-traditional embedded folks (people who have experienced
    # both Arduino and have experience with either C or Linux or Python).
    resumes.update(list(set(arduino) & set(linux)))
    resumes.update(list(set(arduino) & set(clanguage)))
    resumes.update(list(set(arduino) & set(pythonlanguage)))
    print('Yocto:', len(resumes))
    return resumes

def matchWithProjects(resumeFiles):
    goldresumes = []
    for resume in resumeFiles:
        matches = []
        for project in projectsMay2017:
            keywordmatches = []
            for keyword in project.keywords:
                if re.search(r'\b' + keyword + r'\b', resume.contents, flags=re.IGNORECASE):
                    keywordmatches.append(keyword.lower())
            if len(keywordmatches) != 0:
                matches.append(outreachyProject(project.name, keywordmatches))
        if len(matches) != 0:
            sorted(matches, key=lambda match: len(match.keywords))
            goldresumes.append((resume, matches))
            resume.projectMatches = matches
    print('Gold', len(goldresumes), 'matched')

    # Count what keyword caused this resume to match (not counting multiple matches)
    hitcount = Counter()
    for resume in goldresumes:
        allkeywords = set()
        for project in resume[1]:
            for keyword in project.keywords:
                allkeywords.add(keyword)
        hitcount.update(allkeywords)
    #print(hitcount)
    filteredresumes = [
        (projectsMay2017[2], filterCadastaResumes(goldresumes, hitcount)),
        (projectsMay2017[3], filterCephResumes(goldresumes, hitcount)),
        (projectsMay2017[4], filterDebianResumes(goldresumes, hitcount)),
        (projectsMay2017[5], filterDiscourseResumes(goldresumes, hitcount)),
        (projectsMay2017[6], filterFedoraResumes(goldresumes, hitcount)),
        (projectsMay2017[7], filterGNOMEResumes(goldresumes, hitcount)),
        (projectsMay2017[9], filterLagomeResumes(goldresumes, hitcount)),
        (projectsMay2017[10], filteroVirtResumes(goldresumes, hitcount)),
        (projectsMay2017[11], filterQEMUResumes(goldresumes, hitcount)),
        (projectsMay2017[12], filterSugarLabsResumes(goldresumes, hitcount)),
        (projectsMay2017[13], filterWikimediaResumes(goldresumes, hitcount)),
        (projectsMay2017[14], filterYoctoResumes(goldresumes, hitcount)),
    ]
    totalmatched = 0
    resumeset = set()
    for i in filteredresumes:
        totalmatched = totalmatched + len(i[1])
        resumeset.update(i[1])
    print('Resumes to review:', len(resumeset))

def main():
    parser = argparse.ArgumentParser(description='Search text resume files for skillset matches.')
    #parser.add_argument('csv', help='CSV file with name,email,org,position')
    parser.add_argument('dir', help='Directory with .txt resume files')
    #parser.add_argument('matches', help='file to write potential matches to')
    args = parser.parse_args()
    resumeFiles = readResumeFiles(args.dir)
    #searchForEmail(args.csv, resumeFiles)
    matchWithProjects(resumeFiles)

if __name__ == "__main__":
    main()
