#!/usr/bin/env python3
#
# Copyright 2020 Sage Sharp <sharp@otter.technology>
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

def main():
    parser = argparse.ArgumentParser(description='Print statistics from 2019 Outreachy longitudinal survey')
    parser.add_argument('--csv', help='CSV file of longitudinal survey responses')
    args = parser.parse_args()

    data = []
    with open(args.csv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=';', quotechar='"')
        for row in freader:
            data.append(row)

    # demographics:
    # 'What is your race and ethnicity? (Select all that apply)/Asian'
    total_alums = 0
    asian_alums = 0
    black_alums = 0
    hispanic_or_latinx_alums = 0
    indigenous_alums = 0
    middle_eastern_alums = 0
    white_alums = 0
    for index, row in enumerate(data):
        total_alums += 1
        if row['What is your race and ethnicity? (Select all that apply)/Asian'] == '1':
            asian_alums += 1
        if row['What is your race and ethnicity? (Select all that apply)/Black'] == '1':
            black_alums += 1
        if row['What is your race and ethnicity? (Select all that apply)/Hispanic or Latinx'] == '1':
            hispanic_or_latinx_alums += 1
        if row['What is your race and ethnicity? (Select all that apply)/Indigenous'] == '1':
            indigenous_alums += 1
        if row['What is your race and ethnicity? (Select all that apply)/Middle Eastern'] == '1':
            middle_eastern_alums += 1
        if row['What is your race and ethnicity? (Select all that apply)/White'] == '1':
            white_alums += 1

    print('Total alums: {}'.format(total_alums))
    print('Asian: {:.0f}% ({})'.format(float(asian_alums / total_alums *100), asian_alums))
    print('Black: {:.0f}% ({})'.format(float(black_alums / total_alums *100), black_alums))
    print('Hispanic or Latinx: {:.0f}% ({})'.format(float(hispanic_or_latinx_alums / total_alums *100), hispanic_or_latinx_alums))
    print('Indigenous: {:.0f}% ({})'.format(float(indigenous_alums / total_alums *100), indigenous_alums))
    print('Middle Eastern: {:.0f}% ({})'.format(float(middle_eastern_alums / total_alums *100), middle_eastern_alums))
    print('White: {:.0f}% ({})'.format(float(white_alums / total_alums *100), white_alums))

if __name__ == "__main__":
    main()
