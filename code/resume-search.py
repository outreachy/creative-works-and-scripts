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
    """Outreachy project name, description, keywords, and matching resume storage."""
    def __init__(self, name, description, keywords):
        self.name = name
        self.description = description
        self.keywords = keywords
        self.strongResumeMatches = []
        self.weakResumeMatches = []

class resumeFile:
    """Information relating to a text and pdf resume pair."""
    def __init__(self, path, textFileName, contents):
        self.path = path
        self.textFileName = textFileName
        self.pdfFileName = os.path.splitext(textFileName)[0] + '.pdf'
        self.contents = contents
        self.emails = re.findall(r'[\w\.-\_\+]+@[\w\.-]+', contents)
        self.strongProjectMatches = []
        self.weakProjectMatches = []

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

projectsMay2017 = [
    #outreachyProject('Outreachy',
    #                 ['open source', 'free software', 'Linux', 'Unix', 'Solaris']),
    outreachyProject('Cadasta', 'enhancing user settings and creating a user dashboard',
                     ['django']),
    outreachyProject('Cadasta', 'adding additional login options',
                     ['django|oauth']),
    outreachyProject('Cadasta', 'improving automated test coverage',
                     ['selenium']),
    outreachyProject('Ceph', 'creating a root cause analysis tool for Linux distributed systems',
                    ['Linux', 'distributed systems']),
    outreachyProject('Ceph', 'evaluating the performance of new reweight algorithms for balancing storage utilization across distributed systems',
                    ['statistics', 'storage', 'linux']),
    outreachyProject('Ceph', 'design a status dashboard to visualize Ceph cluster statistics',
                    ['python', 'linux', 'javascript', 'html5', 'css3']),
    outreachyProject('Ceph', 'identify performance degradation in nodes and automate cluster response',
                    ['Linux', 'python', 'distributed systems']),
    outreachyProject('Ceph', 'design a simplified database backend for the Ceph Object Gateway',
                    ['database', 'Linux', 'C\+\+']),
    outreachyProject('Ceph', 'port tests written in multiple languages to test Amazon S3 storage protocol and Openstack Swift storage',
                    ['python', 'linux', 'storage']),
    outreachyProject('Debian', 'benchmarking scientific packages for general and architecture specific builds',
                    ['linux', 'gcc']),
    outreachyProject('Debian', 'improving the Debian test database and website',
                    ['linux', 'python', 'sql', 'shell']),
    outreachyProject('Debian', 'enhancing the Debian test website',
                    ['html', 'css', 'linux', 'graphic']),
    outreachyProject('Discourse', 'enhancing their forum and chat web services',
                    ['rails', 'javascript']),
    outreachyProject('Fedora', 'creating a coloring book to explain technical concepts',
                     ['inkscape|scribus|storyboard|storyboarding|graphic design']),
    outreachyProject('GNOME', 'improving the recipes or maps applications',
                     ['gtk']),
    outreachyProject('Lagome', "creating an online action sample app to showcase Lagome's microservices",
                     ['Scala']),
    outreachyProject('Linux kernel', 'analyze memory resource release operators and fix Linux kernel memory bugs',
                     ['linux', 'operating systems', 'memory']),
    outreachyProject('Linux kernel', 'improve process ID allocation',
                     ['linux', 'operating systems', 'kernel']),
    outreachyProject('Linux kernel', 'improve nftables (an in-kernel network filtration tool)',
                     ['linux', 'operating systems', 'networking']),
    outreachyProject('Mozilla', 'PROJECT TBD',
                     ['mozilla|firefox']),
    outreachyProject('oVirt', 'implement oVirt integration tests using Lago and oVirt REST API',
                     ['python', 'rest']),
    outreachyProject('oVirt', 'design an oVirt log analyzer for distributed systems',
                     ['python', 'linux', 'distributed systems']),
    outreachyProject('oVirt', 'rewrite oVirt UI dialogs in modern JavaScript technologies',
                     ['es6|react|redux']),
    outreachyProject('QEMU', 'rework the QEMU audio backend',
                     ['C(?!\+\+)', 'audio']),
    outreachyProject('QEMU', 'create a full and incremental disk backup tool',
                     ['C(?!\+\+)', 'python', 'storage']),
    outreachyProject('QEMU', "refactor the block layer's I/O throttling and write notifiers",
                     ['C(?!\+\+)', 'storage']),
    outreachyProject('QEMU', "code an emulated PCIe-to-PCI bridge",
                     ['pci|pcie']),
    outreachyProject('QEMU', "add x86 virtualization support on macOS using Hypervisor.framework",
                     ['C(?!\+\+)', 'mac', 'virtualization']),
    outreachyProject('QEMU', "extend the current vhost-pci based inter-VM communication",
                     ['C(?!\+\+)', 'pci']),
    outreachyProject('Sugar Labs', 'improve Music Blocks, a collection of programming tools for exploring fundamental musical concepts in an integrative and fun way',
                     ['javascript', 'music']),
    outreachyProject('Wikimedia', 'write a Zotero translator and document process',
                     ['javascript', 'documentation']),
    outreachyProject('Wikimedia', 'improve and fix bugs in the quiz extension',
                     ['php', 'documentation']),
    outreachyProject('Wikimedia', 'create user guides to help with translation outreach',
                     ['translation|localization']),
    outreachyProject('Wine', 'implement resource editor and dialog editor',
                     ['C(?!\+\+)', 'Windows', 'UI|UX']),
    outreachyProject('Wine', 'implement missing D3DX9 APIs',
                     ['C(?!\+\+)', 'computer graphics']),
    outreachyProject('Wine', 'implement Direct3D microbenchmarks',
                     ['C(?!\+\+)', 'opengl']),
    outreachyProject('Wine', 'automated game benchmarks',
                     ['C(?!\+\+)', 'game engine']),
    outreachyProject('Wine', 'port WineLib to a new architecture (such as PPC64, Sparc64, RISC-V, or x32)',
                     ['PPC|PowerPC|Sparc|Sparc64|RISC-V']),
    outreachyProject('Wine', 'improve the AppDB website, which lists Wine support for Windows programs',
                     ['php', 'html', 'mysql']),
    outreachyProject('Xen Project', 'create golang bindings for libxl on the Xen hypervisor',
                     ['go', 'C(?!\+\+)']),
    outreachyProject('Xen Project', 'create rust bindings for libxl on the Xen hypervisor',
                     ['rust']),
    outreachyProject('Xen Project', 'KDD (Windows Debugger Stub) enhancements for the Xen hypervisor',
                     ['C(?!\+\+)', 'windows', 'kernel|debugger']),
    outreachyProject('Xen Project', 'fuzz testing the Xen hypercall interface',
                     ['C(?!\+\+)', 'assembly', 'gcc']),
    outreachyProject('Xen Project', 'improving Mirage OS, a unikernel that runs on top of Xen',
                     ['ocaml']),
    outreachyProject('Xen Project', 'create a Xen code review dashboard',
                     ['sql', 'javascript', 'html5', 'java']),
    #outreachyProject('Xen Project', 'implement tools for code standards checking using clang-format',
    #                 ['clang']),
    outreachyProject('Xen Project', 'add more FreeBSD testing to osstest',
                     ['freebsd|bsd|openbsd|netbsd|dragonfly']),
    outreachyProject('Yocto', 'PROJECT TBD',
                     ['C(?!\+\+)', 'python', 'distro|linux|yocto|openembedded', 'embedded|robotics|beaglebone|beagle bone|minnow|minnowboard|arduino']),
]

