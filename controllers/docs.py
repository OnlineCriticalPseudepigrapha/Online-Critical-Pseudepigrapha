#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

from collections import OrderedDict
from kitchen.text.converters import to_unicode
from parse import Book, ElementDoesNotExist, NotAllowedManuscript
import cPickle
from plugin_utils import flatten
from pprint import pprint
import re
import traceback

if 0:
    from gluon import current, URL, A, SPAN, P, BR, redirect
    auth = current.auth
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

DISPLAY_FIELDS = OrderedDict([('introduction', 'Introduction'),
                              ('provenance', 'Provenance and '
                                             'Cultural Setting'),
                              ('themes', 'Major Themes'),
                              ('status', 'Current State of the OCP Text'),
                              ('manuscripts', 'Manuscripts'),
                              ('bibliography', 'Bibliography'),
                              ('corrections', 'Corrections'),
                              ('sigla', 'Sigla Used in the Text'),
                              ('copyright', 'Copyright Information')]
                             )


def index():
    filename = request.args[0]
    return dict(filename=filename)


@auth.requires_membership('administrators')
def create_draft_intro():
    """
    Controller to create a new draft doc intro and redirect to draft_intro
    controller.
    """
    filename = request.args[0]
    published_intro = db(db.docs.filename == filename).select().first()
    if published_intro:
        db['draftdocs'].insert(**published_intro.as_dict())
        db.commit()
    else:
        default_vals = {'filename': filename,
                        'name': 'Document title here',
                        'introduction': 'Provide a brief overview of the '
                                        ' document\'s nature and importance.',
                        'provenance': 'Discuss the date, geographical '
                                      'location, and cultural situation '
                                      'of composition. This is also the '
                                      'place to discuss translation '
                                      'history and the relationship '
                                      'between various text types.',
                        'themes': 'Discuss the document\'s major themes.',
                        'status': 'Discuss the current status of the OCP '
                                  'edition of the text. You should point out '
                                  'whether, e.g., a better eclectic text '
                                  'exists elsewhere, or whether there are '
                                  'manuscripts or text types that are not '
                                  'included here.',
                        'manuscripts': 'Provide a list of all extant '
                                       'manuscripts, including their official '
                                       'designations, their current location '
                                       '(the institution where they are '
                                       'held), their date of copying, and any '
                                       'print editions of the manuscript in '
                                       'running form. If some mss do not '
                                       'contain the full document, specify '
                                       'which parts of the document are '
                                       'contained in each. '
                                       'Note that this list will be converted '
                                       'to a table by the OCP general '
                                       'editors.',
                        'bibliography': 'Provide a bibliography of all '
                                        'published editions of the text. It '
                                        'would be helpful to annotate the '
                                        'list, indicating the quality '
                                        'and distinctive features of each '
                                        'edition. If multiple text types or '
                                        'language traditions have different '
                                        'publication histories, provide '
                                        'a heading and separate bibliography '
                                        'for each.',
                        'corrections': 'If you have found errors in existing '
                                       'print editions these can be presented '
                                       ' here in a list.',
                        'sigla': 'List here each symbol used in the text '
                                 'along with a brief description of its '
                                 'meaning. Standard punctuation need not be '
                                 'listed, but even common text-critical '
                                 'symbols (like square brackets, ellipses, or '
                                 'circles/dots above a character) should be '
                                 'included.',
                        'copyright': 'Explain here, as best you understand '
                                     'it, the copyright status of each text '
                                     'type included in the OCP edition of '
                                     'your text. If you have question about '
                                     'copyright issues, feel free to ask the '
                                     'OCP general editors.',
                        'version': '0.1'
                        }
        db['draftdocs'].insert(**default_vals)
        db.commit()
    redirect(URL('draft_intro', args=[filename]))


@auth.requires_login()
def update_draft_intro():
    """
    """
    filename = request.vars['filename']

    mytext = request.vars['text']
    mysection = request.vars['section']
    myfield_title = [f for f in DISPLAY_FIELDS.keys()
                     if DISPLAY_FIELDS[f] == mysection][0]
    new_content = {myfield_title: mytext}

    db(db.draftdocs.filename == filename).update(**new_content)
    db.commit()

    return 'Success!'


