import copy
import json

import pylons.config as config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

from webhelpers.html import literal


def extended_build_nav(*args):
    # we go through the args, add links for raw links, and then pass the rest to core build_nav_main
    output = ''
    for item in args:
        menu_item, title = item[:2]

        if len(item) == 3 and not check_access(item[2]):
            continue

        if menu_item.startswith('http') or menu_item.startswith('/'):
            # it's a link
            output += literal('<li><a href="%s">%s</a></li>' % (menu_item, title))
        else:
            # give it to the core helper for this
            output += h._make_menu_item(menu_item, title)
    return output


class NrgiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nrgi')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            # 'frontpage_section_enabled': lambda section: section in toolkit.aslist(config.get('derilinx.frontpage.sections', [])),
            # 'frontpage_sections_enabled': lambda: len(toolkit.aslist(config.get('derilinx.frontpage.sections', []))) > 0,
            'extended_build_nav': extended_build_nav,
        }
