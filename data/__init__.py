# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-11-08 21:44:35
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-11-08 21:47:12

import os;
import sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

__all__ = ["RandomPool"];

try:
	from randomPool import RandomPool;

except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);