@auth.requires_login()
def draft_intro():
    """
    Controller for presenting draft versions of document introductions.
    """
    response.files.append(URL('static/js/codemirror/lib', 'codemirror.js'))
    response.files.append(URL('static/js/codemirror/lib', 'codemirror.css'))
    response.files.append(URL('static/js/codemirror/theme', 'solarized.css'))
    response.files.append(URL('static/js/codemirror/mode/xml', 'xml.js'))
    response.files.append(URL('static/js/summernote', 'summernote.min.js'))
    response.files.append(URL('static/js/summernote', 'summernote.css'))
    session.filename = request.args[0]
    filename = session.filename
    docrow = db(db.draftdocs.filename == filename).select().first()
    if not docrow:
        # draft document does not exist in the database, so can't be edited
        return {'doc_exists': False,
                'editing_permission': False,
                'filename': filename}

    else:
        # draft document does exist in database and can be edited
        editor_ids = [docrow['editor'], docrow['editor2'], docrow['editor3'],
                      docrow['editor4'], docrow['assistant_editor'],
                      docrow['assistant_editor2'], docrow['assistant_editor3'],
                      docrow['proofreader'], docrow['proofreader2'],
                      docrow['proofreader3']
                      ]
        if auth.has_membership('administrators') \
                or (auth.has_membership('editors')
                    and auth.user_id in editor_ids):
            # current user has permission to edit this page
            body_fields = OrderedDict([(v, docrow[k]) for k, v
                                       in DISPLAY_FIELDS.iteritems()
                                       if docrow[k]])

            editor_names = OrderedDict([])
            for ed in ['editor', 'editor2', 'editor3', 'editor4']:
                if docrow[ed]:
                    editor_names[docrow[ed]['id']] = '{} {}'.format(
                        docrow[ed]['first_name'], docrow[ed]['last_name'])

            asst_editor_names = OrderedDict([])
            for ed in ['assistant_editor',
                       'assistant_editor2',
                       'assistant_editor3']:
                if docrow[ed]:
                    asst_editor_names[docrow[ed]['id']] = '{} {}'.format(
                        docrow[ed]['first_name'], docrow[ed]['last_name'])

            proofreader_names = OrderedDict([])
            for ed in ['proofreader', 'proofreader2', 'proofreader3']:
                if docrow[ed]:
                    proofreader_names[docrow[ed]['id']] = '{} {}'.format(
                        docrow[ed]['first_name'], docrow[ed]['last_name'])

            return {'doc_exists': True,
                    'editing_permission': True,
                    'title': docrow['name'],
                    'body_fields': body_fields,
                    'citation_format': docrow['citation_format'],
                    'editors': editor_names,
                    'assistant_editors': asst_editor_names,
                    'proofreaders': proofreader_names,
                    'filename': filename,
                    'version': docrow['version']}
        else:
            # current user does not have permission
            return {'doc_exists': True,
                    'editing_permission': False,
                    'filename': filename,
                    'title': docrow['name']}


def intro():
    session.filename = request.args[0]
    filename = session.filename
    docrow = db(db.docs.filename == filename).select().first()

    display_fields = OrderedDict([('introduction', 'Introduction'),
                                  ('provenance',
                                   'Provenance and Cultural Setting'),
                                  ('themes', 'Major Themes'),
                                  ('status', 'Current State of the OCP Text'),
                                  ('manuscripts', 'Manuscripts'),
                                  ('bibliography', 'Bibliography'),
                                  ('corrections', 'Corrections'),
                                  ('sigla', 'Sigla Used in the Text'),
                                  ('copyright', 'Copyright Information')]
                                 )
    body_fields = OrderedDict([(v, docrow[k]) for k, v
                               in display_fields.iteritems() if docrow[k]])

    editor_names = OrderedDict([])
    for ed in ['editor', 'editor2', 'editor3', 'editor4']:
        if docrow[ed]:
            myrow = docrow[ed][0] if type(docrow[ed]) is list else docrow[ed]
            if myrow:
                editor_names[myrow['id']] = '{} {}'.format(
                    myrow['first_name'], myrow['last_name'])

    asst_editor_names = OrderedDict([])
    for ed in ['assistant_editor', 'assistant_editor2', 'assistant_editor3']:
        if docrow[ed]:
            myrow = docrow[ed][0] if type(docrow[ed]) is list else docrow[ed]
            if myrow:
                asst_editor_names[myrow['id']] = '{} {}'.format(
                    myrow['first_name'], myrow['last_name'])

    proofreader_names = OrderedDict([])
    for ed in ['proofreader', 'proofreader2', 'proofreader3']:
        if docrow[ed]:
            myrow = docrow[ed][0] if type(docrow[ed]) is list else docrow[ed]
            if myrow:
                proofreader_names[myrow['id']] = '{} {}'.format(
                    myrow['first_name'], myrow['last_name'])

    return {'title': docrow['name'],
            'body_fields': body_fields,
            'citation_format': docrow['citation_format'],
            'editors': editor_names,
            'assistant_editors': asst_editor_names,
            'proofreaders': proofreader_names,
            'filename': filename,
            'version': docrow['version']}


