# encoding: utf-8

import ckan
import pylons
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import BaseController
import ckan.lib.helpers as h

c = toolkit.c

class NrgiController(BaseController):
    def search(self):
        context = {'model': ckan.model, 'session': ckan.model.Session,
                   'user': pylons.c.user}

        q = c.q = toolkit.request.params.get('query', u'')

        query = toolkit.get_action('resource_search')(context, {'query': q})

        c.page = h.Page(
            collection=query['results'],
            # page=page,
            # url=pager_url,
            item_count=query['count'],
            # items_per_page=limit
        )

        return p.toolkit.render('ckanext/nrgi/resource_search/search.html')
