# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-08-25 14:09:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 22:57:10

from eventDispatchCore.EventId import EVENT_ID as G_EVENT;

# 热键配置
HotKeyConfig = {
	"CTRL_P" : G_EVENT.SHOW_SEARCH_PANEL_EVENT, # Ctrl + P
	"ESC" : G_EVENT.ESC_DOWN_EVENT, # ESC
	"CTRL_F5" : G_EVENT.RESTART_APP_EVENT, # Ctrl + F5
	"SHIFT_ESC" : G_EVENT.STOP_APP_EVENT, # Shift + ESC
	"ALT_P" : G_EVENT.SCREENSHOT, # Alt + P
	"CTRL_ALT_P" : G_EVENT.SCREENSHOT_AFTER_HIDING_WIN, # Ctrl + Alt + P
};

# 键盘值映射表
KeyCodeMap = {
	314 : "LEFT",
	315 : "UP",
	316 : "RIGHT",
	317 : "DOWN",
};

# Unicode值映射表
UnicodeKeyMap = {
	27 : "ESC",
	32 : "SPACE",
};
