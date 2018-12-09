#
# Flask-Rev
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


"""
https://thusoy.com/2014/server-side-assets-file-revisioning
https://github.com/yeoman/grunt-filerev
https://github.com/richardbolt/grunt-filerev-assets
"""


import json
import warnings

from flask import url_for, current_app
from werkzeug.local import LocalProxy


assets = LocalProxy(lambda: current_app.config.get('FILEREV'))


class Rev(object):
    """
    Flask-Rev

    Refer to http://flask-rev.readthedocs.io for more details.

    :param app: Flask app to initialize with. Defaults to `None`
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # app.context_processor(revved_url_for)
        global url_for
        url_for = app.jinja_env.globals['url_for']

        app.jinja_env.globals['url_for'] = _revved_url_for
        app.filerev = self

        def inject_assets():
            return dict(assets=app.config.get('FILEREV'))

        app.context_processor(inject_assets)

        # TODO
        try:
            with app.open_resource(app.config.get('REV_MANIFEST'), mode='r') as f:
                filerevs = json.load(f)
                app.config['FILEREV'] = filerevs
        except IOError:
            warnings.warn('REV_MANIFEST not set', RuntimeWarning, stacklevel=2)
            app.config['FILEREV'] = {}


def revved_url_for():
    return {'url_for': _revved_url_for}


def _revved_url_for(endpoint, **values):
    if endpoint == 'static':
        original_filename = values.get('filename')
        if original_filename:
            revved_filename = current_app.config['FILEREV'].get(original_filename)
            if revved_filename:
                del values['filename']
                return url_for(endpoint, filename=revved_filename, **values)
    return url_for(endpoint, **values)


# EOF
