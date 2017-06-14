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
    # and then pass the rest to core build_nav_main
    output = ''
    for item in args:
        menu_item, title = item[:2]

        if len(item) == 3 and not toolkit.check_access(item[2]):
            continue

        if menu_item.startswith('http') or menu_item.startswith('/'):
            # it's a link
            output += literal(
                '<li><a href="%s">%s</a></li>' % (menu_item, title)
            )
        else:
            # give it to the core helper for this
            output += h._make_menu_item(menu_item, title)
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

def get_facet_items_dict_questions(facet, limit=None, exclude_active=False):
    if facet != 'question':
        return []
    
    facets = h.get_facet_items_dict(facet, limit=None, exclude_active=False)

    newfacets = []
    facet_counts = {}

    for facet in facets:
        if not facet or len(facet) == 0:
            continue
        newfacet = facet
        #Clean up
        num = newfacet['display_name'].replace('[', '').replace(']', '').replace('"', '').replace(' ', '')
        if num == '':
            continue
        #Handle multiple questions; should actually be doable in SOLR
        if ',' in num:
            parts = num.split(',')
            #For counts of items having both, add the total to both counts
            for part in parts:
                if part in facet_counts:
                    facet_counts[part] = facet_counts[part] + newfacet['count']
                else:
                    facet_counts[part] = newfacet['count']
            #And now don't show it
            continue
        if num in facet_counts:
            facet_counts[num] = facet_counts[num] + newfacet['count']
        else:
            facet_counts[num] = newfacet['count']

        newfacet['display_name'] = qchoices[num] 
        newfacet['num'] = num
        newfacet['name'] = '[\\"' + num  + '\\"]'
        newfacets.append(newfacet)

    for facet in newfacets:
       facet['count'] = facet_counts[facet['num']]
       del facet_counts[facet['num']]

    #The remaining ones don't have a facet to update, create new ones
    for count in facet_counts:
       name = '[\\"' + count  + '\\"]'
       cfacet = {'count': facet_counts[count], 'display_name': qchoices[count], 'name': name}
       newfacets.append(cfacet)

    #Now we have to resort
    sortedfacets = sorted(newfacets, key=lambda k: k['count'], reverse=True)

    #Mark selected
    selectedfacet = None
    for item in request.params.items():
        if item[0] == "question":
            selectedfacet = item[1]

    for facet in sortedfacets:
        if facet["name"] == selectedfacet:
            facet["active"] = True

    return sortedfacets

class NrgiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

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
            'get_facet_items_dict_questions': get_facet_items_dict_questions
        }

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        if package_type == 'dataset':
            facets_dict = OrderedDict([
                ('country', toolkit._('Countries')),
                #('year', toolkit._('Year')),
                ('res_format', toolkit._('Formats')),
                ('openness_score', toolkit._('Openness'))
            ])
            
        elif package_type == 'document':
            facets_dict = OrderedDict([
                ('category', toolkit._('Sub-components')),
                ('country', toolkit._('Countries')),
                #('year', toolkit._('Year')),
                ('assessment_type', toolkit._('Assessment Type')),
                ('question', toolkit._('Questions')),
                ('scoring_question', toolkit._('Question Usage')),
                ('law_practice_question', toolkit._('Law/Practice Question'))
            ])

        return facets_dict
        
        

    def organization_facets(self, facets_dict, organization_type, package_type):
        #Why so convoluted? I'll tell you why, here's why: https://github.com/ckan/ckan/issues/2713
        for key in facets_dict:
            del facets_dict[key]
        if package_type == 'dataset':   
          g_facets_dict = OrderedDict([
                  ('country', toolkit._('Countries')),
                  #('year', toolkit._('Year')),
                  ('res_format', toolkit._('Formats')),
                  ('openness_score', toolkit._('Openness'))
              ])
        elif package_type == 'document': 
          g_facets_dict = OrderedDict([
                  ('category', toolkit._('Sub-components')),
                  ('country', toolkit._('Countries')),
                  #('year', toolkit._('Year')),
                  ('assessment_type', toolkit._('Assessment Type')),
                  ('question', toolkit._('Questions')), #See above
                  ('scoring_question', toolkit._('Question Usage')),
                  ('law_practice_question', toolkit._('Law/Practice Question'))
              ])
        facets_dict.update(g_facets_dict)
        return facets_dict

    # IRoutes

    def after_map(self, map):
        map.connect('resource_search', '/resource_search',
                    controller='ckanext.nrgi.controller:NrgiController',
                    action='search')
        return map
