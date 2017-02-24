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

import argparse
import csv
import os
import re
#from fuzzywuzzy import fuzz
from collections import Counter

class outreachyProject:
    name = ''
    description = ''
    keywords = []
    filterFunction = None

    def __init__(self, name, description, keywords, function):
        self.name = name
        self.description = description
        self.keywords = keywords
        self.filterFunction = function

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

def filterIntersection(proj, matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList
                     if project.name == proj.name and project.description == proj.description]
                    for (resume, projectList) in matches], [])
    resumes = set([resume for (resume, project) in cmatches if proj.keywords[0].lower() in project.keywords])
    for keyword in proj.keywords[1:]:
        resumes.intersection_update([resume for (resume, project) in cmatches if keyword.lower() in project.keywords])
    print(len(resumes), '\t', proj.name, '\t', proj.description)
    return resumes

def filterUnion(proj, matches, hitcount):
    cmatches = sum([[(resume, project) for project in projectList
                     if project.name == proj.name and project.description == proj.description]
                    for (resume, projectList) in matches], [])
    resumes = set()
    for keyword in proj.keywords:
        resumes.update([resume for (resume, project) in cmatches if keyword.lower() in project.keywords])
    print(len(resumes), '\t', proj.name, '\t', proj.description)
    return resumes

