import os;
import re;
import inspect;
import json;

from _Global import _GG;
from function.base import *;

# 缓存数据管理器
class CacheManager(object):
    def __init__(self):
        super(CacheManager, self).__init__();
        self._className_ = CacheManager.__name__;
        self.__cache = {};

    def getNamespace(self):
        toolsDataPath = os.path.join(_GG("g_DataPath"), "tools").replace("\\", "/");
        for frame in inspect.stack():
            filename = frame[0].f_code.co_filename;
            mt = re.match(f"^{toolsDataPath}/((local/)?[^/]+)/.*$", filename.replace("\\", "/"));
            if mt:
                return mt.group(1).replace("/", "-");
        return "pytoolsip-common"; # 返回默认的命名空间

    def setCache(self, key, value):
        namespace = self.getNamespace();
        cacheJson = self.__getCacheJson__(namespace);
        cacheJson[key] = value;
        self.__setCacheJson__(namespace);

    def getCache(self, key, default = None):
        namespace = self.getNamespace();
        cacheJson = self.__getCacheJson__(namespace);
        return cacheJson.get(key, default);

    def deleteCache(self, key):
        namespace = self.getNamespace();
        cacheJson = self.__getCacheJson__(namespace);
        if key in cacheJson:
            cacheJson.pop(key);
            self.__setCacheJson__(namespace);

    def __getCacheJson__(self, namespace):
        if namespace not in self.__cache:
            cacheJson, cachePath = {}, os.path.join(_GG("g_DataPath"), "cache", f"{namespace}.json");
            if os.path.exists(cachePath):
                try:
                    with open(cachePath, "rb") as f:
                        cacheJson = json.load(f);
                except Exception as e:
                    _GG("Log").w(f"Failed to get cache json by namespace[{namespace}], err=>{e}!");
            self.__cache[namespace] = cacheJson;
        return self.__cache[namespace];

    def __setCacheJson__(self, namespace):
        cachePath = os.path.join(_GG("g_DataPath"), "cache", f"{namespace}.json");
        try:
            with open(cachePath, "wb") as f:
                f.write(json.dumps(self.__cache.get(namespace, {}), indent=4).encode("utf-8"));
        except Exception as e:
            _GG("Log").w(f"Failed to set cache json by namespace[{namespace}], err=>{e}!");