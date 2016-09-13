#!/usr/bin/python3
# Copyright © 2016 Sarah Sharp <sarah@thesharps.us>
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

# input file is from the Outreachy wiki, in the form
# || Org || Status || email <email@example.com> || person's title || Possible sponsors || Confirmed sponsors || Notes ||

email = '''
From: Sarah Sharp <saharabeara@gmail.com>
To: {contact}
Cc: outreachy-admins@gnome.org
Subject: {project} participation in Outreachy?

Hi {names},

The Outreachy program is looking for organizations to participate in
round 13.  Do you think {project} would be willing to participate again?
The round will open on September 12, and the sooner {project} is listed,
the more likely you'll get strong applicants.

Sarah Sharp

On Sat, Aug 27, 2016 at 4:41 PM, Sarah A Sharp <sarah@thesharps.us> wrote:
> Dear coordinators and mentors,
>
> Thank you for being a part of our outreach program! The next round for
> Outreachy is scheduled to open on September 12, with an application deadline
> of October 17. Internships will run from December 6 to March 6.
>
> If your organization is interested in participating in the next round,
> please update your landing page, and let us know by September 7 if you will
> participate. Organization coordinators and mentors, please coordinate on the
> following:
>  
>  * Review set up information at
> https://wiki.gnome.org/Outreachy/Admin/GettingStarted
>  * Secure funding for your org to sponsor at least one intern ($6,500)
>  * Update your org's landing page
>  * List your project ideas and recruit other mentors
>  * Let us know at outreachy-admins@gnome.org that your org is participating
>  * Start spreading the word about your org's internships - no need to wait
> for September 12
>
> We plan on having a twitter chat about Outreachy on Wednesday, September 21,
> to spotlight the organizations that are participating, and allow orgs to
> answer any questions people have. Participation in the chat is optional, but
> if you do want to participate, being able to link to a blog post that
> describes why you're passionate about your project would help us promote
> your project.
>
> The updated resources for the upcoming round are:
>  
>  * https://wiki.gnome.org/Outreachy/2016/DecemberMarch - a page with a
> timeline and participating organizations listing.
>
>  * https://wiki.gnome.org/Outreachy/Admin/InfoForOrgs and
> https://wiki.gnome.org/Outreachy/Admin/InfoForOrgs/Proposal - these pages
> have motivation and information for sponsorship; you can use and customize
> the text from the Proposal page to approach companies about sponsorship
> (please do a quick check with Karen, Marina, and myself at
> outreachy-admins@gnome.org alias first to make sure we coordinate any
> efforts to approach the same company).
>
>  * https://wiki.gnome.org/Outreachy/Admin/GettingStarted - please review
> this page when you are updating the landing page for your organization.
>
>  * https://wiki.gnome.org/Outreachy#Contracts - please make all people who
> volunteer as mentors in your organization aware that they will need to sign
> a contract similar to this to be a mentor in the program. Interns cannot be
> paid until their mentors sign the contract, so it is important that mentors
> sign the contract as soon as the application system opens on September 12.
>  
>  * https://wiki.gnome.org/Outreachy#Eligibility - last year we expanded the
> Outreachy program to include underrepresented people of color
> underrepresented in tech in the U.S.  Outreachy continues to be open
> internationally to women (cis and trans), trans men, and genderqueer people.
>  
> Please contact Karen, Marina, and myself at outreachy-admins@gnome.org alias
> if you have any questions. We hope you can join us for this round!
>  
> Thanks,
> Sarah Sharp
>
'''.strip()

with open('to-ping.csv', 'r') as contactsFile:
    for line in contactsFile:
        fields = line.split("||")
        project = fields[1].strip()
        contacts = fields[3].strip()
        # Assumes email addresses are of the form "First Last <email>, First Last <email>"
        names = " and ".join([(fullName.strip().split(" ")[0]) for fullName in contacts.split(", ")])
        with open("ping/ping-" + project + ".txt", 'w') as draft:
            draft.write(email.format(project = project, contact = contacts, names = names))
