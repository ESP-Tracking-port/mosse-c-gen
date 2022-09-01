"""
Generates a table of logarithms for integers from 1 to 256. Since only 8 bits
unsigned grayscales are expected, it is better to use a relatively small
precompiled matrix than compute the entire logarithm.

Considering that preprocessing is performed on each incoming frame, a
substantial increase in performance is expected
"""

import common
import numpy as np


ARRAY_PREFIX = "kLogMatrix8bit"
FILENAME = common.GEN_DIR_PREFIX + "LogMatrix.hpp"
_LOG_INFIMUM = 1
_LOG_SUPREMUM = 257


def generate_format_iter():
	yield common.CXX_NAMESPACE_BEGIN

	arr = np.array(list(map(lambda i: np.log(i), range(_LOG_INFIMUM,
		_LOG_SUPREMUM))))

	yield from common.format_array_iter_nd(ARRAY_PREFIX, arr, "float")
	yield common.CXX_NAMESPACE_END


def generate_format_savefile():
	for i in generate_format_iter():
		common.append_file(i, FILENAME)
