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

def print_percentage(name, partial, total):
    print('{}: {:.0f}% ({})'.format(name, float(partial / total * 100), partial))

def race_and_ethnicity_demographics(data):
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
    print_percentage('Asian', asian_alums, total_alums)
    print_percentage('Black', black_alums, total_alums)
    print_percentage('Hispanic or Latinx', hispanic_or_latinx_alums, total_alums)
    print_percentage('Middle Eastern', middle_eastern_alums, total_alums)
    print_percentage('White', white_alums, total_alums)

def before_outreachy_statistics(data):
    # overview:
    # 'In the three months before your Outreachy internship, were you:'
    #  - "A student"
    #  - "Employed"
    #  - "Unemployed"
    #  - "Other"
    #  - "A full-time parent"
    student_applicants = 0
    employed_applicants = 0
    unemployed_applicants = 0
    other_applicants = 0
    parent_applicants = 0
    total_applicants = 0

    print()
    print("Before Outreachy")
    print("---")
    print()

    for index, row in enumerate(data):
        total_applicants += 1
        if row['In the three months before your Outreachy internship, were you:'] == 'A student':
            student_applicants += 1
        elif row['In the three months before your Outreachy internship, were you:'] == 'Employed':
            employed_applicants += 1
        elif row['In the three months before your Outreachy internship, were you:'] == 'Unemployed':
            unemployed_applicants += 1
        elif row['In the three months before your Outreachy internship, were you:'] == 'A full time parent':
            parent_applicants += 1
        elif row['In the three months before your Outreachy internship, were you:'] == 'Other':
            other_applicants += 1
            print("Other:", row['In the three months before your Outreachy internship, what was your employment or educational situation?'])

    print()
    print('Total alums: {}'.format(total_applicants))
    print_percentage('Students', student_applicants, total_applicants)
    print_percentage('Employed', employed_applicants, total_applicants)
    print_percentage('Unemployed', unemployed_applicants, total_applicants)
    print_percentage('Parents', parent_applicants, total_applicants)
    print_percentage('Other', other_applicants, total_applicants)

def retention_statistics(data):
    # overview:
    # 'Are you currently:'
    #  - "A student"
    #  - "Employed"
    #  - "Unemployed"
    #  - "Other"
    #  - "A full-time parent"
    student_alums = 0
    stem_student_alums = 0
    student_alums_who_use_foss_in_school = 0
    student_alums_who_contribute_to_foss_in_school = 0
    employed_alums = 0
    tech_employed_alums = 0
    employed_alums_who_use_foss_at_work = 0
    employed_alums_who_contribute_to_foss_at_work = 0
    unemployed_alums = 0
    other_alums = 0
    parent_alums = 0
    total_alums = 0

    print()
    print("Current Employment and Education status of alums")
    print("---")
    print()
    for index, row in enumerate(data):
        total_alums += 1
        if row['Are you currently:'] == 'A student':
            student_alums += 1
            if row['Are you a student in a science, technology, engineering, or mathematics field?'] == 'Yes':
                stem_student_alums += 1
            if row['Do you use free software / open source to complete your student projects or research?'] == 'Yes':
                student_alums_who_use_foss_in_school += 1
            if row['Do you contribute to free software / open source as part of your student projects or research?'] == 'Yes':
                student_alums_who_contribute_to_foss_in_school += 1
        elif row['Are you currently:'] == 'Employed':
            employed_alums += 1
            if row['Are you employed in the technology industry?'] == 'Yes':
                tech_employed_alums += 1
            if row['Does your job involve using free software / open source?'] == 'Yes':
                employed_alums_who_use_foss_at_work += 1
            if row['Does your job involve contributing to free software / open source?'] == 'Yes':
                employed_alums_who_contribute_to_foss_at_work += 1
        elif row['Are you currently:'] == 'Unemployed':
            unemployed_alums += 1
        elif row['Are you currently:'] == 'A full-time parent':
            parent_alums += 1
        elif row['Are you currently:'] == 'Other':
            other_alums += 1
            print("Other:", row['What is your current employment or educational situation?'])

    print()
    print('Total alums: {}'.format(total_alums))
    print_percentage('Students', student_alums, total_alums)
    print_percentage(' - STEM students', stem_student_alums, student_alums)
    print_percentage(' - Students who use FOSS for school projects or research', student_alums_who_use_foss_in_school, student_alums)
    print_percentage(' - Students who contribute to FOSS for school projects or research', student_alums_who_contribute_to_foss_in_school, student_alums)
    print_percentage('Employed', employed_alums, total_alums)
    print_percentage(' - Tech employees', tech_employed_alums, employed_alums)
    print_percentage(' - Employees who use FOSS as part of their job', employed_alums_who_use_foss_at_work, employed_alums)
    print_percentage(' - Employees who contribute to FOSS as part of their job', employed_alums_who_contribute_to_foss_at_work, employed_alums)
    print_percentage('Unemployed', unemployed_alums, total_alums)
    print_percentage('Parents', parent_alums, total_alums)

def main():
    parser = argparse.ArgumentParser(description='Print statistics from 2019 Outreachy longitudinal survey')
    parser.add_argument('--csv', help='CSV file of longitudinal survey responses')
    args = parser.parse_args()

    data = []
    with open(args.csv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=';', quotechar='"')
        for row in freader:
            data.append(row)

    race_and_ethnicity_demographics(data)
    before_outreachy_statistics(data)
    retention_statistics(data)

if __name__ == "__main__":
    main()
