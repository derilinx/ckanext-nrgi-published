from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

from webhelpers.html import literal

from ckan.common import request

import os
import json

from natsort import natsorted

qchoices = {}

with open(os.path.dirname(os.path.realpath(__file__)) + '/schema.json') as jsonfile:    
    schema = json.load(jsonfile)
    for field in schema['dataset_fields']:
        if field['field_name'] == 'question':
            for item in field['choices']:
                qchoices[item['value']] = item['label']
            break

ccolors = {u'Canada': 'rgba(0,0,177,1.0)', u'Libyan Arab Jamahiriya': 'rgba(0,196,0,1.0)', u'Sao Tome and Principe': 'rgba(255,57,0,1.0)', u'Venezuela, Bolivarian Republic of': 'rgba(204,28,28,1.0)', u'Guinea-Bissau': 'rgba(0,170,171,1.0)', u'Montenegro': 'rgba(0,252,0,1.0)', u'Lithuania': 'rgba(0,210,0,1.0)', u'Cambodia': 'rgba(0,172,0,1.0)', u'Saint Kitts and Nevis': 'rgba(0,178,0,1.0)', u'Ethiopia': 'rgba(0,141,221,1.0)', u'Aruba': 'rgba(0,0,0,1.0)', u'Swaziland': 'rgba(254,0,0,1.0)', u'Argentina': 'rgba(84,0,96,1.0)', u'Cameroon': 'rgba(0,0,201,1.0)', u'Burkina Faso': 'rgba(130,0,147,1.0)', u'Turkmenistan': 'rgba(230,0,0,1.0)', u'Ghana': 'rgba(0,163,191,1.0)', u'Saudi Arabia': 'rgba(255,181,0,1.0)', u'Rwanda': 'rgba(255,185,0,1.0)', u'Togo': 'rgba(241,0,0,1.0)', u'Japan': 'rgba(0,162,0,1.0)', u'American Samoa': 'rgba(103,0,117,1.0)', u'United States Minor Outlying Islands': 'rgba(210,0,0,1.0)', u'Cocos (Keeling) Islands': 'rgba(0,0,181,1.0)', u'Pitcairn': 'rgba(240,234,0,1.0)', u'Guatemala': 'rgba(0,170,157,1.0)', u'Bosnia and Herzegovina': 'rgba(120,0,155,1.0)', u'Kuwait': 'rgba(0,183,0,1.0)', u'Russian Federation': 'rgba(255,189,0,1.0)', u'Jordan': 'rgba(0,159,0,1.0)', u'Virgin Islands, British': 'rgba(204,44,44,1.0)', u'Dominica': 'rgba(0,103,221,1.0)', u'Liberia': 'rgba(0,194,0,1.0)', u'Maldives': 'rgba(0,234,0,1.0)', u'Micronesia, Federated States of': 'rgba(0,156,211,1.0)', u'Jamaica': 'rgba(0,154,0,1.0)', u'Oman': 'rgba(228,241,0,1.0)', u'Martinique': 'rgba(88,255,0,1.0)', u'Christmas Island': 'rgba(0,47,221,1.0)', u'Gabon': 'rgba(0,158,207,1.0)', u'Niue': 'rgba(204,249,0,1.0)', u'Monaco': 'rgba(0,226,0,1.0)', u'Wallis and Futuna': 'rgba(204,108,108,1.0)', u'New Zealand': 'rgba(224,243,0,1.0)', u'Saint Helena, Ascension and Tristan da Cunha': 'rgba(255,161,0,1.0)', u'Jersey': 'rgba(0,156,0,1.0)', u'Bahamas': 'rgba(131,0,154,1.0)', u'Yemen': 'rgba(204,140,140,1.0)', u'Albania': 'rgba(47,0,53,1.0)', u'Samoa': 'rgba(204,124,124,1.0)', u'Norfolk Island': 'rgba(192,253,0,1.0)', u'United Arab Emirates': 'rgba(75,0,85,1.0)', u'Guam': 'rgba(0,170,152,1.0)', u'India': 'rgba(0,163,83,1.0)', u'Azerbaijan': 'rgba(125,0,142,1.0)', u'Madagascar': 'rgba(0,231,0,1.0)', u'Lesotho': 'rgba(0,207,0,1.0)', u'Saint Vincent and the Grenadines': 'rgba(204,12,12,1.0)', u'Kenya': 'rgba(0,167,0,1.0)', u'Macao': 'rgba(0,218,0,1.0)', u'Turkey': 'rgba(218,0,0,1.0)', u'Afghanistan': 'rgba(9,0,11,1.0)', u'Bangladesh': 'rgba(131,0,148,1.0)', u'Mauritania': 'rgba(59,255,0,1.0)', u'Solomon Islands': 'rgba(255,141,0,1.0)', u'Turks and Caicos Islands': 'rgba(246,0,0,1.0)', u'Saint Lucia': 'rgba(0,199,0,1.0)', u'San Marino': 'rgba(255,105,0,1.0)', u'Mongolia': 'rgba(15,255,0,1.0)', u'France': 'rgba(0,154,219,1.0)', u'Macedonia, the former Yugoslav Republic of': 'rgba(0,242,0,1.0)', u'Syrian Arab Republic': 'rgba(249,0,0,1.0)', u'Bermuda': 'rgba(77,0,160,1.0)', u'Namibia': 'rgba(161,255,0,1.0)', u'Somalia': 'rgba(255,93,0,1.0)', u'Peru': 'rgba(241,231,0,1.0)', u'Vanuatu': 'rgba(204,92,92,1.0)', u'Nauru': 'rgba(220,244,0,1.0)', u'Seychelles': 'rgba(252,0,0,1.0)', u'Norway': 'rgba(212,247,0,1.0)', u'Malawi': 'rgba(117,255,0,1.0)', u'Cook Islands': 'rgba(0,0,213,1.0)', u'Benin': 'rgba(129,0,146,1.0)', u'Congo, the Democratic Republic of the': 'rgba(0,0,205,1.0)', u'Cuba': 'rgba(0,37,221,1.0)', u'Iran, Islamic Republic of': 'rgba(0,159,51,1.0)', u'Falkland Islands (Malvinas)': 'rgba(0,149,221,1.0)', u'Mayotte': 'rgba(147,255,0,1.0)', u'Heard Island and McDonald Islands': 'rgba(0,170,144,1.0)', u'China': 'rgba(0,0,193,1.0)', u'Armenia': 'rgba(93,0,107,1.0)', u'Timor-Leste': 'rgba(228,0,0,1.0)', u'Dominican Republic': 'rgba(0,120,221,1.0)', u'Ukraine': 'rgba(211,0,0,1.0)', u'Bahrain': 'rgba(134,0,151,1.0)', u'Tonga': 'rgba(225,0,0,1.0)', u'Finland': 'rgba(0,144,221,1.0)', u'Western Sahara': 'rgba(0,133,221,1.0)', u'Cayman Islands': 'rgba(0,56,221,1.0)', u'Central African Republic': 'rgba(0,0,173,1.0)', u'Mexico': 'rgba(0,236,0,1.0)', u'Tajikistan': 'rgba(236,0,0,1.0)', u'Liechtenstein': 'rgba(0,202,0,1.0)', u'Belarus': 'rgba(99,0,158,1.0)', u'Mali': 'rgba(0,244,0,1.0)', u'Sweden': 'rgba(255,9,0,1.0)', u'Bulgaria': 'rgba(133,0,150,1.0)', u'Virgin Islands, U.S.': 'rgba(204,60,60,1.0)', u'Mauritius': 'rgba(103,255,0,1.0)', u'Romania': 'rgba(255,193,0,1.0)', u'Angola': 'rgba(19,0,21,1.0)', u'French Southern Territories': 'rgba(119,0,136,1.0)', u'Portugal': 'rgba(251,213,0,1.0)', u'Trinidad and Tobago': 'rgba(222,0,0,1.0)', u'Tokelau': 'rgba(233,0,0,1.0)', u'Cyprus': 'rgba(0,65,221,1.0)', u'South Georgia and the South Sandwich Islands': 'rgba(255,165,0,1.0)', u'Brunei Darussalam': 'rgba(35,0,166,1.0)', u'Qatar': 'rgba(255,201,0,1.0)', u'Malaysia': 'rgba(132,255,0,1.0)', u'Austria': 'rgba(123,0,140,1.0)', u'Mozambique': 'rgba(44,255,0,1.0)', u'Slovenia': 'rgba(255,21,0,1.0)', u'Uganda': 'rgba(212,0,0,1.0)', u'Hungary': 'rgba(0,167,115,1.0)', u'Niger': 'rgba(188,255,0,1.0)', u'United States': 'rgba(207,0,0,1.0)', u'Brazil': 'rgba(56,0,163,1.0)', u'Faroe Islands': 'rgba(0,155,215,1.0)', u'Guinea': 'rgba(0,166,183,1.0)', u'Panama': 'rgba(236,239,0,1.0)', u'Korea, Republic of': 'rgba(0,180,0,1.0)', u'Costa Rica': 'rgba(0,28,221,1.0)', u'Luxembourg': 'rgba(0,212,0,1.0)', u'Cape Verde': 'rgba(0,19,221,1.0)', u'Andorra': 'rgba(56,0,64,1.0)', u'Gibraltar': 'rgba(0,164,187,1.0)', u'Ireland': 'rgba(0,161,61,1.0)', u'Pakistan': 'rgba(232,240,0,1.0)', u'Palau': 'rgba(244,226,0,1.0)', u'Nigeria': 'rgba(196,252,0,1.0)', u'Ecuador': 'rgba(0,125,221,1.0)', u'Czech Republic': 'rgba(0,75,221,1.0)', u'Viet Nam': 'rgba(204,76,76,1.0)', u'Australia': 'rgba(122,0,139,1.0)', u'Algeria': 'rgba(0,122,221,1.0)', u"Korea, Democratic People's Republic of": 'rgba(249,215,0,1.0)', u'El Salvador': 'rgba(255,117,0,1.0)', u'Tuvalu': 'rgba(216,0,0,1.0)', u'South Africa': 'rgba(204,156,156,1.0)', u'Saint Pierre and Miquelon': 'rgba(255,81,0,1.0)', u'Holy See (Vatican City State)': 'rgba(204,0,0,1.0)', u'Marshall Islands': 'rgba(0,239,0,1.0)', u'Chile': 'rgba(0,0,189,1.0)', u'Puerto Rico': 'rgba(248,218,0,1.0)', u'Belgium': 'rgba(127,0,144,1.0)', u'Kiribati': 'rgba(0,175,0,1.0)', u'Haiti': 'rgba(0,169,125,1.0)', u'Belize': 'rgba(88,0,159,1.0)', u'Hong Kong': 'rgba(0,170,147,1.0)', u'Sierra Leone': 'rgba(255,129,0,1.0)', u'Georgia': 'rgba(0,160,199,1.0)', u"Lao People's Democratic Republic": 'rgba(0,188,0,1.0)', u'Gambia': 'rgba(0,168,175,1.0)', u'Philippines': 'rgba(243,229,0,1.0)', u'Netherlands Antilles': 'rgba(65,0,75,1.0)', u'Croatia': 'rgba(0,170,139,1.0)', u'French Polynesia': 'rgba(255,205,0,1.0)', u'Guernsey': 'rgba(0,162,195,1.0)', u'Thailand': 'rgba(238,0,0,1.0)', u'Switzerland': 'rgba(0,0,185,1.0)', u'Grenada': 'rgba(0,170,163,1.0)', u'Taiwan, Province of China': 'rgba(215,0,0,1.0)', u'\xc5land Islands': 'rgba(37,0,43,1.0)', u'Isle of Man': 'rgba(0,165,93,1.0)', u'Tanzania, United Republic of': 'rgba(214,0,0,1.0)', u'Chad': 'rgba(244,0,0,1.0)', u'Estonia': 'rgba(0,138,221,1.0)', u'Uruguay': 'rgba(208,0,0,1.0)', u'Equatorial Guinea': 'rgba(0,170,168,1.0)', u'Lebanon': 'rgba(0,191,0,1.0)', u'Svalbard and Jan Mayen': 'rgba(255,157,0,1.0)', u'Uzbekistan': 'rgba(206,0,0,1.0)', u'Tunisia': 'rgba(219,0,0,1.0)', u'Djibouti': 'rgba(0,93,221,1.0)', u'Greenland': 'rgba(0,170,160,1.0)', u'Antigua and Barbuda': 'rgba(121,0,138,1.0)', u'Spain': 'rgba(0,136,221,1.0)', u'Colombia': 'rgba(0,0,217,1.0)', u'Burundi': 'rgba(126,0,143,1.0)', u'Slovakia': 'rgba(255,33,0,1.0)', u'Fiji': 'rgba(0,146,221,1.0)', u'Barbados': 'rgba(45,0,164,1.0)', u'Saint Martin (French part)': 'rgba(0,220,0,1.0)', u'Italy': 'rgba(0,154,8,1.0)', u'Bhutan': 'rgba(24,0,167,1.0)', u'Sudan': 'rgba(255,177,0,1.0)', u'Bolivia, Plurinational State of': 'rgba(67,0,162,1.0)', u'Nepal': 'rgba(216,245,0,1.0)', u'Malta': 'rgba(0,247,0,1.0)', u'Netherlands': 'rgba(208,248,0,1.0)', u'Northern Mariana Islands': 'rgba(29,255,0,1.0)', u'Suriname': 'rgba(255,45,0,1.0)', u'Anguilla': 'rgba(28,0,32,1.0)', u'Israel': 'rgba(0,155,19,1.0)', u'R\xe9union': 'rgba(255,197,0,1.0)', u'Indonesia': 'rgba(0,166,104,1.0)', u'Iceland': 'rgba(0,157,29,1.0)', u'Zambia': 'rgba(204,172,172,1.0)', u'Senegal': 'rgba(255,173,0,1.0)', u'Papua New Guinea': 'rgba(245,223,0,1.0)', u'Zimbabwe': 'rgba(204,188,188,1.0)', u'Germany': 'rgba(0,84,221,1.0)', u'Denmark': 'rgba(0,112,221,1.0)', u'Kazakhstan': 'rgba(0,164,0,1.0)', u'Poland': 'rgba(247,221,0,1.0)', u'Moldova, Republic of': 'rgba(0,228,0,1.0)', u'Eritrea': 'rgba(0,130,221,1.0)', u'Kyrgyzstan': 'rgba(0,170,0,1.0)', u'Saint Barth\xe9lemy': 'rgba(109,0,156,1.0)', u'British Indian Ocean Territory': 'rgba(0,162,72,1.0)', u'Iraq': 'rgba(0,158,40,1.0)', u'Montserrat': 'rgba(73,255,0,1.0)', u'New Caledonia': 'rgba(176,255,0,1.0)', u'Paraguay': 'rgba(252,210,0,1.0)', u'Latvia': 'rgba(0,215,0,1.0)', u'South Sudan': 'rgba(204,204,204,1.0)', u'Guyana': 'rgba(0,170,149,1.0)', u'Guadeloupe': 'rgba(0,167,179,1.0)', u"C\xf4te d'Ivoire": 'rgba(0,0,197,1.0)', u'Morocco': 'rgba(0,223,0,1.0)', u'Honduras': 'rgba(0,170,141,1.0)', u'Myanmar': 'rgba(0,250,0,1.0)', u'Bouvet Island': 'rgba(13,0,168,1.0)', u'Egypt': 'rgba(0,128,221,1.0)', u'Nicaragua': 'rgba(200,251,0,1.0)', u'Singapore': 'rgba(255,169,0,1.0)', u'Serbia': 'rgba(255,69,0,1.0)', u'Botswana': 'rgba(3,0,170,1.0)', u'United Kingdom': 'rgba(0,159,203,1.0)', u'Antarctica': 'rgba(112,0,128,1.0)', u'Congo': 'rgba(0,0,209,1.0)', u'Greece': 'rgba(0,170,165,1.0)', u'Sri Lanka': 'rgba(0,204,0,1.0)', u'French Guiana': 'rgba(0,170,155,1.0)', u'Palestinian Territory, Occupied': 'rgba(253,207,0,1.0)', u'Comoros': 'rgba(0,9,221,1.0)'}


