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
# This program expects you to have created a directory with identically
# named PDF and text resume files. You can translate PDF files to text with:
# $ for i in `ls *.pdf`; do pdftotext $i; done

import argparse
import csv
import os
import re
#from fuzzywuzzy import fuzz
from collections import Counter

class outreachyProject:
    name = ''
    keywords = []
    optionalKeywords = []

    def __init__(self, name, keywords, optional):
        self.name = name
        self.keywords = keywords
        self.optionalKeywords = optional

projectsMay2017 = [
    outreachyProject('Outreachy', ['open source', 'free software'], ['Linux', 'Unix', 'Solaris']),
    outreachyProject('Cadasta', ['Python', 'Django', 'JavaScript', 'HTML', 'OAuth', 'Selenium'], ['front-end', 'back-end']),
    outreachyProject('Ceph', ['Python', 'storage', 'file system', 'file systems', 'distributed system', 'distributed systems'], ['C(?!\+\+)', 'C\+\+', 'Linux', 'probability', 'statistics', 'front-end', 'design', 'operating systems']),
    outreachyProject('Debian', ['Debian', 'Linux', 'Greek', 'scientific', 'linear algebra', 'optimization', 'gcc', 'localization', 'documentation', 'internationalization'], ['Python', 'Perl']),
    outreachyProject('Discourse', ['rails', 'ember.js', 'JavaScript'], ['OpenCollective', 'Slack', 'chat']),
    outreachyProject('Fedora', ['design', 'graphics', 'artist', 'Fedora', 'Linux', 'storyboard', 'storyboarding'], ['Inkscape', 'Scribus']),
    outreachyProject('GNOME', ['GTK', 'C(?!\+\+)', 'Linux'], ['Python', 'Vala', 'maps']),
    outreachyProject('Lagome', ['Java'], ['Scala', 'REST', 'reactive', 'microservice', 'microservices']),
    outreachyProject('Linux kernel', ['Linux', 'operating systems', 'C(?!\+\+)'], ['networking', 'memory']),
    outreachyProject('oVirt', ['Python', 'JavaScript', 'distributed systems', 'distributed system'], ['react', 'redux', 'ES6']),
    outreachyProject('QEMU', ['C(?!\+\+)', 'Python', 'virtualization'], ['audio', 'GStreamer', 'Linux', 'PCI', 'PCIe', 'PCI Express', 'block layer', 'hypervisor']),
    outreachyProject('Sugar Labs', ['JavaScript', 'documentation'], ['design', 'graphics', 'music', 'audio']),
    outreachyProject('Wikimedia', ['JavaScript', 'PHP', 'documentation', 'Hungarian'], ['localization', 'MediaWiki', 'wiki']),
    outreachyProject('Wine', ['C(?!\+\+)', 'Windows programming', 'Win32', 'computer graphics'], ['UI', 'Direct3D', 'OpenGL', 'DirectDraw', 'scripting', 'PPC64', 'PowerPC', 'Sparc64', 'RISC-V', 'x32', 'dll', 'PHP', 'HTML', 'MySQL']),
]

class resumeFile:
    """Information relating to a text and pdf resume pair."""
    path = ''
    textFileName = ''
    pdfFileName = ''
    contents = ''
    emails = []

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
    return resumes

def filterCephResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Ceph'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'storage' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'file system' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'file systems' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed system' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed systems' in project.keywords])
    return resumes

def filterDebianResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Debian'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'debian' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'optimization' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'gcc' in project.keywords])
    return resumes

def filterDiscourseResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Discourse'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'rails' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'ember.js' in project.keywords])
    return resumes

def filterFedoraResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Fedora'] for (resume, projectList) in matches], [])
    print('Fedora', len(cmatches))
    for k in projectsMay2017[5].keywords + projectsMay2017[5].optionalKeywords:
        print('\t', k, len([resume for (resume, project) in cmatches
                            if k.lower() in project.keywords or
                            k.lower() in project.optionalKeywords
                           ]))
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'inkscape' in project.optionalKeywords])
    resumes.update([resume for (resume, project) in cmatches if 'storyboard' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'storyboarding' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'fedora' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'artist' in project.keywords])
    print(len(resumes))
    return resumes

def filterGNOMEResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'GNOME'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'gtk' in project.keywords])
    return resumes

def filterLagomeResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'Lagome'] for (resume, projectList) in matches], [])
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'scala' in project.optionalKeywords])
    resumes.update([resume for (resume, project) in cmatches if 'reactive' in project.optionalKeywords])
    return resumes

def filteroVirtResumes(matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList if project.name == 'oVirt'] for (resume, projectList) in matches], [])
    print('oVirt', len(cmatches))
    for k in projectsMay2017[9].keywords + projectsMay2017[9].optionalKeywords:
        print('\t', k, len([resume for (resume, project) in cmatches
                            if k.lower() in project.keywords or
                            k.lower() in project.optionalKeywords
                           ]))
    resumes = set()
    resumes.update([resume for (resume, project) in cmatches if 'react' in project.optionalKeywords])
    resumes.update([resume for (resume, project) in cmatches if 'redux' in project.optionalKeywords])
    resumes.update([resume for (resume, project) in cmatches if 'es6' in project.optionalKeywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed system' in project.keywords])
    resumes.update([resume for (resume, project) in cmatches if 'distributed systems' in project.keywords])
    print(len(resumes))
    return resumes

def matchWithProjects(resumeFiles):
    goldresumes = []
    silverresumes = []
    for resume in resumeFiles:
        matches = []
        for project in projectsMay2017:
            keywordmatches = []
            for keyword in project.keywords:
                if re.search(r'\b' + keyword + r'\b', resume.contents, flags=re.IGNORECASE):
                    keywordmatches.append(keyword.lower())
            optkeywordmatches = []
            for keyword in project.optionalKeywords:
                try:
                    if re.search(keyword, resume.contents, flags=re.IGNORECASE):
                        optkeywordmatches.append(keyword.lower())
                except:
                    print('FAIL on', project.name, keyword)
            if len(keywordmatches) != 0 or len(optkeywordmatches) != 0:
                matches.append(outreachyProject(project.name, keywordmatches, optkeywordmatches))
        if len(matches) != 0:
            sorted(matches, key=lambda match: (len(match.keywords), len(match.optionalKeywords)))
            if len(matches[0].keywords) != 0:
                goldresumes.append((resume, matches))
            else:
                silverresumes.append((resume, matches))
    print('Gold', len(goldresumes), 'matched')
    print('Silver', len(silverresumes), 'matched')

    # Count what keyword caused this resume to match (not counting multiple matches)
    hitcount = Counter()
    for resume in goldresumes + silverresumes:
        allkeywords = set()
        for project in resume[1]:
            for keyword in project.keywords + project.optionalKeywords:
                allkeywords.add(keyword)
        hitcount.update(allkeywords)
    print(hitcount)
    #filterCadastaResumes(goldresumes + silverresumes, hitcount)
    #filterCephResumes(goldresumes + silverresumes, hitcount)
    #filterDebianResumes(goldresumes + silverresumes, hitcount)
    #filterDiscourseResumes(goldresumes + silverresumes, hitcount)
    #filterFedoraResumes(goldresumes + silverresumes, hitcount)
    #filterGNOMEResumes(goldresumes + silverresumes, hitcount)
    #filterLagomeResumes(goldresumes + silverresumes, hitcount)
    filteroVirtResumes(goldresumes + silverresumes, hitcount)

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
