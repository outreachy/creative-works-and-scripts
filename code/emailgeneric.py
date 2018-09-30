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
import os

def main():
    parser = argparse.ArgumentParser(description='Send a generic email to a list of receipents with a personal greeting')
    parser.add_argument('email', help='email text template')
    parser.add_argument('contacts', help='CSV file of people who stopped by the booth')
    parser.add_argument('outdir', help='Directory to create form emails in')
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    tosend = []
    with open(args.contacts, 'r') as contactsFile:
        for row in contactsFile:
            if not row[0] == '#':
                tosend.append(row)

    for index, contact in enumerate(tosend):
        with open(args.email, 'r') as emailFile:
            given_name = contact.split(' ')[0]
            body = emailFile.read().replace('NAME', given_name)
            with open(os.path.join(args.outdir, str(index) + '.txt'), 'w') as email:
                email.write('To: ' + contact)
                email.write(body)
    print('Wrote', len(tosend), 'resume draft emails to', args.outdir)

if __name__ == "__main__":
    main()
