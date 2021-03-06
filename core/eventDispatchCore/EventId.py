# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-01 10:56:10
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-07 00:12:36

from enum import Enum, unique;

# 自增的事件Id函数
global CUR_EVENT_ID;
CUR_EVENT_ID = -1;
def getNewEventId():
	global CUR_EVENT_ID;
	CUR_EVENT_ID += 1;
	return CUR_EVENT_ID;

# 枚举事件Id
@unique
class EVENT_ID(Enum):
	# 获取新的事件ID【供具体工具创建新的事件ID】
	@staticmethod
	def getNewId():
		return getNewEventId();

	TO_UPDATE_VIEW = getNewEventId(); # 创建事件Id的标准样式
	
	UPDATE_TREE_ITEMS = getNewEventId(); # 更新树状Items事件

	UPDATE_WINDOW_RIGHT_VIEW = getNewEventId(); # 更新右窗口视图

	SHOW_SEARCH_PANEL_EVENT = getNewEventId(); # 显示搜索面板事件

	ESC_DOWN_EVENT = getNewEventId(); # ESC按键事件
	
	STOP_APP_EVENT = getNewEventId(); # 停止APP事件

	RESTART_APP_EVENT = getNewEventId(); # 重启APP事件

	ADD_LAUNCHER_EVENT = getNewEventId(); # 添加启动事件

	LOGIN_SUCCESS_EVENT = getNewEventId(); # 登录成功事件

	UPDATE_WINDOW_LEFT_VIEW = getNewEventId(); # 更新左窗口视图
	
	LOGOUT_SUCCESS_EVENT = getNewEventId(); # 注销成功事件

	UPDATE_APP_EVENT = getNewEventId(); # 更新APP事件

	SAVE_IP_CONFIG = getNewEventId(); # 保存平台配置
	
	CREATE_FIXED_PAGE = getNewEventId(); # 创建已固定的标签页
	
	SAVE_FIXED_PAGE_DATA = getNewEventId(); # 保存已固定的标签页数据
	
	SCREENSHOT = getNewEventId(); # 截屏

	SCREENSHOT_AFTER_HIDING_WIN = getNewEventId(); # 隐藏窗口后截屏

	REVEAL_IN_WINDOW_LEFT_VIEW = getNewEventId(); # 定位到左窗口视图