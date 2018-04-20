#!/usr/bin/python
from flask import jsonify
from datetime import datetime
try:
    from urllib import urlopen  # Python 2
except ImportError:
    from urllib.request import urlopen  # Python 3


class UserCredentials(object):
    """Stores interface authentication session results when searching for a client on the network."""

    def __init__(self, un, pw, priv):
        """Initialization method."""
        self.un = un
        self.pw = pw
        self.priv = priv


"""Global variables."""
# Credentials class variable.  Stores as creds.un and creds.pw for username and password
creds = UserCredentials('', '', '')


def setUserCredentials(username, password, privPassword=''):
    """Return creds class with username and password in it."""
    creds.un = username
    creds.pw = password
    creds.priv = privPassword
    return creds


def containsSkipped(x):
    """Return if the word 'skipped' is in the provided string.

    Returns True if string contains the word "skipped".
    Returns False otherwise.
    """
    try:
        if "skipped" in str(x):
            return True
        else:
            return False
    except:
        return False


def removeDictKey(d, key):
    """Remove key from dictionary."""
    r = dict(d)
    del r[key]
    return r


def isInteger(x):
    """Test if provided value is an integer or not."""
    try:
        int(x)
        return True
    except ValueError:
        return False


def checkForVersionUpdate(config):
    """Check for NetConfig updates on GitHub."""
    try:
        # with urlopen(config['GH_MASTER_BRANCH_URL']) as a:
        # masterConfig = a.read().decode('utf-8')
        masterConfig = urlopen(config['GH_MASTER_BRANCH_URL'])
        masterConfig = masterConfig.read().decode('utf-8')
        # Reverse lookup as the VERSION variable should be close to the bottom
        if masterConfig:
            for x in masterConfig.splitlines():
                if 'VERSION' in x:
                    x = x.split('=')
                    try:
                        # Strip whitespace and single quote mark
                        masterVersion = x[-1].strip().strip("'")
                    except IndexError:
                        continue
                    # Verify if current version matches most recent GitHub release
                    if masterVersion != config['VERSION']:
                        # Return False if the current version does not match the most recent version
                        return jsonify(status="False", masterVersion=masterVersion)
            # If VERSION can't be found, successfully compared, or is identical, just return True
            return jsonify(status="True")
        else:
            # Error when accessing URL. Default to True
            return "True"
    except IOError as e:
        # Catch exception if unable to access URL, or access to internet is blocked/down. Default to True
        return "True"
    except Exception as e:
        # Return True for all other exceptions
        return "True"


# Get current timestamp for when starting a script
def getCurrentTime():
    """Get current timestamp."""
    currentTime = datetime.now()
    return currentTime


# Returns time elapsed between current time and provided time in 'startTime'
def getScriptRunTime(startTime):
    """Calculate time elapsed since startTime was first measured."""
    endTime = getCurrentTime() - startTime
    return endTime


def interfaceReplaceSlash(x):
    """Replace all forward slashes in string 'x' with an underscore."""
    x = x.replace('_', '/')
    return x
