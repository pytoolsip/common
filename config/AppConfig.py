# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-15 10:23:21
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 20:21:12

import wx;
from ProjectConfig import ProjectConfig;

AppConfig = {
	"AppTitle" : u"PyToolsIP【python工具集成环境】",
	"AppSize" : (960,640),
	"AppBGColor" : wx.Colour(230,230,230),
	"CopyrightInfo" : u"Copyright(C) 2018-2019 JimDreamHeart. All Rights Reserved",
	"PyToolsIPUrl" : "http://jimdreamheart.club/pytoolsip",
	"SearchToolUrl" : "http://jimdreamheart.club/pytoolsip/toollist",

	"SearchPanelSize" : (380,320),
	"SearchPanelBGColor" : wx.Colour(220,220,220),
	"searchItemFocusColor" : wx.Colour(160,160,160),
	"searchItemBlurColor" : wx.Colour(210,210,210),
};

_ExcludeKey = ["AppTitle", "CopyrightInfo"];

# 合并配置
for k,v in ProjectConfig.items():
	if k not in _ExcludeKey:
		AppConfig[k] = v;

