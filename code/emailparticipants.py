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
from  email.message import EmailMessage
from email.parser import Parser
import email.policy
import os
import re
import smtplib
import sys
import csv

from_address = 'organizers@outreachy.org'

standard_headers = {
    'From': from_address,
    'Bcc': from_address
}

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
            type=argparse.FileType('r', encoding='UTF-8')
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

    template = Parser(policy=email.policy.EmailPolicy(linesep='\n', cte_type='8bit')).parse(args.body)
    body = template.get_content()

    for pair in cohort_pairs:
        intern_name = pair.intern_contact.split('<', 1)[0].strip()
        filename = intern_name.replace(' ', '-') + '.txt'
        this_body = body.replace('$INTERN', intern_name)

        mailfile = os.path.join(args.outdir, filename)

        recipients = []
        if args.include_mentor:
            recipients += re.split('\s*,\s*', pair.mentor_contacts)
        if args.include_coordinator:
            recipients += re.split('\s*,\s*', pair.coordinator_contacts)
        if args.include_intern:
            recipients += (pair.intern_contact,)

        message = EmailMessage()
        for k, v in standard_headers.items():
            message[k] = v
        for k, v in template.items():
            message[k] = v
        message['To'] = recipients

        message.set_content(this_body + signature.format(organizer=args.organizer))

        with open(mailfile, 'wb') as outfile:
            outfile.write(message.as_bytes())

        if smtp:
            recipients.append(from_address) # Bcc:

            with open(mailfile, 'rb') as infile:
                msg = infile.read()

            smtp.sendmail(from_address, recipients, msg)

if __name__ == "__main__":
    main()