def get_from_flat_dict(list_of_dicts, key, default=None):
    '''Extract data from a list of dicts with keys 'key' and 'value'
    e.g. pkg_dict['extras'] = [{'key': 'language', 'value': '"french"'}, ... ]
    '''
    for dict_ in list_of_dicts:
        if dict_.get('key', '') == key:
            return (dict_.get('value', default) or '').strip('"')
    return default


def extended_build_nav(*args):
    # we go through the args, add links for raw links,
    
    output = ''
    for item in args:
        menu_item, title = item[:2]

        active = ""
        for keyword in ('/pages', '/dataset', '/document', '/organization', '/data', '/about'):          
            if keyword in menu_item and keyword in h.current_url():
                active = "active" 

        output += literal(
            '<li><a href="%s" class="%s">%s</a></li>' % (menu_item, active, title)
        )
    return output

def dataset_count():
    try:
        q = toolkit.get_action('package_search')({}, {'q': 'type:dataset'})
        return q.get('count')
    except Exception:
        return ''

def document_count():
    try:
        q = toolkit.get_action('package_search')({}, {'q': 'type:document'})
        return q.get('count')
    except Exception:
        return ''

def country_count():
    try:
        q = toolkit.get_action('package_search')({}, {'facet.field': ['country'], 'facet.limit': -1})
        return len(q.get('facets').get('country').keys())
    except Exception:
        return ''

