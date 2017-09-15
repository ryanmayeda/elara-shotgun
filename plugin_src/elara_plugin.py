# Foundry and/or Shotgun Software license goes here.

"""
This file will be imported by Nuke.
It launches the plugin's bootstrap process.
It should be expanded/duplicated to cover other applications later.

It is an offshoot of the file from Nuke:
https://github.com/shotgunsoftware/tk-nuke/blob/master/plugins/basic/menu.py

There is an equivalent file for each tk- engine, ex.:
https://github.com/shotgunsoftware/tk-houdini/blob/master/plugins/basic/python2.7libs/pythonrc.py
"""


import os
import sys


def plugin_startup():
    """
    Initializes the Toolkit plugin for Nuke.
    """

    # construct the path to the plugin root's folder.
    #      plugins/basic/menu.py
    #      -------------|
    # this part ^
    plugin_root_path = os.path.dirname(__file__)

    # the plugin python path will be just below the root level. add it to
    # sys.path
    plugin_python_path = os.path.join(plugin_root_path, "Python")
    sys.path.insert(0, plugin_python_path)

    # now that the path is there, we can import the plugin bootstrap logic
    try:
        from tk_elara import plugin_bootstrap
        plugin_bootstrap.bootstrap(plugin_root_path)
    except Exception, e:
        import traceback
        stack_trace = traceback.format_exc()

        message = "Shotgun Toolkit Error: %s" % (e,)
        details = "Error stack trace:\n\n%s" % (stack_trace)

        print e


# Invoked on startup
plugin_startup()
