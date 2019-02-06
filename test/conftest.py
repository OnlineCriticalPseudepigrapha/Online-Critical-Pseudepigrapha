#!/usr/bin/env python

'''
py.test configuration and fixtures file.

This file is lightly adapted from the one by viniciusban;
Part of the web2py.test model app (https://github.com/viniciusban/web2py.test)

This file
- Tells application it's running in a test environment.
- Creates a complete web2py environment, similar to web2py shell.
- Creates a WebClient instance to browse your application, similar to a real
web browser.
- Propagates some application data to test cases via fixtures, like baseurl
and automatic appname discovery.

To write to db in test:

web2py.db.table.insert(**data)
web2py.db.commit()

To run tests:

cd path/to/web2py (you must be in web2py root directory to run tests)
python3.6 -m pytest -x [-l] [-q|-v] -s applications/my_app_name/tests

(used to need running web2py instance:
    python3.6 web2py.py -a my_password --nogui &
but no longer necessary.)


'''

import os
import pytest
import sys
#from pprint import pprint
#sys.path.insert(0, '')

# allow imports from modules and site-packages
dirs = os.path.split(__file__)[0]
appname = dirs.split(os.path.sep)[-2]
modules_path = os.path.join('applications', appname, 'modules')
if modules_path not in sys.path:
    sys.path.append(modules_path)  # imports from app modules folder
if 'site-packages' not in sys.path:
    sys.path.append('site-packages')  # imports from site-packages

#from gluon.shell import env
#web2py_env = env(appname, import_models=True,
#                 extra_request=dict(is_local=True))


@pytest.fixture(scope='module')
def baseurl(appname):
    '''The base url to call your application.

    Change you port number as necessary.
    '''

    return 'http://localhost:8000/%s' % appname


@pytest.fixture(scope='module')
def appname():
    '''Discover application name.

    Your test scripts must be on applications/<your_app>/tests
    '''
    dirs = os.path.split(__file__)[0]
    appname = dirs.split(os.path.sep)[-2]
    return appname


@pytest.fixture(scope='module', autouse=True)
def fixture_create_testfile_for_application(request, appname):
    '''
    Creates a temp file to tell application she's running under a
    test environment.

    Usually you will want to create your database in memory to speed up
    your tests and not change your development database.

    This fixture is automatically run by py.test at module level. So, there's
    no overhad to test performance.
    '''
    import os
    import shutil

    # note: if you use Ubuntu, you can allocate your test database on ramdisk
    # simply using the /dev/shm directory.
    temp_dir = '/dev/shm/' + appname

    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)

    # IMPORTANT: temp_filename must be the same as set in app/models/db.py
    temp_filename = '%s/tests_%s.tmp' % (temp_dir, appname)

    with open(temp_filename, 'w+') as tempfile:
        tempfile.write('application %s running in test mode' % appname)

    def _remove_temp_file_after_tests():
        shutil.rmtree(temp_dir)
    request.addfinalizer(_remove_temp_file_after_tests)


#@pytest.fixture(autouse=True)
def fixture_cleanup_db(web2py):
    '''Truncate all database tables before every single test case.

    This can really slow down your tests. So, keep your test data small and try
    to allocate your database in memory.

    Automatically called by test.py due to decorator.

    '''
    # TODO: Is this deprecated in favor of the fin() finalizer function of the
    # db fixture?

    # TODO: figure out db rollback to standard state (not truncate to None)
    # web2py.db.rollback()
    # for tab in web2py.db.tables:
    #     web2py.db[tab].truncate()
    # web2py.db.commit()
    print('\nran fixture cleanup !!!!!!!!!!!!!!!!!!!!!!!!!\n')
    pass


@pytest.fixture(scope='module')
def client(baseurl, fixture_create_testfile_for_application):
    '''
    Create a new WebClient instance once per module.
    '''
    from gluon.contrib.webclient import WebClient
    webclient = WebClient(baseurl)
    return webclient


@pytest.fixture(scope='module')
def user_login(request, web2py, client, db):
    """
    Provide a new, registered, and logged-in user account for testing.
    """
    # register test user
    auth = web2py.current.auth
    reg_data = {'first_name': 'Homer',
                'last_name': 'Simpson',
                'email': 'scottianw@gmail.com',
                'password': 'testing',
                'time_zone': 'America/Toronto'}
    # create new test user if necessary and delete if there's more than one
    user_query = db((db.auth_user.first_name == reg_data['first_name']) &
                    (db.auth_user.last_name == reg_data['last_name']) &
                    (db.auth_user.email == reg_data['email']) &
                    (db.auth_user.time_zone == reg_data['time_zone']))
    user_count = user_query.count()
    if user_count == 0:
        auth.table_user().insert(**reg_data)
    elif user_count > 1:
        u_count = user_count
        userset = user_query.select()
        while u_count > 1:
            lastu = userset.last()
            lastu.delete_record()
            u_count -= 1
    else:
        pass

    assert user_query.count() == 1
    user_record = user_query.select().first()
    assert user_record

    # log test user in
    auth.login_user(user_record)
    assert auth.is_logged_in()

    def fin():
        """
        Delete the test user's account.
        """
        # FIXME: below causes db hang in test_walk_reply case 2
        # user_record.delete_record()
        # db.commit()
        # TODO: remove test user's performance record
        #assert user_query.count() == 0

    request.addfinalizer(fin)
    return user_record.as_dict()


@pytest.fixture(scope='module')
def web2py(appname, fixture_create_testfile_for_application):
    '''
    Create a Web2py environment similar to that achieved by Web2py shell.

    It allows you to use global Web2py objects like db, request, response,
    session, etc.

    Concerning tests, it is usually used to check if your database is an
    expected state, avoiding creating controllers and functions to help
    tests.
    '''

    from gluon.shell import env
    from gluon.storage import Storage

    web2py_env = env(appname, import_models=True,
                     extra_request=dict(is_local=True))

    # Uncomment next 3 lines to allow using global Web2py objects directly
    # in your test scripts.
    if hasattr(web2py_env, '__file__'):
        del web2py_env['__file__']  # avoid py.test import error
    globals().update(web2py_env)

    return Storage(web2py_env)


@pytest.fixture(scope='module')
def db(web2py, request):
    """
    Provides a access to the production database from within test functions.

    While the web2py object (providing global framework objects standard in a
    web2py session) has a module-level scope, this db fixture has a function-
    level scope. This means that any code below is run for each test function,
    allowing for function-level db setup and teardown.

    The fin teardown function expects a 'newrows' dictionary to be created in
    the requesting test function. This dictionary should have db table names as
    its keys and a list of newly-inserted row id numbers as the values.
    """
    # TODO: make sure test functions all create a 'newrows' dictionary
    mydb = web2py.db
    newrows = getattr(request.node.instance, 'newrows', None)

    def fin():
        """
        Delete any newly inserted rows in the test database.
        """
        print('checking for inserted rows to remove**********')
        #pprint(newrows)
        if newrows:
            print('removing')
            for tbl, rowids in newrows.iteritems():
                mydb(mydb[tbl].id.belongs(rowids)).delete()
                for i in rowids:
                    assert not mydb[mydb[tbl]](i)

    request.addfinalizer(fin)
    return mydb
