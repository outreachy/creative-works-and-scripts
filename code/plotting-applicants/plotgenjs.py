#!/usr/bin/env python3
#
# Copyright 2017 Sage Sharp <sharp@otter.technology>
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
#
# This script uses plotly to generate a world heat map (choropleth)
# of the number of Outreachy applicants.
#
# Resources:
# https://plot.ly/python/choropleth-maps/#world-choropleth-map
# https://plot.ly/python/reference/#choropleth
# https://docs.python.org/3/library/csv.html

import os
import re
import argparse
import csv
from plotly.offline import offline
from plotly.graph_objs import *

def main():
    parser = argparse.ArgumentParser(description='Create html that uses plotly to display a world heat graph of applicants')
    parser.add_argument('applicants', help='csv of applicant data with headings Number of Applicants,Country,Code')
    parser.add_argument('countries', help='csv of all countries to passively outline with headings Number of Applicants,Country,Code')
    parser.add_argument('--output', help='html file to output to', type=str, default='output.html')
    # Note that plotly needs the three-letter country abbreviation to use as location
    # see https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv
    args = parser.parse_args()

    z = []
    text = []
    locations = []
    with open(args.applicants) as csvfile:
        creader = csv.DictReader(csvfile, delimiter=',')
        for row in creader:
            z.append(row['Number of Applicants'])
            text.append(row['Country'])
            locations.append(row['Code'])

    all_text = []
    all_locations = []
    with open(args.countries) as csvfile:
        creader = csv.DictReader(csvfile, delimiter=',')
        for row in creader:
            if row['Code'] not in locations:
                all_text.append(row['Country'])
                all_locations.append(row['Code'])
    all_zeros = ['0']*len(all_locations)

    data = [
        dict(
	    type = 'choropleth',
	    locations = all_locations,
	    z = all_zeros,
	    text = all_text,
	    marker = dict(
		line = dict (
		    color = 'rgb(180,180,180)',
		    width = 0.5
		)
            ),
            hoverinfo = 'none',
	    colorscale = [[0,"rgb(255, 255, 255)"],[1,"rgb(255, 255, 255)"]],
	    autocolorscale = False,
            showlegend = False,
	    showscale = False,
        ),
        dict(
	    type = 'choropleth',
	    locations = locations,
	    z = z,
	    text = text,
	    colorscale = [[0,"rgb(177, 230, 241)"],[1,"rgb(17, 95, 110)"]],
	    autocolorscale = False,
	    zmin = 1,
	    marker = dict(
		line = dict (
		    color = 'rgb(180,180,180)',
		    width = 0.5
		)
            ),
            hoverinfo = 'text+z',
            name = '',
	    colorbar = dict(
		autotick = False,
		title = 'Number of Applicants'),
        ),
    ]

    layout = dict(
        title = 'Outreachy Applicants By Country<BR>December to March 2017 round',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    print(offline.plot(fig, show_link=False, validate=False, filename=args.output))

if __name__ == "__main__":
    main()