def theme_counts():
    try:
        q = toolkit.get_action('package_search')({}, {'facet.field': ['category'], 'facet.limit': -1})
        return q.get('facets').get('category', {})
    except Exception:
        return {}

def sectorcolors():
    return {'Mining': '#e25020', 'Oil and Gas': '#000000'}

def countrycolors():
    return ccolors

def sort_by_display_name(facets):
    return natsorted(facets, key=lambda x: x['display_name'])

#Change the display of question numbers from their index representation (int) to a text label used in the schema
def get_facet_items_dict_questions(facet, limit=None, exclude_active=False):
    if facet != 'question':
        return []
    
    facets = h.get_facet_items_dict(facet, limit=None, exclude_active=False)

    newfacets = []

    for facet in facets:
        if not facet or len(facet) == 0:
            continue
        newfacet = facet
        
        #Questions can get deleted from the schema, then we have no label
        newfacet['display_name'] = qchoices.get(facet['name'], facet['name'])
        newfacets.append(newfacet)
    
    return sort_by_display_name(newfacets)

def get_facet_items_dict_categories(facet, limit=None, exclude_active=False):
    facets = h.get_facet_items_dict(facet, limit=None, exclude_active=False)
    return sort_by_display_name(facets)


class NrgiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    
    def before_index(self, pkg_dict):
        # JSON Strings to lists
        questions = []
        multivalued_elements = ['scoring_question', 'law_practice_question', 'question', 'country', 'country_iso3', 'assessment_year', 'category']
        if pkg_dict['type'] != 'document':
            multivalued_elements.append('year')
        for element in multivalued_elements:
            newlist = []
            aslist = json.loads(pkg_dict.get(element, '[]'))
            #Can be used to debug paster rebuild if bad data is in the DB
            #print pkg_dict.get('id'), element, pkg_dict.get(element, '[]')
            for value in aslist:
                newlist.append(value)
            pkg_dict[element] = newlist
        return pkg_dict

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nrgi')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_from_flat_dict': get_from_flat_dict,
            'extended_build_nav': extended_build_nav,
            'dataset_count': dataset_count,
            'document_count': document_count,
            'country_count': country_count,
            'theme_counts': theme_counts,
            'sectorcolors': sectorcolors,
            'countrycolors': countrycolors,
            'get_facet_items_dict_questions': get_facet_items_dict_questions,
            'get_facet_items_dict_categories': get_facet_items_dict_categories
        }

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        if package_type in ('record', 'dataset'):
            facets_dict = OrderedDict([
                ('category', toolkit._('Natural Resource Charter Precepts')),
                ('country', toolkit._('Countries')),
                #('year', toolkit._('Year')),
                ('res_format', toolkit._('Formats'))
                #As nice as this is, the code to get the stars interferes with custom nrgi facets template
                #('openness_score', toolkit._('Openness'))
            ])
            
        elif package_type == 'document':
            facets_dict = OrderedDict([
                #('subcomponent', toolkit._('Sub-components')),
                ('category', toolkit._('Natural Resource Charter Precepts')),
                ('country', toolkit._('Countries')),
                #('year', toolkit._('Year')),
                #('assessment_type', toolkit._('Assessment Type')),
                #('law_practice_question', toolkit._('Law/Practice Question')),
                ('question', toolkit._('Questions'))
            ])

        return facets_dict
        
        

    def organization_facets(self, facets_dict, organization_type, package_type):
        #Why so convoluted? I'll tell you why, here's why: https://github.com/ckan/ckan/issues/2713
        for key in facets_dict:
            del facets_dict[key]

        g_facets_dict = OrderedDict([
                  ('country', toolkit._('Countries')),
                  #('year', toolkit._('Year')),
                  ('res_format', toolkit._('Formats')),
                  #As nice as this is, the code to get the stars interferes with custom nrgi facets template
                  #('openness_score', toolkit._('Openness')),
                  ('category', toolkit._('Natural Resource Charter Precepts')),
                  ('country', toolkit._('Countries')),
                  ('assessment_type', toolkit._('Assessment Type')),
                  ('question', toolkit._('Questions'))#,
                  #Removed until we sort multivalued facets properly ('law_practice_question', toolkit._('Law/Practice Question'))
              ])
        facets_dict.update(g_facets_dict)
        return facets_dict

    # IRoutes

    def after_map(self, map):
        map.connect('resource_search', '/resource_search',
                    controller='ckanext.nrgi.controller:NrgiController',
                    action='search')
        return map
