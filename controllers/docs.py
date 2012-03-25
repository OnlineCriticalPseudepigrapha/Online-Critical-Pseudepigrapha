# coding: utf8
from lxml import etree
from parse import Book
import pprint, inspect, re

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
    title = info['title']

    #get names of all versions of current doc
    session.versions = [version['title'] for version in info['versions']]     
    first_version = info['versions'][0]
    delimiters = first_version['delimiters']

    levels = first_version['organisation_levels']

    #build flat list of references
    refraw = [ref for ref, units in first_version['text_structure'].items()]   
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
    #print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    print 'start of section() method with url ', request.url, varlist
    #get filename from end of url and parse the file with BookParser class
    filename = request.args[0]
    print 'filename: ', filename
    if ('info' in session) and (filename in session.info):
        info = session.info[filename]
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
        i = session.versions.index(current_version)
        session.versions.insert(0, versions.pop(i))
        print 'current version: ', current_version.replace(' ', '&nbsp;')
    else:
        current_version = session.versions[0]
        print 'current version: ', current_version.replace(' ', '&nbsp;')

    #find selected version in parsed text
    for version in info['versions']:
        for k, v in version.items():
            if k == 'title' and v == current_version:
                curv = version
                vlang = curv['language']
                levels = curv['organisation_levels']
            else:
                pass

    #get list of mss
    mslist = [k.strip() for k, v in curv['manuscript'].items()]
    print 'mslist for this version: ', mslist
    #use the third url argument as manuscript name if present, otherwise default to first version
    #check for 'newval' value, indicating the version has changed
    if 'type' in request.vars and request.vars['type'] != 'newval':
        current_ms = request.vars['type'].replace('_', ' ')
        current_ms = current_ms.strip()
        print 'current_ms: ', current_ms
        #move selected text type to top of list for ms selectbox
        i = mslist.index(current_ms)
        mslist.insert(0, mslist.pop(i))        
    else:
        current_ms = mslist[0]
        print 'current_ms: ', current_ms

    #gather text from units within the selected section of the doc
    #filters the current version for only readings in the current
    #text type
    reflist = session.refraw
    startref = session.startref
    endref = session.endref

    sel_text = []
    print 'matching text in: '
    startIndex = reflist.index(startref)
    endIndex = reflist.index(endref)

    for ref, units in curv['text_structure'].items():
        if (reflist.index(ref) >= reflist.index(startref)) and \
            (reflist.index(ref) <= reflist.index(endref)):
        #ref_parts = re.split('[:\.,;_-]', ref)
        #if int(ref_parts[0]) >= int(start_sel[0]) and int(ref_parts[0]) <= int(end_sel[0]):                
                sel_text.append(SPAN(ref, _class = 'ref'))
                for unit_ref, unit_val in units.items():
                    for mss, raw_text in unit_val.items():
                        if current_ms[-1] != ' ':
                            current_ms += ' '
                        if current_ms in (mss + ' '):
                            if len(unit_val) > 1:
                                sel_text.append(A(raw_text, _class = vlang, _href=unit_ref))
                            else:
                                sel_text.append(SPAN(raw_text, _class = vlang))
                            print 'unit_val length: ', len(unit_val)
                            print unit_val
                        else:
                            pass
    for s in sel_text:
        print s[0]

    return dict(versions = session.versions, current_version = current_version,
                mslist = mslist, sel_text = sel_text, filename = session.filename)


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