# We have two types of resumes:
# 1. They matched *some* but not all of the important keywords for a project.
# 2. They matches all of the keywords we need.
def matchResumes(resumeFiles):
    for resume in resumeFiles:
        for project in projectsMay2017:
            matches = [set(re.findall(r'\b(?:' + keyword + r')\b', resume.contents, flags=re.IGNORECASE)) for keyword in project.keywords]
            # New syntax for me!
            # * takes a list and expands it to arguments to a function.
            # ** takes a dictionary and expands it to key-value arguments to a function.
            # union combines the list of sets and removes duplicates.
            keywords = set.union(*matches)
            if all(matches):
                resume.strongProjectMatches.append((project, keywords))
                project.strongResumeMatches.append(resume)
            elif any(matches):
                resume.weakProjectMatches.append((project, keywords))
                project.weakResumeMatches.append(resume)

def matchWithProjects(resumeFiles):
    goldresumes = []
    matchResumes(resumeFiles)

    # Count what keyword caused this resume to match (not counting multiple matches)
    #hitcount = Counter()
    #for resume in resumeFiles:
    #    allkeywords = set()
    #    for project, keywords in resume.strongProjectMatches + resume.weakProjectMatches:
    #        allkeywords.update(keywords)
    #        for keyword in keywords:
    #            allkeywords.add(keyword)
    #    hitcount.update(allkeywords)

    for project in projectsMay2017:
        print(len(project.strongResumeMatches), '\t', project.name, '\t', project.description)

    print('Resumes to review:', len([resume for resume in resumeFiles if len(resume.strongProjectMatches) > 0]))

    print('Resumes with strong matches:')
    for i in range(1, 9):
        resumeCount = [resume for resume in resumeFiles if len(resume.strongProjectMatches) == i]
        if resumeCount:
            print(len(resumeCount), 'with', i, 'strong matches')

    resumeCount = [resume for resume in resumeFiles if len(resume.strongProjectMatches) > 9]
    if resumeCount:
        print(len(resumeCount), 'with > 10 matches')

    print('Resumes with weak matches:')
    for i in range(1, 9):
        resumeCount = [resume for resume in resumeFiles
                       if not resume.strongProjectMatches and len(resume.weakProjectMatches) == i]
        if resumeCount:
            print(len(resumeCount), 'with', i, 'weak matches')

    resumeCount = [resume for resume in resumeFiles
                   if not resume.strongProjectMatches and len(resume.weakProjectMatches) > 9]
    if resumeCount:
        print(len(resumeCount), 'with > 10 matches')

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
