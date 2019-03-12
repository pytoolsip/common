# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-02-23 18:39:59
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-02-25 23:47:15

import os;
import sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

__all__ = ["CommonClient"];

try:
	from common_client import CommonClient;

except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);