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

import argparse
import csv
import os

header1 = '''From: Sage Sharp <applicant-help@outreachy.org>
'''
header3 = '''Subject: Outreachy - remote, paid internships

'''

body = '''I'm Sage Sharp, and we met when you stopped by the Outreachy booth at the Tapia conference last September. I'd like to invite you to apply for Outreachy internships. If this opportunity isn't right for you, please pass it along to a friend or other students.

https://www.outreachy.org/apply/

Outreachy internships are fully remote. You'll be working with a remote mentor from a free and open source sofware community. Projects may include programming, user experience, documentation, illustration, graphical design, or data science.

You'll be paid a $5,500 USD stipend for three months of work. You'll also have a $500 USD travel stipend to attend conferences or events.

Outreachy internships run from May 20 to August 20. Our application period is open now through April 2. Applicants need to make a contribution to a project to be eligible for the internship. It typically takes 1-2 weeks to make a contribution, so apply early!

Outreachy internships are open to applicants around the world who meet our eligibility rules:

https://www.outreachy.org/apply/eligibility/

Outreachy expressly invites women (both cis and trans), trans men, and genderqueer people to apply. We also expressly invite applications from residents and nationals of the United States of any gender who are Black/African American, Hispanic/Latin@, Native American/American Indian, Alaska Native, Native Hawaiian, or Pacific Islander. Anyone who faces under-representation, systemic bias, or discrimination in the technology industry of their country is invited to apply.

The current list of Outreachy internship projects is available at:

https://www.outreachy.org/apply/project-selection/

New Outreachy projects will be added until March 12.

Please reply to this email with your questions. I hope you'll apply!

Sage Sharp
Outreachy Organizer
'''

promote_body = '''I'm Sage Sharp, and we met when you stopped by the Outreachy booth at the Tapia conference last September. You said you would be willing to help us spread the word about Outreachy internships to students at your university. Applications for the May to August Outreachy internships are now open!

https://www.outreachy.org/apply/

Outreachy internships are fully remote. Outreachy interns works with a remote mentor from a free and open source sofware community. Projects may include programming, user experience, documentation, illustration, graphical design, or data science.

Outreachy interns are paid a $5,500 USD stipend for three months of work. Interns also have a $500 USD travel stipend to attend conferences or events.

Outreachy internships run from May 20 to August 20. Our application period is open now through April 2. Applicants need to make a contribution to a project to be eligible for the internship. It typically takes 1-2 weeks to make a contribution, so we encourage people to apply early!

Outreachy internships are open to applicants around the world who meet our eligibility rules:

https://www.outreachy.org/apply/eligibility/

Outreachy expressly invites women (both cis and trans), trans men, and genderqueer people to apply. We also expressly invite applications from residents and nationals of the United States of any gender who are Black/African American, Hispanic/Latin@, Native American/American Indian, Alaska Native, Native Hawaiian, or Pacific Islander. Anyone who faces under-representation, systemic bias, or discrimination in the technology industry of their country is invited to apply.

The current list of Outreachy internship projects is available at:

https://www.outreachy.org/apply/project-selection/

New Outreachy projects will be added until March 12.

Thanks for your help passing this opportunity along!

Sage Sharp
Outreachy Organizer
'''

def write_email(outdir, index, contact, body):
    with open(os.path.join(outdir, str(index) + '.txt'), 'w') as email:
        email.write(header1)
        email.write('To: ' + contact + '\n')
        email.write(header3)
        email.write(body)

def main():
    parser = argparse.ArgumentParser(description='Send an email to people who stopped by the Outreachy booth at Tapia')
    parser.add_argument('outdir', help='Directory to create form emails in')
    parser.add_argument('csv', help='CSV file of people who stopped by the booth')
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)

    applicants = []
    promoter = []
    with open(args.csv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=';', quotechar='"')
        for row in freader:
            # Only send email to people interested in the May to August round
            if row['Email'] and row['Which Outreachy round do you want to apply for?,May 2019 to August 2019'] == '1':
                applicants.append('"' + row['Name'].strip() + '" <' + row['Email'].strip() + '>')
            elif row['Email'] and row["Do you want to help promote Outreachy to students at your university?"] == '1':
                promotor.append('"' + row['Name'].strip() + '" <' + row['Email'].strip() + '>')

    for index, contact in enumerate(applicants):
        write_email(args.outdir, index, contact, body)
    for index, contact in enumerate(promoter):
        write_email(args.outdir, index, contact, promote_body)

    print('Wrote', len(applicants + promoter), 'resume draft emails to', args.outdir)

if __name__ == "__main__":
    main()
