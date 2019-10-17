#!/usr/bin/env python3
#
# Copyright 2019 Sage Sharp <sharp@otter.technology>
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
import datetime
from tempfile import NamedTemporaryFile
import shutil

def main():
    parser = argparse.ArgumentParser(description='Parse a CSV file of longitudinal survey responses and update the participant CSV with which participants responded')
    parser.add_argument('--participantcsv', help='CSV file of alum info')
    parser.add_argument('--surveycsv', help='CSV file of longitudinal survey results')
    args = parser.parse_args()

    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

    participant_data = []
    with open(args.participantcsv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        for row in freader:
            participant_data.append(row)
    fieldnames = freader.fieldnames

    survey_data = []
    with open(args.surveycsv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=';', quotechar='"')
        for row in freader:
            survey_data.append(row)

    for response in survey_data:
        found = False
        for participant in participant_data:
            if response['Email address'].lower() == participant['Email'].lower():
                participant['Responded to 2019-10 survey?'] = 'Yes'
                found = True
                break
        if not found:
            print(response['First Name / Given Name'], response['Last Name / Family Name'], response['Email address'], response['Which Outreachy round did you participate in?'], response['Which community did you intern with?'])

    fwriter = csv.DictWriter(tempfile, delimiter=',', quotechar='"', fieldnames=fieldnames)
    fwriter.writeheader()
    for row in participant_data:
        fwriter.writerow(row)

    print('cat ', tempfile.name)

if __name__ == "__main__":
    main()