projectsMay2017 = [
    #outreachyProject('Outreachy',
    #                 ['open source', 'free software', 'Linux', 'Unix', 'Solaris']),
    outreachyProject('Cadasta', 'enhancing user settings and creating a user dashboard',
                     ['django'], filterUnion),
    outreachyProject('Cadasta', 'adding additional login options',
                     ['django', 'oauth'], filterUnion),
    outreachyProject('Cadasta', 'improving automated test coverage',
                     ['selenium'], filterUnion),
    outreachyProject('Ceph', 'creating a root cause analysis tool for Linux distributed systems',
                    ['Linux', 'distributed systems'], filterIntersection),
    outreachyProject('Ceph', 'evaluating the performance of new reweight algorithms for balancing storage utilization across distributed systems',
                    ['statistics', 'storage', 'linux'], filterIntersection),
    outreachyProject('Ceph', 'design a status dashboard to visualize Ceph cluster statistics',
                    ['python', 'linux', 'javascript', 'html5', 'css3'], filterIntersection),
    outreachyProject('Ceph', 'identify performance degradation in nodes and automate cluster response',
                    ['Linux', 'python', 'distributed systems'], filterIntersection),
    outreachyProject('Ceph', 'design a simplified database backend for the Ceph Object Gateway',
                    ['database', 'Linux', 'C\+\+'], filterIntersection),
    outreachyProject('Ceph', 'port tests written in multiple languages to test Amazon S3 storage protocol and Openstack Swift storage',
                    ['python', 'linux', 'storage'], filterIntersection),
    outreachyProject('Debian', 'benchmarking scientific packages for general and architecture specific builds',
                    ['linux', 'gcc'], filterIntersection),
    outreachyProject('Debian', 'improving the Debian test database and website',
                    ['linux', 'python', 'sql', 'shell'], filterIntersection),
    outreachyProject('Debian', 'enhancing the Debian test website',
                    ['html', 'css', 'linux', 'graphic'], filterIntersection),
    outreachyProject('Discourse', 'enhancing their forum and chat web services',
                    ['rails', 'javascript'], filterIntersection),
    outreachyProject('Fedora', 'creating a coloring book to explain open source concepts',
                     ['(inkscape|scribus)', '(storyboard|storyboarding)', 'graphic design'], filterUnion),
    outreachyProject('GNOME', 'improving the recipes or maps applications',
                     ['gtk'], filterUnion),
    outreachyProject('Lagome', "creating an online action sample app to showcase Lagome's microservices",
                     ['Scala'], filterIntersection),
    outreachyProject('Linux kernel', 'analyze memory resource release operators and fix Linux kernel memory bugs',
                     ['linux', 'operating systems', 'memory'], filterIntersection),
    outreachyProject('Linux kernel', 'improve process ID allocation',
                     ['linux', 'operating systems', 'kernel'], filterIntersection),
    outreachyProject('Linux kernel', 'improve nftables (an in-kernel network filtration tool)',
                     ['linux', 'operating systems', 'networking'], filterIntersection),
    outreachyProject('Mozilla', 'PROJECT TBD',
                     ['mozilla', 'firefox'], filterUnion),
    outreachyProject('oVirt', 'implement oVirt integration tests using Lago and oVirt REST API',
                     ['python', 'rest'], filterIntersection),
    outreachyProject('oVirt', 'design an oVirt log analyzer for distributed systems',
                     ['python', 'linux', 'distributed systems'], filterIntersection),
    outreachyProject('oVirt', 'rewrite oVirt UI dialogs in modern JavaScript technologies',
                     ['es6', 'react', 'redux'], filterUnion),
    outreachyProject('QEMU', 'rework the QEMU audio backend',
                     ['C(?!\+\+)', 'audio'], filterIntersection),
    outreachyProject('QEMU', 'create a full and incremental disk backup tool',
                     ['C(?!\+\+)', 'python', 'storage'], filterIntersection),
    outreachyProject('QEMU', "refactor the block layer's I/O throttling and write notifiers",
                     ['C(?!\+\+)', 'storage'], filterIntersection),
    outreachyProject('QEMU', "code an emulated PCIe-to-PCI bridge",
                     ['pci', 'pcie'], filterUnion),
    outreachyProject('QEMU', "add x86 virtualization support on macOS using Hypervisor.framework",
                     ['C(?!\+\+)', 'mac', 'virtualization'], filterIntersection),
    outreachyProject('QEMU', "extend the current vhost-pci based inter-VM communication",
                     ['C(?!\+\+)', 'pci'], filterIntersection),
    outreachyProject('Sugar Labs', 'improve Music Blocks, a collection of programming tools for exploring fundamental musical concepts in an integrative and fun way',
                     ['javascript', 'music'], filterIntersection),
    outreachyProject('Wikimedia', 'write a Zotero translator and document process',
                     ['javascript', 'documentation'], filterIntersection),
    outreachyProject('Wikimedia', 'improve and fix bugs in the quiz extension',
                     ['php', 'documentation'], filterIntersection),
    outreachyProject('Wikimedia', 'create user guides to help with translation outreach',
                     ['translation', 'localization'], filterUnion),
    outreachyProject('Wine', 'implement resource editor and dialog editor',
                     ['C(?!\+\+)', 'Windows', '(UI|UX)'], filterIntersection),
    outreachyProject('Wine', 'implement missing D3DX9 APIs',
                     ['C(?!\+\+)', 'computer graphics'], filterIntersection),
    outreachyProject('Wine', 'implement Direct3D microbenchmarks',
                     ['C(?!\+\+)', 'opengl'], filterIntersection),
    outreachyProject('Wine', 'automated game benchmarks',
                     ['C(?!\+\+)', 'game engine'], filterIntersection),
    outreachyProject('Wine', 'port WineLib to a new architecture (such as PPC64, Sparc64, RISC-V, or x32)',
                     ['PPC', 'PowerPC', 'Sparc', 'Sparc64', 'RISC-V'], filterUnion),
    outreachyProject('Wine', 'improve the AppDB website, which lists Wine support for Windows programs',
                     ['PPC', 'PowerPC', 'Sparc', 'Sparc64', 'RISC-V'], filterUnion),
    outreachyProject('Xen Project', 'create golang bindings for libxl on the Xen hypervisor',
                     ['go', 'C(?!\+\+)'], filterIntersection),
    outreachyProject('Xen Project', 'create rust bindings for libxl on the Xen hypervisor',
                     ['rust'], filterIntersection),
    outreachyProject('Xen Project', 'KDD (Windows Debugger Stub) enhancements for the Xen hypervisor',
                     ['C(?!\+\+)', 'windows', '(kernel|debugger)'], filterIntersection),
    outreachyProject('Xen Project', 'fuzz testing the Xen hypercall interface',
                     ['C(?!\+\+)', 'assembly', 'gcc'], filterIntersection),
    outreachyProject('Xen Project', 'improving Mirage OS, a unikernel that runs on top of Xen',
                     ['ocaml'], filterUnion),
    outreachyProject('Xen Project', 'create a Xen code review dashboard',
                     ['sql', 'javascript', 'html5', 'java'], filterIntersection),
    #outreachyProject('Xen Project', 'implement tools for code standards checking using clang-format',
    #                 ['clang'], filterIntersection),
    outreachyProject('Xen Project', 'add more FreeBSD testing to osstest',
                     ['freebsd', 'bsd', 'openbsd', 'netbsd', 'dragonfly'], filterUnion),
    outreachyProject('Yocto', 'PROJECT TBD',
                     ['C(?!\+\+)', 'python', '(distro|linux|yocto|openembedded)', '(embedded|robotics|beaglebone|beagle bone|minnow|minnowboard|arduino)'], filterIntersection),
]

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
                matches.append(outreachyProject(project.name, project.description, keywordmatches, None))
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
    filteredresumes = []
    for proj in projectsMay2017:
        filteredresumes.append((proj, proj.filterFunction(proj, goldresumes, hitcount)))
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
