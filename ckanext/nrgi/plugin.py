from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

from webhelpers.html import literal


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
        q = toolkit.get_action('package_search')({}, {})
        return q.get('count')
    except Exception:
        return ''


def publisher_count():
    try:
        q = toolkit.get_action('organization_list')({}, {})
        return len(q)
    except Exception:
        return ''


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
            'publisher_count': publisher_count
        }

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        if (package_type == 'dataset'):
            facets_dict = OrderedDict([
                ('country', toolkit._('Country')),
                ('year', toolkit._('Year')),
                ('assessment_type', toolkit._('Assessment Type')),
                # ('category', plugins.toolkit._('Categories')),
                ('tags', toolkit._('Tags')),
                ('res_format', toolkit._('Formats')),
                ('license_id', toolkit._('Licenses')),
                ('openness_score', toolkit._('Openness'))
            ])
        return facets_dict

    # IRoutes

    def after_map(self, map):
        map.connect('resource_search', '/resource_search',
                    controller='ckanext.nrgi.controller:NrgiController',
                    action='search')
        return map
