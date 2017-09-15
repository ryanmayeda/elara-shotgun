# Foundry and/or Shotgun Software license goes here.

import os
import sys
import time

import os
from urlparse import urlparse


def autopopulate_shotgun_url():
    """
    Write $ELARA_SHOTGUN_URL to $SHOTGUN_HOME/authentication.yml to auto-populate Shotgun URL
    May not be needed if $SHOTGUN_HOME is a shared location
    """

    shotgun_home = os.environ["SHOTGUN_HOME"]
    elara_shotgun_url = os.environ["ELARA_SHOTGUN_URL"]
    authentication_yaml_file = open(os.path.expanduser("%s/authentication.yml" % (shotgun_home)), "w")
    authentication_yaml_file.write("{current_host: '%s'}" % (elara_shotgun_url))
    authentication_yaml_file.close()

def bootstrap(plugin_root_path):
    """
    Entry point for toolkit bootstrap in Nuke.

    Called by the basic/startup/menu.py file.

    :param str plugin_root_path: Path to the root folder of the plugin
    """

    # --- Import Core ---
    #
    # - If we are running the plugin built as a stand-alone unit,
    #   try to retrieve the path to sgtk core and add that to the pythonpath.
    #   When the plugin has been built, there is a sgtk_plugin_elara_basic
    #   module which we can use to retrieve the location of core and add it
    #   to the pythonpath.
    # - If we are running toolkit as part of a larger zero config workflow
    #   and not from a standalone workflow, we are running the plugin code
    #   directly from the engine folder without a bundle cache and with this
    #   configuration, core already exists in the pythonpath.

    # Now see if we are running stand alone or in situ
    from sgtk_plugin_elara_basic import manifest

    # Retrieve the Shotgun toolkit core included with the plug-in and
    # prepend its python package path to the python module search path.
    # this will allow us to import sgtk
    tk_core_python_path = manifest.get_sgtk_pythonpath(plugin_root_path)
    sys.path.insert(0, tk_core_python_path)
    import sgtk

    # Plugin info from the manifest
    plugin_id = manifest.plugin_id
    base_config = manifest.base_configuration

    # Get the path to the built plugin's bundle cache
    bundle_cache = os.path.join(plugin_root_path, "bundle_cache")

    # Ensure Shotgun login screen auto-populates with the URL tracked by Elara
    autopopulate_shotgun_url()

    # Start logging for the Nuke engine, expand to other engines later
    sgtk.LogManager().initialize_base_file_handler("tk-nuke")

    # Bootstrap Toolkit (see http://developer.shotgunsoftware.com/tk-core/bootstrap.html#toolkitmanager)
    mgr = sgtk.bootstrap.ToolkitManager()
    mgr.plugin_id = "elara.basic"

    # Set base configuration to whatever is in the manifest (likely to be Shotgun's defaul basic config)
    mgr.base_configuration = manifest.base_configuration

    # Use plugin's pre-cached bundle cache
    mgr.bundle_cache_fallback_paths = [bundle_cache]

    # Run the Nuke bootstrap, expand to other applications later
    elara_shotgun_id = os.environ["ELARA_SHOTGUN_ID"]
    e = mgr.bootstrap_engine("tk-nuke", entity={"type": "Project", "id": int(elara_shotgun_id)})