# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

if 0:
    from gluon import db, current, auth, LOAD
    response = current.response
    request = current.request


def index():
    """
    Present main index page.

    Send dictionary of document records to the view views/default/index.html
    """
    docrows = db(db.docs.id > 0).select()
    return {'docrows': docrows}


def page():
    """
    """
    pagelabel = request.args[0]
    pagerow = db(db.pages.page_label == pagelabel).select().first()
    return {'body': pagerow['body'],
            'title': pagerow['title']}


def list():
    """
    Present a plugin_listandedit widget for creating and editing db records.

    URL Arguments
    ---------

        0:  The name of the db table to be manipulated by the widget.

    """

    widget = LOAD('plugin_listandedit', 'widget.load',
                  args=request.args,
                  vars=request.vars,
                  ajax=False)
    return {'widget': widget}


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

'''
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
'''
