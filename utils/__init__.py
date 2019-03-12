# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-11-24 15:40:54
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-12-01 11:53:19

import os;
import sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

__all__ = ["importUtil"];

try:
	import importUtil;

except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);