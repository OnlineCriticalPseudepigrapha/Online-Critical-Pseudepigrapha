#! /usr/bin/python
"""
Run this app's tests via py.test

place this file in applications/<appname>/bin/

run with:
python <your web2py dir>/web2py.py -S <appname> -M -R applications/<appname>/bin/runtest.py

If you need access to a logged-in web2py user account (auth) you may need to run
this script with a web2py instance already running in the background. (Just run
web2py.py)
"""
import os
import sys
import pytest


def run_pytest(w2p_dir, test_dir, app_name):
    #errlist = (OSError,ValueError,SystemExit)

    try:
        test_dir = os.path.join(w2p_dir,
                                'applications', app_name, test_dir)
        if test_dir not in sys.path:
            sys.path.append(test_dir)  # imports from current folder
        modules_path = os.path.join('applications',
                                    app_name, 'modules')
        if modules_path not in sys.path:
            sys.path.append(modules_path)  # imports from app modules folder
        if 'site-packages' not in sys.path:
            sys.path.append('site-packages')  # imports from site-packages
        pytest.main([test_dir])

    except Exception, e:
        print type(e), e

if __name__ == '__main__':
    paths = ['/home/iscott/web/web2py/', '/home/ian/web/web2py/']
    runpath = paths[1]
    if os.path.exists(paths[0]):
        runpath = paths[0]
    run_pytest(runpath, 'modules', 'grammateus3')
