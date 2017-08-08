#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

if 0:
    from gluon import current, T, auth, I, A, URL, SPAN
    response = current.response
    request = current.request

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = 'The Online Critical Pseudepigrapha'
response.mobiletitle = 'OCP'
response.subtitle = T('Developing and Publishing Accurate Texts of the "Old Testament Pseudepigrapha"\
    and related literature')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Ian W. Scott <scottianw@gmail.com>'
response.meta.description = 'Free-access editions of the "Old Testament Pseudepigrapha"\
    and related literature'
response.meta.keywords = 'early judaism, religion, ancient, literature, Pseudepigrapha,\
    apocrypha, textual criticism, primary texts, sources, manuscripts'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2006-2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## main application menu
#########################################################################

app = request.application
ctr = request.controller
response.menu = []

if auth.has_membership('editors', auth.user_id):
    response.menu += [
        (T('Drafts'), False, A(I(_class='fa fa-book'), SPAN(' Drafts', _class="visible-lg-inline"),
                               _href=URL('default', 'page', args=['drafts']),
                               _class='draftslink'), []),
    ]

if auth.has_membership('administrators', auth.user_id):
    response.menu += [
        (T('Admin'), False, A(I(_class='fa fa-cog'), SPAN(' Admin', _class="visible-lg-inline"),
                              _href='#', _class='adminlink'), [
            (T('Documents'), False, A('Documents', _href=URL('default', 'listing', args=['docs'])), []),
            (T('Bibliography'), False, A('Bibliography', _href=URL('default', 'listing', args=['biblio'])), []),
            (T('Pages'), False, A('Pages', _href=URL('default', 'listing', args=['pages'])), []),
            (T('Users'), False, A('Users', _href=URL('default', 'listing', args=['auth_user'])), []),
            (T('Database'), False, A('Database', _href=URL(app, 'appadmin', 'index')), []),
            (T('Web IDE'), False, A('Web IDE', _href=URL('admin', 'default', 'design/{}'.format(app))), []),
            (T('Errors'), False, A('Errors', _href=URL('admin', 'default', 'errors/{}'.format(app))), []),
        ]),
    ]

response.menu += [
    (T('Documents'), False, A(I(_class='fa fa-book'),
                              SPAN(' Documents', _class="visible-lg-inline"),
                              _href=URL('default', 'index'), _class='documentslink'), []),
    (T('Help and Information'), False, A(I(_class='fa fa-info-circle'),
                                         SPAN(' Help and Information',  _class="visible-lg-inline"),
                                         _href='#', _class='helplink'), [
        (T('About'), False, A(I(_class='fa fa-info-circle fa-fw'),
                              SPAN('About'),
                              _href=URL('default', 'page', args=['about']),
                              _class='aboutlink'), []),
        (T('FAQ'), False, A(I(_class='fa fa-question-circle fa-fw'),
                            SPAN('FAQ'),
                            _href=URL('default', 'page', args=['faq']),
                            _class='faqlink'), []),
        (T('Copyright'), False, A(I(_class='fa fa-copyright fa-fw'),
                                  SPAN(' Copyright'),
                                  _href=URL('default', 'page', args=['copyright']),
                                  _class='copyrightlink'), []),
    ])
    # (T('Contact Us'), False, A(I(_class='fa fa-bullhorn'),
    #                            SPAN(' Contact us', _class="visible-lg-inline"),
    #                            _href=URL('default', 'page', args=['contact']), _class='contactlink'), [
    #     (T('Bug reports'), False, A(I(_class='fa fa-bug fa-fw'),
    #                                 SPAN(' Bug reports'),
    #                                 _href=URL('default', 'page', args=['bugs']),
    #                                 _class='bugslink'), []),
    #     (T('Suggestions'), False, A(I(_class='fa fa-commenting-o fa-fw'),
    #                                 SPAN(' Suggestions'),
    #                                 _href=URL('default', 'page', args=['suggestions']),
    #                                 _class='suggestionslink'), []),
    # ]),
    ]


def _():
    # shortcuts
    # useful links to internal and external resources
    response.menu += [
        (SPAN('web2py', _style='color:yellow'), False, None, [
                (T('This App'), False, URL('admin', 'default', 'design/%s' % app), [
                        (T('Controller'), False,
                         URL('admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
                        (T('View'), False,
                         URL('admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
                        (T('Layout'), False,
                         URL('admin', 'default', 'edit/%s/views/layout.html' % app)),
                        (T('Stylesheet'), False,
                         URL('admin', 'default', 'edit/%s/static/css/web2py.css' % app)),
                        (T('DB Model'), False,
                         URL('admin', 'default', 'edit/%s/models/db.py' % app)),
                        (T('Menu Model'), False,
                         URL('admin', 'default', 'edit/%s/models/menu.py' % app)),
                        (T('Database'), False, URL(app, 'appadmin', 'index')),
                        (T('Errors'), False, URL('admin', 'default', 'errors/' + app)),
                        (T('About'), False, URL('admin', 'default', 'about/' + app)),
                        ]),
                ('web2py.com', False, 'http://www.web2py.com', [
                        (T('Download'), False, 'http://www.web2py.com/examples/default/download'),
                        (T('Support'), False, 'http://www.web2py.com/examples/default/support'),
                        (T('Demo'), False, 'http://web2py.com/demo_admin'),
                        (T('Quick Examples'), False, 'http://web2py.com/examples/default/examples'),
                        (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
                        (T('Videos'), False, 'http://www.web2py.com/examples/default/videos/'),
                        (T('Free Applications'), False, 'http://web2py.com/appliances'),
                        (T('Plugins'), False, 'http://web2py.com/plugins'),
                        (T('Layouts'), False, 'http://web2py.com/layouts'),
                        (T('Recipes'), False, 'http://web2pyslices.com/'),
                        (T('Semantic'), False, 'http://web2py.com/semantic'),
                        ]),
                ]
         )]
