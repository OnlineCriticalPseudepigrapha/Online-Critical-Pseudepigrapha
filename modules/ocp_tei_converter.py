#! /usr/bin/env python2

from lxml import etree
import os
import sys


def new_tei_doc(filename):
    """
    Convert a document with OCP markup to a TEI compliant markup.

    returns the new document content as a serialized string
    """
    ocp = etree.parse('/home/ian/web/web2py-grammateus3/'
                      'applications/grammateus3/static/docs/'
                      '{}'.format(filename))

    teiCorpus = etree.Element('teiCorpus')
    teiCorpus.set('xmlns', 'http://www.tei-c.org/ns/1.0')

    globalHeader = etree.SubElement(teiCorpus, 'teiHeader')
    # fileDesc
    fileDesc = etree.SubElement(globalHeader, 'fileDesc')
    titleStmt = etree.SubElement(fileDesc, 'titleStmt')
    title = etree.SubElement(titleStmt, 'title')
    title.text = ocp.xpath('/book/@title')[0]
    editionStmt = etree.SubElement(fileDesc, 'editionStmt')
    edition = etree.SubElement(editionStmt, 'edition')
    edition.set('n', '')
    etree.SubElement(edition, 'date')
    seriesStmt = etree.SubElement(fileDesc, 'seriesStmt')
    seriesTitle = etree.SubElement(seriesStmt, 'title')
    seriesTitle.text = 'Online Critical Pseudepigrapha'
    respStmt = etree.SubElement(seriesStmt, 'respStmt')
    respStmt.text = 'Ian W. Scott and Ken M. Penner, General Editors'
    publicationStmt = etree.SubElement(fileDesc, 'publicationStmt')
    publisher = etree.SubElement(publicationStmt, 'publisher')
    publisher.text = 'Society of Biblical Literature'
    pubPlace = etree.SubElement(publisher, 'pubPlace')
    pubPlace.text = 'Atlanta'
    availability = etree.SubElement(publisher, 'availability')
    availability.set('status', '')
    etree.SubElement(publisher, 'date')
    # other parts of global header
    encodingDesc = etree.SubElement(globalHeader, 'encodingDesc')
    projectDesc = etree.SubElement(encodingDesc, 'projectDesc')
    projectDesc.text = 'The Online Critical Pseudepigrapha is a project to ' \
                       'create accurate and complete electronic editions of ' \
                       'the so-called "Old Testament Pseudepigrapha" and ' \
                       'related literature. It is an electronic publication ' \
                       'of the Society of Biblical Literature.'
    etree.SubElement(globalHeader, 'profileDesc')
    etree.SubElement(globalHeader, 'revisionDesc')

    for version in ocp.xpath('/book/version'):
        tei = etree.SubElement(teiCorpus, 'TEI')
        # metadata for the current version
        localHeader = etree.SubElement(tei, 'teiHeader')
        localTitleStmt = etree.SubElement(localHeader, 'titleStmt')
        localTitle = etree.SubElement(localTitleStmt, 'title')
        localTitle.text = '{}: {}'.format(ocp.xpath('/book/@title')[0],
                                          version.get('title'))
        localFileDesc = etree.SubElement(localHeader, 'fileDesc')
        localSourceDesc = etree.SubElement(localFileDesc, 'sourceDesc')
        listWit = etree.SubElement(localSourceDesc, 'listWit')
        for ms in version.xpath('manuscripts/ms'):
            witness = etree.SubElement(listWit, 'witness')
            witness.set('{http://www.w3.org/XML/1998/namespace}id',
                        ms.get('abbrev'))
            witness.set('{http://www.w3.org/XML/1998/namespace}lang',
                        ms.get('language'))
            idno = etree.SubElement(witness, 'idno')
            idno.text = ms.xpath('./name')[0].text
            if ms.xpath('./bibliography'):
                listBib = etree.SubElement(witness, 'listBib')
                bibl = etree.SubElement(listBib, 'bibl')
                bibl.text = ms.xpath('./bibliography')[0].text
        localEncodingDesc = etree.SubElement(localHeader, 'encodingDesc')
        refsDecl = etree.SubElement(localEncodingDesc, 'refsDecl')
        for divn in version.xpath('divisions/division'):
            refState = etree.SubElement(refsDecl, 'refState')
            refState.set('unit', divn.get('label'))
            if divn.get('delimiter'):
                refState.set('delim', divn.get('delimiter'))
        editorialDecl = etree.SubElement(localEncodingDesc, 'editorialDecl')
        etree.SubElement(editorialDecl, 'correction')
        etree.SubElement(editorialDecl, 'normalization')
        etree.SubElement(editorialDecl, 'quotation')
        etree.SubElement(editorialDecl, 'segmentation')

        # text of the current version
        teiText = etree.SubElement(tei, 'text')
        teiTextAttr = teiText.attrib
        mylang = version.get('language')
        teiTextAttr['{http://www.w3.org/XML/1998/namespace}lang'] = mylang
        body = etree.SubElement(teiText, 'body')

        def addLayer(sourcediv, mydiv, mylevel, mybook, mynum):
            mylevel = mylevel + 1
            if sourcediv.xpath('div'):
                myref = refsDecl.xpath('refState')[mylevel]
                lastref = refsDecl.xpath('refState')[mylevel - 1]
                mydelim = lastref.get('delim')
                for sdiv in sourcediv.xpath('div'):
                    mdiv = etree.SubElement(mydiv, 'div')
                    thisnum = '{}{}{}'.format(mynum,
                                              mydelim,
                                              sdiv.get('number'))
                    mdiv.set('n', thisnum)
                    mdiv.set('{http://www.w3.org/XML/1998/namespace}id',
                             '{}{}'.format(mybook, thisnum))
                    mdiv.set('type', myref.get('unit'))
                    addLayer(sdiv, mdiv, mylevel, mybook, thisnum)
            else:
                for unit in sourcediv.xpath('unit'):
                    app = etree.SubElement(mydiv, 'app')
                    app.set('{http://www.w3.org/XML/1998/namespace}id',
                            unit.get('id'))
                    print unit.get('id')
                    for reading in unit.xpath('reading'):
                        rdg = etree.SubElement(app, 'rdg')
                        witstring = ' '.join(['#{}'.format(sig) for sig in
                                              reading.get('mss').encode('utf8'
                                              ).split(' ') if sig
                                              ]
                                             )
                        print witstring
                        rdg.set('wit', witstring.decode('utf8'))
                        if reading.text:
                            rdg.text = reading.text

        for div in version.xpath('text/div'):
            mydiv = etree.SubElement(body, 'div')
            myref = refsDecl.xpath('refState')[0]
            mybook = ocp.xpath('/book/@filename')[0]
            mynum = div.get('number')
            mydiv.set('n', mynum)
            mydiv.set('{http://www.w3.org/XML/1998/namespace}id',
                      '{}{}'.format(mybook, mynum))
            mydiv.set('type', myref.get('unit'))
            addLayer(div, mydiv, 0, mybook, mynum)

    return etree.tostring(teiCorpus, pretty_print=True)


def write_converted_xml(filename):
    '''
    Write out new xml string to a file in the directory static/docs/tei
    '''
    xmlstring = new_tei_doc(filename)
    newpath = os.path.join('/home/ian/web/web2py-grammateus3/'
                           'applications/grammateus3/static/docs/tei',
                           filename)
    with open(newpath, 'w') as myfile:
        myfile.write(xmlstring)

    print xmlstring


if __name__ == '__main__':
    write_converted_xml('{}.xml'.format(sys.argv[1]))
