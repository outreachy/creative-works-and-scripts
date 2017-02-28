#!/bin/bash
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
# This is a small, potentially error prone script to search for international
# resumes and put them into a separate directory.  We do a simple search for
# abbreviated state names (which would be found in addresses on resumes) and
# put any resumes that don't have those words into the directory. This fails
# for resumes that don't have an address, or for resumes which are images
# instead of text (yes, those exist).
#
# This script assumes you've run pdftotext to generate .txt files with the same
# name as the pdf filename:
# $ for i in `ls *.pdf`; do pdftotext $i; done

mkdir international-maybe; for i in `grep -wL 'AL\|AK\|AZ\|AR\|CA\|CO\|CT\|DE\|DC\|FL\|GA\|HI\|ID\|IL\|IN\|IA\|KS\|KY\|LA\|ME\|MD\|MA\|MI\|MN\|MS\|MO\|MT\|NE\|NV\|NH\|NJ\|NM\|NY\|NC\|ND\|OH\|OR\|PA\|RI\|SC\|SD\|TN\|TX\|UT\|VT\|WA\|WV\|WI\|WY\|AS\|GU\|MP\|PR\|VI\|UM\|FM\|MH\|PW' *.txt`; do mv $i international-maybe/; done; for i in `ls international-maybe/`; do mv `basename -s .txt $i`.pdf international-maybe/; done;
