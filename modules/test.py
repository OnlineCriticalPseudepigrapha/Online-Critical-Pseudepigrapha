### Test script for parse.py

from lxml import etree

from parse import BookParser

#book_file = '/home/jeff/src/ve/ocp/src/ocp/static/grammateus/docs/1En.xml'
book_file = '../static/docs/1En_small.xml'

p = Book(book_file)

info = p.book_info()

print 'title =', info['title']
print 'structure =', info['structure']

for version in info['versions']:
    for key in version:
        if key != 'text_structure':
            print 'Version', key, '-->', version[key]

        else:
            print 'Version textstructure'
            for ref in version[key]:
                for unit in version[key][ref]:
                    print '\t', ref, '-->', unit, '-->', version[key][ref][unit]['p']
    print '************'
print
print
