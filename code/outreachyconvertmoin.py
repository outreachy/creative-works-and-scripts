#!/usr/bin/env python3
#
# Copyright 2016 Sarah Sharp <sharp@otter.technology>
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
# The goal is to convert the Outreachy wiki history dump into only
# the current webpages, in markdown format.
#
# The current structure:
# 1. Flat directory structure (including anchor tag links).
# 2. Each directory contains:
#   - current - one line with the current revision number
#   - revisions - numbered files containing moinmoin markup text
#   - attachments - file attachments - we should probably store these in a public git repository until we have Rackspace hosted storage
#   - cache - safely ignore?
#   - edit-log - ip addresses and what action they took - safely ignore
#
#
# Input:
#  - directory path to wiki history files
#  - directory path to new website files
#
# For each wiki directory,
#  - if there's a not a 'current' file in that directory, skip it (this skips any anchor links)
#  - read the current file contents, save in $CURREV
#  - copy $WIKIDIR/$PAGEDIR/revisions/$CURREV to $WEBSITEDIR/$PAGEDIR.moin
#  - if the attachments file isn't empty, create $WEBSITEDIR/$PAGEDIR.attachments directory, copy files over
#  - validate assumptions:
#    - print a warning if there's anything in $PAGEDIR that isn't current, revisions, attachments, cache, or edit-log
#    - print a warning if any directory in $PAGEDIR contains a directory
#
# Translate flat directory structure into actual directories - not sure if we need this??

import argparse
import os
import re
import collections
from shutil import copyfile

def createdirectories(args):
    files = os.listdir(args.wikidir)
    attachments = []
    isapage = []
    notapage = []
    for f in files:
        fdir = os.path.join(args.wikidir, f)
        if not os.path.isdir(fdir):
            continue
        attachdir = os.path.join(fdir, "attachments")
        if os.path.isdir(attachdir):
            attachments.extend([os.path.join(attachdir, x) for x in os.listdir(attachdir)])
        currevfile = os.path.join(fdir, "current")
        if not os.path.isfile(currevfile):
            if not os.path.isdir(attachdir):
                notapage.append(fdir)
            continue
        with open(currevfile, 'r') as crf:
            isapage.append(os.path.join(fdir, "revisions", crf.readline().strip('\n')))
    print('Number of pages with a current revision', len(isapage))
    print('\nNumber of attachments', len(attachments))
    print('\nNumber of directories without attachments or a current revision', len(notapage))

    # create a list of path directories by splitting the flat directory name on (2f)
    # remove the last three elements from that path (PAGENAME/revisions/CURREV)
    # create a new directory path from that list, 
    # use os.mkdirs(path) to create all directories for that file (in a try-catch block)
    for currevfile in isapage:
        # PAGENAME/revisions/CURREV
        basedir = os.path.split(os.path.dirname(os.path.dirname(currevfile)))[1]
        paths = basedir.split('(2f)')
        moin = paths[-1] + '.moin'
        paths = paths[:-1]
        paths.append(moin)
        if len(paths) > 1:
            basedir = os.path.join(args.websitedir, *(paths[:-1]))
            try:
                os.makedirs(basedir)
            except:
                pass
        else:
            basedir = args.websitedir
        try:
            copyfile(currevfile, os.path.join(basedir, moin))
        except:
            print('Missing revision!', currevfile)

    # Copy all attachments into one folder,
    # creating a list of where they were linked from
    adir = os.path.join(args.websitedir, 'attachments')
    try:
        os.mkdir(adir)
    except:
        pass
    attachmentnames = []
    with open(os.path.join(adir, 'attachment-link-map.txt'), 'w') as linkmap:
        for afile in attachments:
            # PAGENAME/attachments/a
            basedir = os.path.split(os.path.dirname(os.path.dirname(afile)))[1]
            paths = basedir.split('(2f)')
            aname = os.path.split(afile)[1]
            attachmentnames.append(aname)
            linkmap.write(aname + '\t' + os.path.join(*paths, aname) + '\n')
            try:
                copyfile(afile, os.path.join(adir, aname))
            except:
                print('Missing attachment!', afile)
    # If there is already a file with the same name, warn for now and don't overwrite.
    # In the future, we should choose a unique new name.
    # But I don't care, because my three duplicate files are all copies of each other.
    duplicates = [item for item, count in collections.Counter(attachmentnames).items() if count > 1]
    if duplicates:
        print('Warning, attachments with duplicate names!')
        print(duplicates)

# This assumes the moinmoin files have been copied into a directory structure
def copymarkdown(args):
    files = os.listdir(args.markdowndir)
    for f in files:
        tocopy = os.path.join(args.markdowndir, f)
        if not os.path.isfile(tocopy) or not f.endswith('.md'):
            print('Bad markdown file:', tocopy)
            continue
        paths = f.split('(2f)')
        mddir = os.path.join(args.websitedir, *paths[:-1])
        destination = os.path.join(mddir, paths[-1])
        if not os.path.isdir(mddir):
            print('Directory', mddir, 'for markdown file', f, 'does not exist')
        try:
            copyfile(tocopy, destination)
        except:
            print('Missing file or bad permissions to copy', tocopy, 'to', destination)

def main():
    parser = argparse.ArgumentParser(description='Convert a moinmoin database dump into markdown')
    parser.add_argument('wikidir', help='Directory with moinmoin files')
    parser.add_argument('websitedir', help='Directory to put converted files')
    parser.add_argument('--copy', help='Copy the current revision of each file from the moinmoin directory into the website directory', default=False)
    parser.add_argument('--markdowndir', help='Copy the translated markdown of each moinmoin file in MARKDOWNDIR into the right website directory', default=None)
    #parser.add_argument('matches', help='file to write potential matches to')
    args = parser.parse_args()
    print('Wiki dir:', args.wikidir)
    print('Website dir:', args.wikidir)
    if args.copy:
        createdirectories(args)
    if args.markdowndir:
        copymarkdown(args)

if __name__ == "__main__":
    main()
