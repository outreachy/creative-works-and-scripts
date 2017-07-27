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
# This script modified markdown from converted moinmoin.
# This fixes the moinmoin that was converted to markdown to point to
# files in a directory structure, rather than the flat moin structure.

import argparse
import os
import re

def main():
    parser = argparse.ArgumentParser(description='Fix flat links to directory structures in moinmoin to markdown converted files.')
    parser.add_argument('file', type=argparse.FileType('r+'), nargs='+', help='one or more files to convert')
    args = parser.parse_args()
    for f in args.file:
        print("Fixing file", f.name)
        contents = re.sub(r'\(2f\)', '/', f.read())
        # Note that if you're using Jekyll, you'll need the jekyll-relative-links gem
        # so that the relative markdown file links show up correctly.
        # FYI - this regex also handles anchors in relative links
        contents = re.sub(r'\(\.\/Outreach(.*)\.html([\)#])', r'(./Outreach\1.md\2', contents)
        # Fix all links to Outreachy.md => index.md (or relative, depending on the page)
        f.seek(0)
        f.write(contents)
        f.truncate()

if __name__ == "__main__":
    main()
