# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-15 10:23:21
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-04-20 11:41:00

import wx;
from ProjectConfig import ProjectConfig;

AppConfig = {
	"key" : "9efab2399c7c560b34de477b9aa0a465",
	"version" : "1.0.0",
	"AppTitle" : u"PyToolsIP【python工具集成环境】",
	"AppSize" : (960,640),
	"AppBGColor" : wx.Colour(230,230,230),
	"CopyrightInfo" : u"Copyright(C) 2018-2019 JimDreamHeart. All Rights Reserved",
	"SearchToolUrl" : "http://jimdreamheart.club",

	"SearchPanelSize" : (380,320),
	"SearchPanelBGColor" : wx.Colour(220,220,220),
	"searchItemFocusColor" : wx.Colour(160,160,160),
	"searchItemBlurColor" : wx.Colour(210,210,210),
};

_ExcludeKey = ["key", "version", "AppTitle", "CopyrightInfo"];

# 合并配置
for k,v in ProjectConfig.items():
	if k not in _ExcludeKey:
		AppConfig[k] = v;

