#!/usr/bin/python3
# Copyright (c) 2017 Sage Sharp <sharp@otter.technology>
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
import os
import re
import smtplib
import sys
import csv

from_address = 'organizers@outreachy.org'
header1 = '''From: Outreachy Organizers <{}>
'''.format(from_address)

signature = '''
{organizer}
Outreachy organizer
'''

class CohortPair:
    def __init__(self, community, coordinator_contacts, intern_contact, mentor_contacts):
        self.community = community
        self.coordinator_contacts = coordinator_contacts
        self.intern_contact = intern_contact
        self.mentor_contacts = mentor_contacts

    def __str__(self):
        return 'Community: ' + self.community + '\n' + \
                'Coordinator(s): ' + self.coordinator_contacts + '\n' + \
                'Intern: ' + self.intern_contact + '\n' + \
                'Mentor(s): ' + self.mentor_contacts

def main():
    parser = argparse.ArgumentParser(description='Generate several text-based emails to a mentor about their intern')
    parser.add_argument('outdir', help='Directory to create draft emails in')
    parser.add_argument('body', help='File containing the text-based body of the email', type=argparse.FileType('r'))
    parser.add_argument('--organizer', help='Organizer sending this email', required=True)
    parser.add_argument('--smtp-server', help='SMTP server to send mail via')
    parser.add_argument('--smtp-port', help='Port to use on SMTP server (default is 25 for non-ssl, 465 for SSL)', default=0, type=int)
    parser.add_argument('--smtp-ssl', help='Connect to the SMTP server via SSL',
                        default=False, action='store_true')
    parser.add_argument('--smtp-login', help='Login to the SMTP server. ' +
                        'SMTP USER and SMTP PASSWORD must be set in the environment',
                        default=False, action='store_true')
    parser.add_argument('--include-coordinator', help='Include coordinator on the email?',
                        default=False, action='store_true')
    parser.add_argument('--include-mentor', help='Include mentor(s) on the email?',
                        default=False, action='store_true')
    parser.add_argument('--include-intern', help='Include coordinator on the email?',
                        default=False, action='store_true')
    parser.add_argument('contacts',
            help='File of the form:\n' + \
            '# COMMUNITY\n' + \
            'Coordinators:\n' + \
            '  coordinator1 <email@example.com>, coordinator2 <email@example.com>\n' + \
            'Unpaired mentors:\n' + \
            '  mentor1 <email@example.com>,\n' + \
            'Mentor-intern pairs:\n' + \
            '  intern1 <email@example.com>, mentor2 <email@example.com>, mentor3 <email@example.com>' + \
            '  intern2 <email@example.com>, mentor4 <email@example.com>',
            type=argparse.FileType('r')
            )
    args = parser.parse_args()

    if not (args.include_mentor or args.include_intern or args.include_mentor):
        print('One or more of --include-mentor, --include-intern, or --include-mentor\nmust be specified', file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    community = ''
    coordinator = ''
    # list of CohortPairs
    cohort_pairs = []
    while True:
        line = args.contacts.readline()
        community = line.split(' ')[1].strip()
        line = args.contacts.readline()
        line = args.contacts.readline()
        coordinators = line.strip()
        line = args.contacts.readline()
        # Ignore any unpaired mentors
        if line.startswith('Unpaired mentors:'):
            while True:
                line = args.contacts.readline()
                if line.startswith('Mentor') or line.startswith('#'):
                    break
        if line.startswith('#'):
            continue
        if line == '':
            break
        # Parse intern-mentor pairings
        while True:
            line = args.contacts.readline()
            if line == '' or line == '\n':
                break
            # assuming no commas in the names - switch to tabs or | later
            pair_list = line.split(',', 1)
            if len(pair_list) < 2:
                mentor = ''
            else:
                mentor = pair_list[1].strip()
            cohort_pairs.append(CohortPair(
                community,
                coordinators,
                pair_list[0].strip(),
                mentor
                ))
        if line == '':
            break

    if args.smtp_server:
        if args.smtp_ssl:
            port = args.smtp_port if args.smtp_port else 465
            smtp = smtplib.SMTP_SSL(args.smtp_server, port=port)
        else:
            port = args.smtp_port if args.smtp_port else 25
            smtp = smtplib.SMTP(args.smtp_server, port=port)

        if args.smtp_login:
            try:
                user = os.environ['SMTP_USER']
                password = os.environ['SMTP_PASSWORD']
            except KeyError:
                print('SMTP_USER and SMTP_PASSWORD must be set in the environment when --smtp-login is specified', file=sys.stderr)
                sys.exit(1)

            smtp.login(user, password)
    else:
         smtp = None

    body = args.body.read()
    for pair in cohort_pairs:
        intern_name = pair.intern_contact.split('<', 1)[0].strip()
        filename = intern_name.replace(' ', '-') + '.txt'
        this_body = body.replace('$INTERN', intern_name)
        mailfile = os.path.join(args.outdir, filename)

        to_lines = []
        if args.include_mentor:
            to_lines.append(pair.mentor_contacts)
        if args.include_coordinator:
            to_lines.append(pair.coordinator_contacts)
        if args.include_intern:
            to_lines.append(pair.intern_contact)

        to_line = ',\n\t'.join(to_lines)

        with open(mailfile, 'w') as outfile:
            outfile.write(header1)
            outfile.write('To: ' + to_line + '\n')
            outfile.write(this_body)
            outfile.write(signature.format(organizer=args.organizer))

        if smtp:
            to_addresses = re.split(r'\s*,\s*', to_line)

            with open(mailfile, 'r') as infile:
                msg = infile.read()

            smtp.sendmail(from_address, to_addresses, msg)

if __name__ == "__main__":
    main()
