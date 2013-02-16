# coding: utf8
from parse import Book
import pprint
import re

if 0:
    from gluon import current, URL, A, SPAN, H1, DIV, H2, H3, H4
    request = current.request
    session = current.session
    db = current.db

"""
List of session objects used in text display:
session.filename
session.info -- dict; parsed results of BookParser class for current doc
session.title -- string; title of current doc
session.versions -- list; names of all versions in current doc
session.refraw -- list; references in the first version
session.startref --
session.endref --
"""

def index():
    filename = request.args[0]
    return dict(filename = filename)

def text():
    session.filename = request.args[0]
    filename = session.filename
    #TODO: provide fallback and prompt if no filename is given in url

    #url to pass to web2py load helper in view to load doc section via ajax
    load_url = URL('docs', 'section.load', args=filename)

    #print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    print 'start of section() method with url ', request.url, varlist
    #get filename from end of url and parse the file with BookParser class
    print 'filename: ', filename
    if ('info' in session) and (filename in session.info):
        info = session.info[filename]
        print '\n\nstarting controller.section() using session.info'
    else:
        book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
        p = Book(book_file)
        info = p.book_info()
        session.info = {filename:info}
    #get title of document
    title = info['book']['title']

    #get names of all versions of current doc
    versions = info['version']
    session.versions = [v['attributes']['title'] for v in versions]
    first_v = versions[0]
    delimiters = first_v['divisions']['delimiters']
    levels = first_v['organisation_levels']

    #build flat list of references
    refraw = [ref for ref, units in first_v['text_structure'].items()]
    session.refraw = refraw

    #build list for starting ref
    if 'from' in request.vars:
        start_sel = request.vars['from'][:-1]
        start_sel = re.split('-', start_sel)
        #create string ref with proper delimiters
        startlist = [None] * (len(start_sel) + len(levels))
        startlist[::2] = start_sel
        startlist[1::2] = delimiters
        startref = ''.join(startlist)
        print 'using url ref ', start_sel
    else:
        startref = refraw[0]
        start_sel = re.split('[:\.,;_-]', startref)
        print 'using default first ref ', start_sel

    #build list for ending ref
    if 'to' in request.vars:
        end_sel = request.vars['to'][:-1]
        end_sel = re.split('-', end_sel)
        #create string ref with proper delimiters
        endlist = [None] * (len(end_sel) + len(levels))
        endlist[::2] = end_sel
        endlist[1::2] = delimiters
        endref = ''.join(endlist)
    else:
        regex = re.compile('^'+start_sel[0]+delimiters[0])
        #find all refs with the same top-level reference
        this_div = [ref for ref in refraw if regex.match(ref)]
        #choose the last one
        endref = this_div[-1]
        end_sel = re.split('[:\.,;_-]', endref)

    session.startref = startref
    session.endref = endref
    print 'start_sel', start_sel
    print 'end_sel', end_sel

    return dict(load_url = load_url, title = title, levels = levels,
        start_sel = start_sel, end_sel = end_sel, filename = filename)

