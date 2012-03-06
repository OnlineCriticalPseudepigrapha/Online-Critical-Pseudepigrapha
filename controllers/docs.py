# coding: utf8
from lxml import etree

from parse import BookParser

"""
List of session objects used in text display:
session.filename
session.info -- dict; parsed results of BookParser class for current doc
session.title -- string; title of current doc
session.versions -- list; names of all versions in current doc
"""

def index():
    filename = request.args[0]
    return dict(filename = filename)

def text():
    filename = request.args[0]
    #TODO: provide fallback and prompt if no filename is given in url
    
    #url to pass to web2py load helper in view to load doc section via ajax
    load_url = URL('docs', 'section.load', args=filename)

    return dict(load_url = load_url, filename = filename)

def section():
    """
    populates a single text pane via the section.load view (refreshable via ajax)
    """
    #get filename from end of url and parse the file with BookParser class
    filename = request.args[0]
    print filename
    book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
    p = BookParser(book_file)
    info = p.book_info()
    #get title of document
    title = info['title']
    #get names of all versions of current doc and select the version to display
    #use second url argument as version name if present, otherwise default to first version
    versions = [version['title'] for version in info['versions']]     
    if len(request.args) < 2:
        current_version = versions[0]
    else:
        current_version = request.args[1].replace('_', ' ')
        #move selected version to top of list for selectbox
        i = versions.index(current_version)
        versions.insert(0, versions.pop(i))

    ref = dict()
        
    print versions, current_version
    return dict(title = title, versions = versions, current_version = current_version, 
                info = info, filename = filename)

def test():
    filename = request.args[0]
    book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
    p = BookParser(book_file)
    info = p.book_info()

    title = info['title']
    for version in info['versions']:
        for key, value in version.items():
            if key != 'text_structure':
                print 'Version', key, '-->', value

            else:
                print 'Version textstructure'
                for ref, ref_val in value.items():
                    for unit, unit_val in ref_val.items():
                        for mss, mss_val in unit_val.items():
                            print '\t', ref, '-->', unit, '-->', mss, '-->', mss_val
        print '************'
    print
    print

    return dict(title = title, info = info)