def text():
    """
    Gather document information to prepare initial reader interface.
    """
    vbs = True
    if vbs: print("text() start -------------------------------------")
    session.filename = request.args[0]
    filename = session.filename
    if vbs: print('filename: ', filename)
    # TODO: provide fallback and prompt if no filename is given in url

    # url to pass to web2py load helper in view to load doc section via ajax
    load_url = URL('docs', 'section.load', args=filename)

    # print url input for debugging purposes
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]
    if vbs: print('start of text() method with url ', request.url, varlist)

    # get parsed document info
    info, p = _get_bookinfo(filename)

    # get title of document
    title = info['book']['title']
    # get structure type for document
    structure = info['book']['textStructure']
    if session.structure:
        session.structure[filename] = structure
    else:
        session.structure = {filename: structure}

    # get names of all versions of current doc
    versions = info['version']

    if structure == 'fragmentary':  # find first fragment and set nav values
        fragments = sorted(list(set([v['attributes']['fragment'] for v
                                     in versions])))
        session.versions = {f: [v['attributes']['title'] for v in versions
                                if v['attributes']['fragment'] == f]
                            for f in fragments}

        levels = None
        start_sel = fragments[0]
        start_sel_str = fragments[0]
        end_sel = start_sel
        end_sel_str = start_sel_str

        if session.refraw:
            session.refraw[filename] = None
        else:
            session.refraw = {filename: None}

    else:  # find start/end refs for first text section and set nav values
        session.versions = [v['attributes']['title'] for v in versions]
        first_v = versions[0]
        delimiters = first_v['divisions']['delimiters']
        levels = first_v['organisation_levels']

        # build flat list of references
        refraw = first_v['reference_list']
        if session.refraw:
            session.refraw[filename] = refraw
        else:
            session.refraw = {filename: refraw}

        # build list for starting ref
        if 'from' in request.vars:
            start_sel = request.vars['from'][:-1]
            start_sel = re.split('-', start_sel)
            # create string ref with proper delimiters
            startlist = [None] * (len(start_sel) + len(levels))
            startlist[::2] = start_sel
            startlist[1::2] = delimiters
            startref = ''.join(startlist)
            if vbs: print('text(): using url ref ', start_sel)
        else:
            startref = refraw[0]
            start_sel = re.split('[:\.,;_-]', startref)
            if vbs: print('text(): using default first ref ', start_sel)

        # build list for ending ref
        if 'to' in request.vars:
            end_sel = request.vars['to'][:-1]
            end_sel = re.split('-', end_sel)
            # create string ref with proper delimiters
            endlist = [None] * (len(end_sel) + len(levels))
            endlist[::2] = end_sel
            endlist[1::2] = delimiters
            endref = ''.join(endlist)
        else:
            if vbs: print('start_sel', start_sel)
            if vbs: print('delimiters', delimiters)
            my_delimiter = delimiters[0] if len(delimiters) else ''
            regex = re.compile('^' + start_sel[0] + my_delimiter)
            # find all refs with the same top-level reference
            this_div = [ref for ref in refraw if regex.match(ref)]
            # choose the last one
            endref = this_div[-1]
            end_sel = re.split('[:\.,;_-]', endref)

        session.startref = startref
        session.endref = endref
        start_sel_str = '|'.join(start_sel),
        end_sel_str = '|'.join(end_sel),

    return {'load_url': load_url,
            'title': title,
            'levels': levels,
            'start_sel': start_sel,
            'start_sel_str': start_sel_str,
            'end_sel': end_sel,
            'end_sel_str': end_sel_str,
            'filename': filename,
            'structure': structure}


def _get_bookinfo(filename):
    """
    Retrieve info about the book and parsed book object from session or parser.

    """
    vbs = False
    # FIXME: error when using session values
    # _element object can't be pickled, and pickling is necessary to store
    # an object in session
    print("Getting info")
    if 0 and ('p' in session.keys()) and (filename in session.p.keys()):
        p = cPickle.loads(session.p[filename])
    else:
        book_file = 'applications/grammateus3/static/docs/' \
                    '{}.xml'.format(filename)
        p = Book(book_file)
        if session.p:
            session.p[filename] = p
        else:
            session.p = {filename: p}

    if ('info' in session.keys()) and (filename in session.info.keys()):
        info = session.info[filename]
    else:
        info = p.get_book_info()
        session.info = {filename: info}
    if vbs: print("info", pprint(info))
    return info, p


