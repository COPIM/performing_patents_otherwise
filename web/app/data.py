# @name: data.py
# @creation_date: 2022-09-14
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: data route for data
# @acknowledgements:
#

from flask import Blueprint, render_template, request
import random
import pycountry
from . import solr

data = Blueprint('data', __name__)

# route for main data page
@data.route('/data/')
def main_data():
    core = 'all'
    total_number = solr.get_total_number(core)
    year_data = solr.get_term_data('year', core)
    country_data = solr.get_term_data('country', core)

    # parse all the year data
    year_labels = []
    year_numbers = []
    year_dataset = []
    for i in range(0, len(year_data)):
        if i % 2:
            year_numbers.append(year_data[i])
            random_colour = "#" + "%06x" % random.randint(0, 0xFFFFFF)
            year_dict = {"label": "number of records", "data": year_numbers, "backgroundColor": random_colour}
        else:
            year_labels.append(year_data[i])
    year_dataset.append(year_dict)

    # parse all the country data
    country_labels = []
    country_numbers = []
    country_dataset = []
    for i in range(0, len(country_data)):
        if i % 2:
            country_numbers.append(country_data[i])
            random_colour = "#" + "%06x" % random.randint(0, 0xFFFFFF)
            country_dict = {"label": "number of records", "data": country_numbers, "backgroundColor": random_colour}
        else:
            country = pycountry.countries.get(alpha_2=country_data[i])
            if country is None:
                country = pycountry.historic_countries.get(alpha_2=country_data[i])
            country_labels.append(country.name)
    country_dataset.append(country_dict)

    germany = pycountry.countries.get(alpha_2='DE')

    return render_template('data.html', total_number=total_number, year_data=year_data, year_labels=year_labels, year_dataset=year_dataset, country_data=country_data, country_labels=country_labels, country_dataset=country_dataset, germany=germany)
