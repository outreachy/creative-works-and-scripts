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

header1 = '''From: Outreachy Organizers <organizers@outreachy.org>
'''
header3 = '''Subject: Outreachy needs your help!

'''

body = '''Hi NAME,

According to our records, you participated in the PROGRAM internships with COMMUNITY from START to END. Now we need your help!

Outreachy is conducting our first longitudinal survey. If you fill out the survey, we'll mail you a thank you card and an Outreachy sticker. The survey should take about 20 minutes to complete. Please complete the survey by DUEDATE:

URL


Why run a longitudinal survey?
---

The TLDR is the survey data and comments will be very helpful to understand how we need to change Outreachy, and to convince sponsors that Outreachy is worth funding.

Outreachy has been running for over 10 years! Our internship program started in 2006 as the GNOME Women's Summer Outreach Program. In 2010, the program was restarted under the name the GNOME Outreach Program for Women. In 2013, more free software communities joined as mentoring organizations, and the name changed again to the Outreach Program for Women (OPW). In 2015, we began inviting more marginalized groups to apply for our internships, and we changed our name to Outreachy.

TOTAL people have been interns! 🤯

We often get asked by sponsors about what happens to Outreachy alums after they finish their internship. We're conducting a longitudinal survey to gather data about who are alums are, and what they're currently doing. We also hope to gather some quotes about the impact the internship had on you.


How will we use the data?
---

The raw survey data will be reviewed by the five Outreachy organizers: Sage Sharp, Karen Sandler, Tony Sebro, Cindy Pallares-Quezada, and Marina Zhurakhinskaya. We'll use the information to identify marginalized communities Outreachy could better support. We'll review data and comments to identify issues in the current program structure. Then we'll make changes to how the Outreachy program works. We'll use future longitudinal surveys to measure the impact of those changes.

We will also use aggregate statistics in sponsorship materials and on the Outreachy website. We won't publish individually identifiable information. We'll ensure that someone can't identify you from the aggregate statistics we publish.

We would like to share your experiences with Outreachy and your success stories! If you provide us with comments, we'll get your permission via email before we post the comments publicly on the website or use the quotes in any sponsor materials. We'll provide you with options, should you want to anonymize your quote. You can choose to include or not include several pieces of information: your picture, your name, community you interned with, and your internship round.

We want to make sure you're comfortable providing feedback! You can note in your comment if this is private feedback only meant for the Outreachy organizers.


Survey Rewards
---

At the end of the longitudinal survey, we'll ask for your mailing address. We'll use that to send you a thank you card with an Outreachy sticker!

Please fill out the survey by DUEDATE in order to receive your sticker. We'll be having volunteers stuff envelopes in Portland, OR, USA on STUFFINGDATE to ENDSTUFFINGTIME. If you want to help out, let us know by replying to this email.

If you don't want a thank you card or sticker, then leave the address field at the end of the survey blank.


Keeping in contact
---

If you want to opt-out from future longitudinal surveys, or you want us to not contact you at all, please reply to this email to let us know.

If your name or email address has changed since your internship, please reply to this email and we'll fix it.

Outreachy now has a private chat server and an opportunities mailing list. Alums, current interns, mentors, and coordinators are welcome to join them. The survey asks whether you want to join either the chat server or the mailing list.


We hope you'll fill out the Outreachy longitudinal survey:

URL

Outreachy Organizers
'''

def main():
    parser = argparse.ArgumentParser(description='Send an email to Outreachy alums to ask them to participate in the longitudinal survey')
    parser.add_argument('--outdir', help='Directory to create form emails in')
    parser.add_argument('--csv', help='CSV file of alum info')
    parser.add_argument('--survey', help='URL for the longitudinal survey')
    parser.add_argument('--duedate', help='Due date for the survey', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date())
    parser.add_argument('--stuffingdate', help='Date for volunteers to stuff survey reward envelopes', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d-%H:%M'))
    parser.add_argument('--endstuffingdate', help='End time for party for volunteers to stuff survey reward envelopes', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d-%H:%M'))
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)

    data = []
    with open(args.csv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        for row in freader:
            data.append(row)

    total_interns = len(data)

    for index, row in enumerate(data):
        with open(os.path.join(args.outdir, str(index) + '.txt'), 'w') as email:
            email.write(header1)
            email.write('To: "' + row['Public Name'] + '" <' + row['Email'] + '>\n')
            email.write(header3)
            thisbody = body.replace('DUEDATE', args.duedate.strftime('%B %d'))
            thisbody = thisbody.replace('STUFFINGDATE', args.stuffingdate.strftime('%B %d from %H:%M'))
            thisbody = thisbody.replace('ENDSTUFFINGTIME', args.endstuffingdate.strftime('%H:%M'))
            thisbody = thisbody.replace('URL', args.survey)
            thisbody = thisbody.replace('TOTAL', str(total_interns))
            thisbody = thisbody.replace('PROGRAM', row['Program Name'])
            thisbody = thisbody.replace('COMMUNITY', row['Community'])
            thisbody = thisbody.replace('START', row['Round Start Date'])
            thisbody = thisbody.replace('END', row['Round End Date'])
            thisbody = thisbody.replace('NAME', row['Public Name'].split(' ')[0])
            email.write(thisbody)

    print('Wrote', total_interns, 'resume draft emails to', args.outdir)

if __name__ == "__main__":
    main()
