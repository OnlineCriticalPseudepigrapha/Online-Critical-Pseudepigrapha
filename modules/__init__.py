import os

# Track changes to modules so that the server knows about them
# Only do this for local requests e.g. on a development machine

# from gluon import *
#
# if current.request.is_local:
#     from gluon.custom_import import track_changes
#     track_changes()


def check_path(path):
    if os.path.exists(path):
        return path
    raise OSError(2, "{}: {}".format(os.strerror(2), path))