"""
deprecated

def _make_refs_hierarchical(refraw, levels):
    '''
    Convert flat list of formatted references into hierarchically nested dicts.

    '''
    vbs = False

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
        childicts = OrderedDict([(l[1], OrderedDict()) for l
        in flatlists if l[0] == num])
        hierarch[num] = childicts
        if levels > 2:
            for key, val in hierarch[num]:
                mydict3 = OrderedDict([(l[2], OrderedDict()) for l in flatlists
                                      if l[0] == num and l[1] == key])
                hierarch[num][key] = mydict3
                if levels > 3:
                    for key3, val3 in hierarch[num][key]:
                        mydict4 = OrderedDict([(l[3], OrderedDict())
                        for l in flatlists
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
    Populate single text pane via the section.load view (refreshable via ajax)

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
    # 'vbs' variable is for turning testing output on and off
    vbs = False
    if vbs: print('section() start ------------------------------------------')
    varlist = [(str(k) + ':' + str(v)) for k, v in request.vars.items()]

    # get filename from end of url and parse the file with BookParser class
    filename = request.args[0]
    info, p = _get_bookinfo(filename)

    def get_version_info(current_version):
        for version in info['version']:
            if version['attributes']['title'] == current_version:
                    curv = version
                    vlang = curv['attributes']['language']
                    levels = curv['organisation_levels']
        mslist = flatten([[to_unicode(k.strip()) for k, c in v.iteritems()
                           if c['attributes']['show'] == 'yes']
                          for v in curv['manuscripts']])

        return curv, vlang, levels, mslist

    def get_current_ms(mslist):
        # use the third url argument as manuscript name if present, otherwise
        # default to first version
        # check for 'newval' value, indicating the version has changed
        if 'type' in request.vars and request.vars['type'] != 'newval':
            current_ms = request.vars['type'].replace('_', ' ')
            current_ms = current_ms.strip()
            if vbs: print('current_ms: ', current_ms)
            # move selected text type to top of list for ms selectbox
            i = mslist.index(to_unicode(current_ms))
            mslist.insert(0, mslist.pop(i))
        else:
            current_ms = mslist[0]

        return current_ms

    def get_prev_next_levels(startref, endref, start_sel, end_sel):
        # handle 'next' and 'previous' navigation via 'endref' values
        # numbers indicate org. level at which to move forward or back
        vbs = False
        next_level = None
        if endref[:4] == 'next':
            next_level = int(endref[4:])  # expects like next2
            end_sel = start_sel
            if vbs: print('next_level:', next_level)
        previous_level = None
        if endref[:4] == 'back':
            previous_level = int(endref[4:])  # expects like previous2
            end_sel = start_sel
            if vbs: print('previous_level:', previous_level)

        return next_level, previous_level, end_sel

    def get_display_version(myversions):
        # select the version to display
        try:
            if 'version' in request.vars:
                current_version = request.vars['version'].replace('_', ' ')
                # move selected version to top of list for selectbox
                if myversions and current_version in myversions:
                    i = myversions.index(current_version)
                    myversions.insert(0, myversions.pop(i))
                else:
                    current_version = myversions[0]
                if vbs: print('current version: ',
                              current_version.replace(' ', '&nbsp;'))
            else:
                current_version = myversions[0]
                if vbs: print('current version: ',
                              current_version.replace(' ', '&nbsp;'))
        except Exception:
            traceback.print_exc(5)
        return current_version, myversions

    myfrag = None  # default value for non-fragmentary texts

    # FRAGMENTARY ==========================================================
    if session.structure[filename] == 'fragmentary':
        myfrags = sorted(session.versions.keys())
        myfrag = myfrags[0] if not request.vars['from'] \
            else request.vars['from'].replace('-', '')

        # handle 'next' and 'back' navigation
        try:
            mydir = request.vars['to'][:4]
        except TypeError:  # because to is None
            pass
        if 'mydir' in locals() and mydir in ['next', 'back']:
            dirs = {'next': 1, 'back': -1}
            fidx = myfrags.index(myfrag) + dirs[mydir]
            if fidx < 0:
                fidx = 0
            elif fidx > (len(myfrags) - 1):
                fidx = len(myfrags) - 1
            myfrag = myfrags[fidx]

        myversions = session.versions[myfrag]
        current_version, myversions = get_display_version(myversions)
        curv, vlang, levels, mslist = get_version_info(current_version)
        current_ms = get_current_ms(mslist)

        if session.refraw[filename]:
            reflist = session.refraw[filename]
        else:
            reflist = curv['reference_list']
            session.refraw[filename] = reflist

        startref = reflist[0]
        start_sel = startref.split(':')
        endref = reflist[-1]
        end_sel = endref.split(':')

    # NON-FRAGMENTARY =========================================================
    else:
        myversions = session.versions
        current_version, myversions = get_display_version(myversions)
        curv, vlang, levels, mslist = get_version_info(current_version)
        current_ms = get_current_ms(mslist)

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

    next_level, previous_level, end_sel = get_prev_next_levels(startref,
                                                               endref,
                                                               start_sel,
                                                               end_sel)

    try:
        # re-set start_sel and end_sel from output in case 'next' or 'back'
        myargs = [current_version,
                  current_ms,
                  start_sel,
                  end_sel,
                  next_level,
                  previous_level]
        text_iterator, start_sel, end_sel = p.get_text(*myargs)
        parsed_text = list(text_iterator)
    except ElementDoesNotExist as e:
        try:
            print(traceback.format_exc())
            myparams = [current_version, current_ms + ' ',
                        start_sel, end_sel]
            myvars = {"next_level": next_level,
                      "previous_level": previous_level}
            text_iterator, start_sel, end_sel = p.get_text(*myparams, **myvars)
            parsed_text = list(text_iterator)
        except ElementDoesNotExist as e:
            print(traceback.format_exc())
            response.flash = 'Sorry, no text matched the selected range.'
    except NotAllowedManuscript as e:
        print(traceback.format_exc())
        response.flash = 'Sorry, that text type is not part of the {} ' \
                         'version'.format(current_version)

    # build the running display text ----------------------------------------
    mytext = []
    refcounter = [None] * levels
    if vbs: print('PARSED =============================')
    if vbs: print(parsed_text)
    for u in parsed_text:
        # insert reference number/label when it changes
        reflist = list(u.div_path)
        for idx, r in enumerate(reflist):
            if refcounter[idx] == r:
                pass
            else:
                mytext.append(SPAN(' {} '.format(unicode(r)),
                                   _class='refmarker refmarker_{}'.format(idx))
                              )
                refcounter[idx] = r
        punctuation = [u'.', u';', u'·', u'"', u"'", u',', u'?', u'«', u'»',
                       u'·']
        if u.text == '':
            mytext.append(A(u' *', _class='placeholder', _href=u.unit_id))
        elif u.readings_in_unit > 1:
            if u.text not in punctuation and u.language not in ['Ethiopic']:
                mytext.append(u' ')
            mytext.append(A(u.text, _class=u.language, _href=u.unit_id))
        else:
            if u.text not in punctuation and u.language not in ['Ethiopic']:
                mytext.append(u' ')
            mytext.append(SPAN(u.text, _class=u.language))
        try:
            if u.linebreak == 'following':
                mytext.append(BR())
            if u.linebreak == 'doubleFollowing':
                mytext.append(BR())
                mytext.append(BR())
        except Exception as e:
            print('LINEBREAK PROBLEM')
            print(e)

    if vbs: print('sending', '-'.join(start_sel))

    return {'versions': myversions,
            'current_version': current_version,
            'version_language': vlang,
            'mslist': mslist,
            'start_sel_str': '|'.join(start_sel),
            'end_sel_str': '|'.join(end_sel),
            'fragment': myfrag,
            'sel_text': mytext,
            'filename': session.filename,
            'structure': session.structure[filename]}


def apparatus():
    vbs = False
    if vbs: print('starting apparatus controller')
    filename = request.args[0]
    info, p = _get_bookinfo(filename)

    # if no unit has been requested, present the default message
    if request.vars['called'] == 'no':
        readings = P('Click on any blue text to display textual variants '
                     'for those words. If no links are available that may '
                     'mean no variants are attested or it may mean that '
                     'this document does not yet have a complete textual '
                     'apparatus. See the document introduction for details.',
                     _class='apparatus-message')
        current_version = ''
    # if a unit has been requested, assemble that unit's readings
    else:
        # get current version
        current_version = request.vars['version'].replace('_', ' ')
        unit = request.vars['unit']
        readings = p.get_readings(current_version, unit)

    return {'rlist': readings,
            'version': current_version}
