# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = 'The Online Critical Pseudepigrapha'
response.subtitle = T('Developing and Publishing Accurate Texts of the "Old Testament Pseudepigrapha"\
    and related literature')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Ian W. Scott <you@example.com>'
response.meta.description = 'Free-access editions of the "Old Testament Pseudepigrapha"\
    and related literature'
response.meta.keywords = 'early judaism, religion, ancient, literature, Pseudepigrapha,\
    apocrypha, textual criticism, primary texts, sources, manuscripts'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2006-2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Documents'), False, URL('default','index'), []),
    (T('Get involved'), False, URL('default','page/get-involved'), []),
    (T('Help'), False, URL('default','page', args=['help']), []),
    (T('Bug reports'), False, URL('default','page', args=['bugs']), []),
    (T('Roadmap'), False, URL('default','page', args=['roadmap']), []),
    (T('Copyright'), False, URL('default','page', args=['copyright']), []),
    (T('Contact us'), False, URL('default','page', args=['contact']), []),  
    ]

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu+=[
        (SPAN('web2py',_style='color:yellow'),False, None, [
                (T('This App'),False,URL('admin','default','design/%s' % app), [
                        (T('Controller'),False,
                         URL('admin','default','edit/%s/controllers/%s.py' % (app,ctr))),
                        (T('View'),False,
                         URL('admin','default','edit/%s/views/%s' % (app,response.view))),
                        (T('Layout'),False,
                         URL('admin','default','edit/%s/views/layout.html' % app)),
                        (T('Stylesheet'),False,
                         URL('admin','default','edit/%s/static/css/web2py.css' % app)),
                        (T('DB Model'),False,
                         URL('admin','default','edit/%s/models/db.py' % app)),
                        (T('Menu Model'),False,
                         URL('admin','default','edit/%s/models/menu.py' % app)),
                        (T('Database'),False, URL(app,'appadmin','index')),
                        (T('Errors'),False, URL('admin','default','errors/' + app)),
                        (T('About'),False, URL('admin','default','about/' + app)),
                        ]),
                ('web2py.com',False,'http://www.web2py.com', [
                        (T('Download'),False,'http://www.web2py.com/examples/default/download'),
                        (T('Support'),False,'http://www.web2py.com/examples/default/support'),
                        (T('Demo'),False,'http://web2py.com/demo_admin'),
                        (T('Quick Examples'),False,'http://web2py.com/examples/default/examples'),
                        (T('FAQ'),False,'http://web2py.com/AlterEgo'),
                        (T('Videos'),False,'http://www.web2py.com/examples/default/videos/'),
                        (T('Free Applications'),False,'http://web2py.com/appliances'),
                        (T('Plugins'),False,'http://web2py.com/plugins'),
                        (T('Layouts'),False,'http://web2py.com/layouts'),
                        (T('Recipes'),False,'http://web2pyslices.com/'),
                        (T('Semantic'),False,'http://web2py.com/semantic'),
                        ]),
                ]
         )]
#_()

