#
# Flask-Rev
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import json
import logging


logger = logging.getLogger('Flask-Rev')


class Rev(object):
    """
    Flask-Rev

    Refer to http://flask-rev.readthedocs.io for more details.

    :param app: Flask app to initialize with. Defaults to `None`
    """

    # https://thusoy.com/2014/server-side-assets-file-revisioning

    manifest = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        manifest = app.config.get('REV_MANIFEST')
        if manifest is None:
            logger.debug('REV_MANIFEST not set')
            return
        try:
            with app.open_resource(manifest, mode='r') as fp:
                self.manifest = json.load(fp)
        except IOError as error:
            logger.error(str(error))
            return
        app.url_defaults(self._revisioned_filename)

    def _revisioned_filename(self, endpoint, values):
        if endpoint == 'static':
            filename = self.manifest.get(values.get('filename'))
            if filename is not None:
                values['filename'] = filename


# EOF
