# -*- coding: utf-8 -*-

from gluon.tools import Auth, Crud, Service, PluginManager, Recaptcha2
from gluon import current
request, response = current.request, current.response
from gluon.dal import DAL
import os

if 0:
    from gluon import URL

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


db = DAL('sqlite://storage.sqlite', fake_migrate=False, migrate=True)
current.db = db

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
# (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------
# get private data from secure file
# -------------------------------------------------------------
keydata = {}
with open('applications/grammateus3/private/app.keys', 'r') as keyfile:
    for line in keyfile:
        k, v = line.split()
        keydata[k] = v

auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

# create all tables needed by auth if not custom tables
auth.define_tables()

# -------------------------------------------------------------
# configure email
# -------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = keydata['email_server']  # 'logging' # SMTP server
print('mail.settings.server')
mail.settings.sender = keydata['email_address']  # email
mail.settings.login = '{}:{}'.format(keydata['email_user'],
                                     keydata['email_pass'])
mail.settings.tls = True
current.mail = mail

# -------------------------------------------------------------
# enable recaptcha (keys for ehosting)
# -------------------------------------------------------------
auth.settings.register_captcha = Recaptcha2(request,
                                            keydata['captcha_public_key'],
                                            keydata['captcha_private_key'])
auth.settings.retrieve_username_captcha = Recaptcha2(request,
                                                     keydata['captcha'
                                                             '_public_key'],
                                                     keydata['captcha'
                                                             '_private_key'])
auth.settings.retrieve_password_captcha = Recaptcha2(request,
                                                     keydata['captcha'
                                                             '_public_key'],
                                                     keydata['captcha'
                                                             '_private_key'])

# -------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.messages.verify_email = 'Click on the link %(link)s ' \
    + 'to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link %(link)s ' \
    + 'to reset your password'
