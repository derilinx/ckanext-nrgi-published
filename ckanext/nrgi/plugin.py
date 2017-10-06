from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

from webhelpers.html import literal

from ckan.common import request

import os
import json

qchoices = {}

with open(os.path.dirname(os.path.realpath(__file__)) + '/schema.json') as jsonfile:    
    schema = json.load(jsonfile)
    for field in schema['dataset_fields']:
        if field['field_name'] == 'question':
            for item in field['choices']:
                qchoices[item['value']] = item['label']
            break

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
    
    return sorted(newfacets, key=lambda x: x['display_name'])

class NrgiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    
    def before_index(self, pkg_dict):
        # JSON Strings to lists
        questions = []
        for element in ('scoring_question', 'law_practice_question', 'question', 'country', 'country_iso3', 'year', 'assessment_year', 'category'):
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
            'get_facet_items_dict_questions': get_facet_items_dict_questions
        }

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        if package_type == 'dataset':
            facets_dict = OrderedDict([
                ('category', toolkit._('Theme')),
                ('country', toolkit._('Countries')),
                #('year', toolkit._('Year')),
                ('res_format', toolkit._('Formats')),
                ('openness_score', toolkit._('Openness'))
            ])
            
        elif package_type == 'document':
            facets_dict = OrderedDict([
                ('subcomponent', toolkit._('Sub-components')),
                ('country', toolkit._('Countries')),
                #('year', toolkit._('Year')),
                ('assessment_type', toolkit._('Assessment Type')),
                ('law_practice_question', toolkit._('Law/Practice Question')),
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
                  ('openness_score', toolkit._('Openness')),
                  ('category', toolkit._('Sub-components')),
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
