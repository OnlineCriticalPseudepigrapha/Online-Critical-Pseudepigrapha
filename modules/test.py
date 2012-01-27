### Test script for parse.py

from lxml import etree

from parse import BookParser

#book_file = '/home/jeff/src/ve/ocp/src/ocp/static/grammateus/docs/1En.xml'
book_file = '1En.xml'

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
