#from lxml import etree
from parse import BookParser

# coding: utf8
def index():
    filename = request.args[0]
    return dict(filename = filename)

def text():
    filename = request.args[0]
    return dict(filename = filename)

def test():
    filename = request.args[0]
    book_file = 'static/docs/%s.xml' % filename
    p = BookParser(book_file)
    info = p.book_info()

    print 'title =', info['title']
    print 'structure =', info['structure']

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

    return dict()