def section():
    """
    populates a single text pane via the section.load view (refreshable via ajax)
    """
    #'verbose' variable is for turning testing output on and off
    verbose = False
    #print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    if verbose == True:
        print 'start of section() method with url ', request.url, varlist
    #get filename from end of url and parse the file with BookParser class
    filename = request.args[0]
    if verbose == True: print 'filename: ', filename
    if 0 and ('info' in session) and (filename in session.info):
        info = session.info[filename]
        if verbose == True:
            print '\n\nstarting controller.section() using session.info'
    else:
        book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
        p = Book(book_file)
        info = p.book_info()
        session.info = {filename:info}

    #select the version to display
    if 'version' in request.vars:
        current_version = request.vars['version'].replace('_', ' ')
        #move selected version to top of list for selectbox
        if 'versions' in session:
            i = session.versions.index(current_version)
            session.versions.insert(0, session.versions.pop(i))
        if verbose == True:
            print 'current version: ', current_version.replace(' ', '&nbsp;')
    else:
        current_version = session.versions[0]
        if verbose == True:
            print 'current version: ', current_version.replace(' ', '&nbsp;')

    #find selected version in parsed text
    for version in info['version']:
        if version['attributes']['title'] == current_version:
                curv = version
                vlang = curv['attributes']['language']
                levels = curv['organisation_levels']
    #get list of mss
    mslist = [[k.strip() for k, c in v.iteritems()] for v in curv['manuscripts']]
    if verbose == True: print 'mslist for this version: ', mslist
    #use the third url argument as manuscript name if present, otherwise default to first version
    #check for 'newval' value, indicating the version has changed
    if 'type' in request.vars and request.vars['type'] != 'newval':
        current_ms = request.vars['type'].replace('_', ' ')
        current_ms = current_ms.strip()
        if verbose == True: print 'current_ms: ', current_ms
        #move selected text type to top of list for ms selectbox
        i = mslist.index(current_ms)
        mslist.insert(0, mslist.pop(i))
    else:
        current_ms = mslist[0]
        if verbose == True: print 'current_ms: ', current_ms

    #gather text from units within the selected section of the doc
    #filters the current version for only readings in the current
    #text type
    reflist = session.refraw
    startref = session.startref
    start_sel = startref.split(':')
    endref = session.endref
    end_sel = endref.split(':')
    #make sure space delimiter is present at end of current_ms
    if current_ms[0][-1] != ' ':
        current_ms[0] += ' '


    text = []
    parsed_text = p.get_reference(current_version, start_sel)
    text.append(SPAN(startref, _class='ref'))
    for u, v in parsed_text.iteritems():
        for mss, reading in v.iteritems():
            if current_ms[0] in (mss + ' '):
                if reading == '':
                    text.append(A('*', _class='placeholder', _href=u))
                elif len(parsed_text.keys()) > 1:
                    text.append(A(reading, _class=vlang, _href=u))
                else:
                    text.append(SPAN(reading, _class = vlang))
            else:
                pass

    return dict(versions=session.versions, current_version=current_version,
                mslist=mslist, sel_text=text, filename=session.filename)


def apparatus():
    filename = request.args[0]
    if session.info and filename in session.info:
        info = session.info[filename]
        print '\n\nstarting controller.section() using session.info'
    else:
        book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
        p = Book(book_file)
        info = p.book_info()
        session.info[filename] = info

    #if no unit has been requested, present the default message
    if request.vars['called'] == 'no':
        rlist = SPAN('Click on any blue text to display textual variants for those words. If no links are available that may mean no variants are attested or it may mean that this document does not yet have a complete textual apparatus. See the document introduction for details.')
    #if a unit has been requested, assemble that unit's readings
    else:
        #get current version
        current_version = request.vars['version'].replace('_', ' ')
        print 'current version: ', current_version

        #find selected version in parsed text
        for version in info['versions']:
            for k, v in version.items():
                if k == 'title' and v == current_version:
                    curv = version
                    vlang = curv['language']

        #find requested unit and get reading information
        for ref, units in curv['text_structure'].items():
            for unit_ref, unit_val in units.items():
                if unit_ref == request.vars['unit']:
                    rlist = {k:v for k, v in unit_val.items()}

    return dict(rlist = rlist)

def test():
    filename = request.args[0]
    book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
    p = Book(book_file)
    info = p.book_info()

    pprint.pprint(info)

    ls = []

    title = info['book']['title']
    ls.append(H1(title))
    for version in info['version']:
        d = DIV()
        d.append(H2('Version'))
        d.append(DIV(H3('Attributes'), version['attributes']))
        d.append(DIV(H3('Organization levels'), version['organisation_levels']))
        d.append(DIV(H3('Divisions'), version['divisions']))
        d.append(DIV(H3('Resources'), version['resources']))
        d.append(DIV(H3('Manuscripts'), version['manuscripts']))
        d.append(DIV(H3('Text structure')))
        for k, v in version['text_structure'].items():
            d.append(H4(k))

        #for key, value in version.items():
            #if key != 'text_structure':
                #print 'Version', key, '-->', value

            #else:
                #print 'Version textstructure'
                #for ref, ref_val in value.items():
                    #for unit, unit_val in ref_val.items():
                        #for mss, mss_val in unit_val.items():
                            #print '\t', ref, '-->', unit, '-->', mss, '-->', mss_val

        ls.append(d)

    return dict(info = info, ls = ls)
