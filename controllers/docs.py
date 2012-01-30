# coding: utf8
from lxml import etree
from parse import BookParser

def index():
    filename = request.args[0]
    return dict(filename = filename)

def text():
    filename = request.args[0]
    return dict(filename = filename)

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
                for k, v in value.items():
                    print '\t', k, '-->', v
        print '************'
    print
    print

    return dict(title = title, info = info)