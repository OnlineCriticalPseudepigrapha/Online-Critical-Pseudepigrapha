# -*- coding: utf-8 -*-

from gluon.tools import Auth, Crud, Service, PluginManager, Recaptcha
from gluon import current
request, response = current.request, current.response
from gluon.dal import DAL
import os

"""
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# request.requires_https()
"""

if current.request.is_local:
    from gluon.custom_import import track_changes
    track_changes()


def check_path(path):
    if os.path.exists(path):
        return path
    raise OSError(2, "{}: {}".format(os.strerror(2), path))

db = DAL('sqlite://storage.sqlite')
current.db = db

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
# (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

# create all tables needed by auth if not custom tables
auth.define_tables()

# configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'


# enable recaptcha (keys for ianwscott.fluxflex.com)
auth.settings.captcha = Recaptcha(request,
    '6Ldy5ccSAAAAALlI2gJuwFQYe-iaZ_oyQs3nhX-9',
    '6Ldy5ccSAAAAABr8FhJeb_aELfEC7SJOOyvhJp0R')
auth.settings.login_captcha = None
auth.settings.register_captcha = Recaptcha(request,
    '6Ldy5ccSAAAAALlI2gJuwFQYe-iaZ_oyQs3nhX-9',
    '6Ldy5ccSAAAAABr8FhJeb_aELfEC7SJOOyvhJp0R')
auth.settings.retrieve_username_captcha = Recaptcha(request,
    '6Ldy5ccSAAAAALlI2gJuwFQYe-iaZ_oyQs3nhX-9',
    '6Ldy5ccSAAAAABr8FhJeb_aELfEC7SJOOyvhJp0R')
auth.settings.retrieve_password_captcha = Recaptcha(request,
    '6Ldy5ccSAAAAALlI2gJuwFQYe-iaZ_oyQs3nhX-9',
    '6Ldy5ccSAAAAABr8FhJeb_aELfEC7SJOOyvhJp0R')

# configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
