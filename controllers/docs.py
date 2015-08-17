# -*- coding: utf-8 -*-

from collections import OrderedDict
from parse import Book, ElementDoesNotExist, NotAllowedManuscript
from plugin_utils import flatten
import re
import traceback

if 0:
    from gluon import current, URL, A, SPAN, P
    request = current.request
    session = current.session
    response = current.response
    db = current.db

"""
List of session objects used in text display:
session.filename
session.info -- dict; parsed results of BookParser class for current doc
session.title -- string; title of current doc
session.versions -- list; names of all versions in current doc
session.refraw -- list; flast list of formatted references in the first version
session.refhierarch -- OrderedDict;
session.startref --
session.endref --
"""


def index():
    filename = request.args[0]
    return dict(filename=filename)


def intro():
    session.filename = request.args[0]
    filename = session.filename
    docrow = db(db.docs.filename == filename).select().first()

    display_fields = OrderedDict([('introduction', 'Introduction'),
                                  ('provenance', 'Provenance and Cultural Setting'),
                                  ('themes', 'Major Themes'),
                                  ('status', 'Current State of the OCP Text'),
                                  ('manuscripts', 'Manuscripts'),
                                  ('bibliography', 'Bibliography'),
                                  ('corrections', 'Corrections'),
                                  ('sigla', 'Sigla Used in the Text'),
                                  ('copyright', 'Copyright Information')]
                                 )
    body_fields = OrderedDict([(v, docrow[k]) for k, v in display_fields.iteritems()
                               if docrow[k]])

    editors = db(db.auth_user.id.belongs(docrow['editor'])).select()
    editor_names = OrderedDict([(e['id'], '{} {}'.format(e['first_name'], e['last_name']))
                    for e in editors])

    asst_editors = db(db.auth_user.id.belongs(docrow['assistant_editor'])).select()
    asst_editor_names = OrderedDict([(e['id'], '{} {}'.format(e['first_name'], e['last_name']))
                    for e in asst_editors])

    proofreaders = db(db.auth_user.id.belongs(docrow['proofreader'])).select()
    proofreader_names = OrderedDict([(e['id'], '{} {}'.format(e['first_name'], e['last_name']))
                    for e in proofreaders])

    return {'title': docrow['name'],
            'body_fields': body_fields,
            'citation_format': docrow['citation_format'],
            'editors': editor_names,
            'assistant_editors': asst_editor_names,
            'proofreaders': proofreader_names,
            'filename': filename,
            'version': docrow['version']}


def text():
    vbs = False
    session.filename = request.args[0]
    filename = session.filename
    if vbs: print 'filename: ', filename
    #TODO: provide fallback and prompt if no filename is given in url

    #url to pass to web2py load helper in view to load doc section via ajax
    load_url = URL('docs', 'section.load', args=filename)

    #print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    if vbs: print 'start of text() method with url ', request.url, varlist

    # get parsed document info
    info, p = _get_bookinfo(filename)

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
    print 'end_sel', end_sel, '\n\n'

    return {'load_url': load_url,
            'title': title,
            'levels': levels,
            'start_sel': start_sel,
            'start_sel_str': '|'.join(start_sel),
            'end_sel': end_sel,
            'end_sel_str': '|'.join(end_sel),
            'filename': filename}


def _get_bookinfo(filename):
    """
    Retrieve info about the book and parsed book object from session or parser.

    """
    vbs = False
    # FIXME: error when using session values
    if 0 and ('info' in session.keys()) and (filename in session.info.keys()) and \
            ('p' in session.keys()) and (filename in session.p.keys()):
        info = session.info[filename]
        p = session.p[filename]
        if vbs: print 'using session.info'
    else:
        book_file = 'applications/grammateus3/static/docs/{}.xml'.format(filename)
        p = Book.open(book_file)
        if session.p:
            session.p[filename] = p
        else:
            session.p = {filename: p}
        info = p.book_info()
        session.info = {filename: info}
    return info, p


"""
deprecated

def _make_refs_hierarchical(refraw, levels):
    '''
    Convert flat list of formatted references into hierarchically nested dicts.

    '''
    vbs = True

    def uniq(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    flatlists = [re.split('[:\.,;_-]', r) for r in refraw]
    if vbs: print flatlists, '\n'
    hierarch = OrderedDict()
    topnums = uniq([l[0] for l in flatlists])
    if vbs: print 'topnums', topnums, '\n'
    for num in topnums:
        childicts = OrderedDict([(l[1], OrderedDict()) for l in flatlists if l[0] == num])
        hierarch[num] = childicts
        if levels > 2:
            for key, val in hierarch[num]:
                mydict3 = OrderedDict([(l[2], OrderedDict()) for l in flatlists
                                      if l[0] == num and l[1] == key])
                hierarch[num][key] = mydict3
                if levels > 3:
                    for key3, val3 in hierarch[num][key]:
                        mydict4 = OrderedDict([(l[3], OrderedDict()) for l in flatlists
                                              if l[0] == num
                                              and l[1] == key
                                              and l[2] == key3])
                        hierarch[num][key][key3] = mydict4
    if vbs: print 'hierarch ------------------------------------------------'
    if vbs: pprint(hierarch)
    return hierarch
"""


