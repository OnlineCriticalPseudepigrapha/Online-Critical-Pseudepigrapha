# coding: utf8
import datetime

if 0:
    from gluon import db, Field, auth

db.define_table('docs',
    Field('name'),
    Field('filename'),
    Field('editor', db.auth_user, default=auth.user_id),
    Field('assistant_editor', db.auth_user, default=auth.user_id),
    Field('proofreader', db.auth_user, default=auth.user_id),
    Field('version', 'double'),
    Field('introduction', 'text'),
    Field('themes', 'text'),
    Field('status', 'text'),
    Field('bibliography', 'text'),
    Field('sigla', 'text'),
    Field('copyright', 'text'),
    format='%(name)s')

db.define_table('biblio',
    Field('record'),
    format='%(record)s')

db.define_table('pages',
    Field('page_label', 'string'),
    Field('title', 'string'),
    Field('body', 'text'),
    Field('poster', db.auth_user, default=auth.user_id),
    Field('post_date', 'datetime', default=datetime.datetime.utcnow()),
    format='%(title)s')

db.define_table('bugs',
    Field('title'),
    Field('body', 'text'),
    Field('poster', db.auth_user, default=auth.user_id),
    Field('post_date', 'datetime'),
    format='%(title)s')
