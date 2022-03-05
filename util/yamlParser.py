import os
import yaml
from easydict import EasyDict as edict

class YamlParser(edict):
    """
    This is yaml parser based on EasyDict.
    """
    def __init__(self, configDict=None, configFile=None):
        if configDict is None:
            configDict = {}

        if configFile is not None:
            assert(os.path.isfile(configFile))
            with open(configFile, 'r') as fo:
                configDict.update(yaml.safe_load(fo.read()))

        super(YamlParser, self).__init__(configDict)

    
    def mergeFromFile(self, configFile):
        with open(configFile, 'r') as fo:
            self.update(yaml.safe_load(fo.read()))

    
    def mergeFromDict(self, configDict):
        self.update(configDict)


def getConfig(configFile=None):
    return YamlParser(configFile=configFile)