def section():
    """
    Populates a single text pane via the section.load view (refreshable via ajax)

    The text is returned by the get_text() generator method as a series of Text
    objects. Converted to a list, the generated output looks like:

        [Text(div_path=('Title', '0'),
            unit_id='1',
            language='Greek',
            readings_in_unit=4,
            linebreak='',
            indent='',
            text=u'\u0394\u03b9\u03b1\u03b8\u1f75\u03ba\u03b7 '),
        Text(div_path=('Title', '0'),
            unit_id='2',
            language='Greek',
            readings_in_unit=2,
            linebreak='',
            indent='',
            text='')]

    """
    #'vbs' variable is for turning testing output on and off
    vbs = True
    #print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    if vbs: print '\n\nstart of section() method with url ', request.url, varlist

    #get filename from end of url and parse the file with BookParser class
    filename = request.args[0]
    info, p = _get_bookinfo(filename)

    #select the version to display
    if 'version' in request.vars:
        current_version = request.vars['version'].replace('_', ' ')
        #move selected version to top of list for selectbox
        if 'versions' in session:
            i = session.versions.index(current_version)
            session.versions.insert(0, session.versions.pop(i))
        if vbs: print 'current version: ', current_version.replace(' ', '&nbsp;')
    else:
        current_version = session.versions[0]
        if vbs: print 'current version: ', current_version.replace(' ', '&nbsp;')

    #find selected version in parsed text
    for version in info['version']:
        if version['attributes']['title'] == current_version:
                curv = version
                vlang = curv['attributes']['language']
                levels = curv['organisation_levels']
    #get list of mss
    mslist = flatten([[k.strip() for k, c in v.iteritems()]
                      for v in curv['manuscripts']])
    #use the third url argument as manuscript name if present, otherwise
    #default to first version
    #check for 'newval' value, indicating the version has changed
    if 'type' in request.vars and request.vars['type'] != 'newval':
        current_ms = request.vars['type'].replace('_', ' ')
        current_ms = current_ms.strip()
        if vbs: print 'current_ms: ', current_ms
        #move selected text type to top of list for ms selectbox
        i = mslist.index(current_ms)
        mslist.insert(0, mslist.pop(i))
    else:
        current_ms = mslist[0]

    #gather text from units within the selected section of the doc
    #filters the current version for only readings in the current
    #text type

    if 'from' in request.vars:
        startref = request.vars['from']
        start_sel = [s for s in startref.split('-') if s]
        if 'to' in request.vars:
            endref = request.vars['to']
            end_sel = [s for s in endref.split('-') if s]

        else:
            end_sel = start_sel

    else:
        reflist = session.refraw
        startref = session.startref
        start_sel = startref.split(':')
        endref = session.endref
        end_sel = endref.split(':')

    mytext = []

    # handle 'next' and 'previous' navigation via 'endref' values
    # numbers indicate organizational level at which to move forward or back
    next_level = None
    if endref[:4] == 'next':
        next_level = int(endref[4:])  # expects like next2
        end_sel = start_sel
        print 'next_level:', next_level
    previous_level = None
    if endref[:4] == 'back':
        previous_level = int(endref[4:])  # expects like previous2
        end_sel = start_sel
        print 'previous_level:', previous_level

    try:
        # re-set start_sel and end_sel from output in case 'next' or 'back'
        text_iterator, start_sel, end_sel = p.get_text(current_version,
                                                       current_ms, start_sel,
                                                       end_sel,
                                                       next_level=next_level,
                                                       previous_level=previous_level)
        parsed_text = list(text_iterator)
    except ElementDoesNotExist, e:
        try:
            print traceback.format_exc()
            text_iterator, start_sel, end_sel = p.get_text(current_version,
                                                           current_ms + ' ',
                                                           start_sel,
                                                           end_sel,
                                                           next_level=next_level,
                                                           previous_level=previous_level)
            parsed_text = list(text_iterator)
        except ElementDoesNotExist, e:
            print traceback.format_exc()
            response.flash = 'Sorry, no text matched the selected range.'
    except NotAllowedManuscript, e:
        print traceback.format_exc()
        response.flash = 'Sorry, that text type is not part of the {} version' \
                         ''.format(current_version)

    # build the running display text ----------------------------------------
    refcounter = [None] * levels
    for u in parsed_text:
        # insert reference number/label when it changes
        reflist = list(u.div_path)
        for idx, r in enumerate(reflist):
            if refcounter[idx] == r:
                pass
            else:
                mytext.append(SPAN(' {}'.format(unicode(r)),
                                   _class='refmarker_{}'.format(idx)))
                refcounter[idx] = r
        punctuation = [u'.', u';', u'·', u'"', u"'", u',', u'?', u'«', u'»', u'·']
        if u.text == '':
            mytext.append(A(u' *', _class='placeholder', _href=u.unit_id))
        elif u.readings_in_unit > 1:
            if u.text not in punctuation:
                mytext.append(u' ')
            mytext.append(A(u.text, _class=u.language, _href=u.unit_id))
        else:
            if u.text not in punctuation:
                mytext.append(u' ')
            mytext.append(SPAN(u.text, _class=u.language))

    print 'sending', '-'.join(start_sel)

    return {'versions': session.versions,
            'current_version': current_version,
            'mslist': mslist,
            'start_sel_str': '|'.join(start_sel),
            'end_sel_str': '|'.join(end_sel),
            'sel_text': mytext,
            'filename': session.filename}


def apparatus():
    print 'starting apparatus controller'
    filename = request.args[0]
    info, p = _get_bookinfo(filename)

    #if no unit has been requested, present the default message
    if request.vars['called'] == 'no':
        readings = P('Click on any blue text to display textual variants '
                        'for those words. If no links are available that may '
                        'mean no variants are attested or it may mean that '
                        'this document does not yet have a complete textual '
                        'apparatus. See the document introduction for details.',
                     _class='apparatus-message')
    #if a unit has been requested, assemble that unit's readings
    else:
        #get current version
        current_version = request.vars['version'].replace('_', ' ')
        unit = request.vars['unit']
        readings = p.get_readings(current_version, unit)

    return {'rlist': readings}
