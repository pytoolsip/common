# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-15 10:23:21
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-15 19:57:55

import wx;
from ProjectConfig import ProjectConfig;

AppConfig = {
	"version" : "1.0.1",
	"AppTitle" : u"PyToolsIP【python工具集成环境】",
	"AppSize" : (960,640),
	"AppBGColor" : wx.Colour(230,230,230),
	"CopyrightInfo" : u"Copyright(C) 2018-2019 JimDreamHeart. All Rights Reserved",

	"SearchPanelSize" : (380,320),
	"SearchPanelBGColor" : wx.Colour(220,220,220),
	"searchItemFocusColor" : wx.Colour(160,160,160),
	"searchItemBlurColor" : wx.Colour(210,210,210),
};

_ExcludeKey = ["version", "AppTitle", "CopyrightInfo"];

# 合并配置
for k,v in ProjectConfig.items():
	if k not in _ExcludeKey:
		AppConfig[k] = v;

