import os, inspect;

from _Global import _GG;
from function.base import *;

# 缓存数据管理器
class CacheManager(object):
    def __init__(self):
        super(CacheManager, self).__init__();
        self._className_ = CacheManager.__name__;

    def setCache(self, namespace, key, value):
        if self.__checkNamespace__(namespace):
            cacheJson = self.__getCacheJson__(namespace);
            cacheJson[key] = value;
            self.__setCacheJson__(namespace);
        return False;

    def getCache(self, namespace, key):
        if self.__checkNamespace__(namespace):
            cacheJson = self.__getCacheJson__(namespace);
            return cacheJson.get(key, None);
        return None;

    def deleteCache(self, namespace, key):
        if self.__checkNamespace__(namespace):
            cacheJson = self.__getCacheJson__(namespace);
            if key in cacheJson:
                cacheJson.pop(key);
                self.__setCacheJson__(namespace);
        return False;

    def __checkNamespace__(self, namespace):
        isFindOut = False;
        for frame in inspect.stack():
            filename = frame[0].f_code.co_filename;
            if filename.find(namespace):
                isFindOut = True;
                break;
        if not isFindOut:
            return False;
        return os.path.exists(os.path.join(_GG("g_DataPath"), "tools", namespace));

    def __getCacheJson__(self, namespace):
        cacheJson, cachePath = {}, os.path.join(_GG("g_DataPath"), "cache", f"{namespace}.json");
        if not os.path.exists(cachePath):
            with open(cachePath, "r") as f:
                cacheJson = json.loads(f.read());
        return cacheJson;

    def __setCacheJson__(self, namespace, cacheJson):
        cachePath = os.path.join(_GG("g_DataPath"), "cache", f"{namespace}.json");
        with open(cachePath, "w") as f:
            f.write(json.dumps(cacheJson, indent=4));