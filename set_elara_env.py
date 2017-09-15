# Set Elara environment for Shotgun/Toolkit launch

"""

"""

import sys
import os

def set_elara_env():
    """
    Mimic the environment variables Elara will set when launching applications
    This will (probably) only be used for testing
    """
    sys.path.append("/data/orgs/Foundry/plugins/shotgun/plugin_build")

    os.environ["ELARA_GROUP_NAME"] = "Foundry"
    os.environ["ELARA_SHOTGUN_URL"] = "https://visionmongers.shotgunstudio.com"
    os.environ["ELARA_SHOTGUN_ID"] = "68"

    os.environ["SHOTGUN_HOME"] = "~/.shotgun"


set_elara_env()
