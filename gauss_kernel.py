import cv2
import math
import numpy as np
from common import *


def euclidean_imcenter_squared(row, col):
	row_center, col_center = IMCENTER

	return (row - row_center) ** 2 + (col - col_center) ** 2


def generate_iter(sz_row=None, sz_col=None):
	if sz_row is None or sz_col is None:
		sz_row, sz_col = IMSIZE_2D

	for row in range(sz_row):
		for col in range(sz_col):
			center_squared = euclidean_imcenter_squared(row, col)
			res = math.exp(center_squared / (-2.0 * SIGMA))

			yield res


def generate():
	return np.fromiter(generate_iter(), float).reshape(IMSIZE_2D)


def generate_format():
	return ''.join(format_array_iter("kGaussKernel", generate_iter, *IMSIZE_2D))


def generate_format_savefile():
	formatted = generate_format()

	with open("gauss_kernel_%dx%d.hpp" % IMSIZE_2D, "w") as f:
		f.write(generate_format())


if __name__ == "__main__":
	generate_format_savefile()
