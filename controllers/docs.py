# coding: utf8
from lxml import etree

from parse import BookParser

import pprint
import inspect

import re

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
    #print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    print 'start of section() method with url ', request.url, varlist
    #get filename from end of url and parse the file with BookParser class
    filename = request.args[0]
    print 'filename: ', filename
    book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
    p = BookParser(book_file)
    info = p.book_info()
    #get title of document
    title = info['title']

    #get names of all versions of current doc and select the version to display
    versions = [version['title'] for version in info['versions']]     
    if 'version' in request.vars:
        current_version = request.vars['version'].replace('_', ' ')
        #move selected version to top of list for selectbox
        i = versions.index(current_version)
        versions.insert(0, versions.pop(i))
        print 'current version: ', current_version.replace(' ', '&nbsp;')
    else:
        current_version = versions[0]
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

    #build hierarchical dict of references
    reflist = [ref for ref, units in curv['text_structure'].items()]

    #build list for starting ref
    if 'from' in request.vars:
        from_input = request.vars['from']
        start_sel = from_input.split('-')
        del start_sel[-1]
        print 'using url ref'
    else:
        firstref = reflist[0]
        firstref_parts = re.split('[:\.,;_-]', firstref)
        start_sel = [firstref_parts[l] for l in range(levels)]
        print 'using default first ref'

    #build list for ending ref
    if 'to' in request.vars:                
        to_input = request.vars['to']
        end_sel = to_input.split('-')
        del end_sel[-1]
    else:
        end_sel = start_sel
    print 'start_sel', start_sel
    print 'end_sel', end_sel
    #gather text from units within the selected section of the doc
    #filters the current version for only readings in the current
    #text type
    sel_text = []
    print 'matching text in: '
    for ref, units in curv['text_structure'].items():
        ref_parts = re.split('[:\.,;_-]', ref)
        if int(ref_parts[0]) >= int(start_sel[0]) and int(ref_parts[0]) <= int(end_sel[0]):
                
                sel_text.append(SPAN(ref, _class = 'ref'))
                for unit_ref, unit_val in units.items():
                    for mss, raw_text in unit_val.items():
                        if current_ms[-1] != ' ':
                            current_ms += ' '
                        if current_ms in (mss + ' '):
                            if len(units) > 1:
                                sel_text.append(A(raw_text, _class = vlang, _href=unit_ref))
                            else:
                                sel_text.append(SPAN(raw_text, _class = vlang))
                        else:
                            pass
    for s in sel_text:
        print s[0]

    return dict(title = title, versions = versions, current_version = current_version,
                info = info, filename = filename, mslist = mslist, sel_text = sel_text,
                levels = levels, start_sel = start_sel, end_sel = end_sel)


def apparatus():
    filename = request.args[0]
    book_file = 'applications/grammateus3/static/docs/%s.xml' % filename
    p = BookParser(book_file)
    info = p.book_info()

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
