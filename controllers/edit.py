# -*- coding: utf-8 -*-

from parse import BookManager, Book

if 0:
    from gluon import current, URL, A, SPAN, P
    request = current.request
    session = current.session
    response = current.response
    db = current.db


def index():
    session.filename = request.args[0]
    filename = session.filename

    BookManager.copy_book(filename)

    # get parsed document info
    info, p = _get_bookinfo(filename)
    #get title of document
    title = info['book']['title']

    buttons = {'renumber units': URL('edit', 'renumber', args=[filename]),
               'publish': URL('edit', 'publish', args=[filename])}

    return {'filename': filename,
            'buttons': buttons,
            'title': title}

def _get_bookinfo(filename):
    """
    Retrieve info about the book and parsed book object from session or parser.

    """
    vbs = True
    # FIXME: error when using session values
    # _element object can't be pickled, and pickling is necessary to store
    # an object in session
    if 0 and ('info' in session.keys()) and (filename in session.info.keys()) and \
            ('p' in session.keys()) and (filename in session.p.keys()):
        info = session.info[filename]
        p = cPickle.loads(session.p[filename])
        if vbs: print info
        if vbs: print 'using session.info'
    else:
        book_file = 'applications/grammateus3/static/docs/drafts/{}.xml'.format(filename)
        p = Book.open(book_file)
        if vbs: print 'using newly parsed book object'
        # if session.p:
        #     session.p[filename] = p
        # else:
        #     session.p = {filename: p}
        info = p.book_info()
        session.info = {filename: info}
    # if vbs: print "info", pprint(info)
    return info, p

def renumber():
    """
    Renumber units and options throughout the current document.

    Units must be numbered consecutively and options must be numbered starting
    at 0 within each unit.
    """
    print 'edit::renumber:'
    filename = session.filename
    return BookManager.renumber_units(filename)

def publish():
    """
    Copy current draft xml file to the public location for document files.
    """
    print 'edit::publish:'
    filename = session.filename
    return BookManager.publish(filename)
