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
# Create a set of generic form emails when we don't have a resume match.

import argparse
import csv
import os
from resumesearch import header1, header3, atBooth, generalInfo, moreInfo

def main():
    parser = argparse.ArgumentParser(description='Search text resume files for skillset matches.')
    parser.add_argument('outdir', help='Directory to create form emails in')
    parser.add_argument('csv', help='CSV file of people who stopped by the booth')
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)

    tosend = []
    with open(args.csv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        for row in freader:
            if not row['Tapia resume database?']:
                tosend.append('"' + row['Name'] + '" <' + row['Email'] + '>')

    for index, contact in enumerate(tosend):
        with open(os.path.join(args.outdir, str(index) + '.txt'), 'w') as email:
            email.write(header1)
            email.write('To: ' + contact + '\n')
            email.write(header3)
            email.write(atBooth + generalInfo + moreInfo)
    print('Wrote', len(tosend), 'resume draft emails to', args.outdir)

if __name__ == "__main__":
    main()
