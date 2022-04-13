#!/usr/bin/env python3
#
# Copyright 2022 Sage Sharp <sage@sfconservancy.org>
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

def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Create files to send mass (semi-personalized) emails with mutt.',
            epilog='''
This script will replace the string "Hi NAME," in the message body
with the first name of the recipient, or "Greetings," if there is no name.

You can send these emails by changing to the directory with the email files,
and running this command:

$ for i in `ls .`; do mutt -F ~/.muttrc-outreachy -H $i; rm $i; done

If you want to test what the command would do, you can run:

$ for i in `ls .`; do echo mutt -F ~/.muttrc-outreachy -H $i; echo rm $i; done
''',
            )
    parser.add_argument('outdir', help='Directory to create form emails in')
    parser.add_argument('csv', help='CSV file of people to email')
    parser.add_argument('fromemail', help='Name and email address to use in the From header')
    parser.add_argument('subject', help='Subject line of email')
    parser.add_argument('messagefile', help='File containing the message body of email')
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)

    body = ''
    with open(args.messagefile, 'r') as messageFile:
        body = messageFile.read()

    count = 0
    with open(args.csv, 'r') as csvFile:
        freader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        for row in freader:
            with open(os.path.join(args.outdir, str(count) + '.txt'), 'w') as email:
                email.write('From: ' + args.fromemail + '\n')
                email.write('To: ' + '"' + row['Name'] + '" <' + row['Email'] + '>' + '\n')
                email.write('Subject: ' + args.subject + '\n')
                email.write('\n')
                if row['Name']:
                    email.write(body.replace('Hi NAME,', 'Hi ' + row['Name'].split(' ')[0] + ','))
                else:
                    email.write(body.replace('Hi NAME,', 'Greetings,'))
                count += 1

    print('Wrote ', count + 1, ' draft emails to ', args.outdir)

if __name__ == "__main__":
    main()
