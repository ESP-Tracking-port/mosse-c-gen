import cv2
import math
import numpy as np
from common import *
import os


def euclidean_imcenter_squared(row, col):
	row_center, col_center = row // 2, col // 2

	return (row - row_center) ** 2 + (col - col_center) ** 2


def generate_iter(sz_row=None, sz_col=None):
	if sz_row is None or sz_col is None:
		sz_row, sz_col = IMSIZE_2D

	for row in range(sz_row):
		for col in range(sz_col):
			center_squared = euclidean_imcenter_squared(row, col)
			res = math.exp(center_squared / (-2.0 * SIGMA))

			yield res


def generate(rows, cols):
	return np.fromiter(generate_iter(cols, rols), float).reshape((rows, cols))


def generate_format(rows, cols):
	return ''.join(format_array_iter("kGaussKernel", generate_iter, rows, cols))


def generate_format_savefile(rows, cols):
	formatted = generate_format(rows, cols)
	fname = "gauss_kernel_%dx%d.hpp" % (cols, rows)

	if not os.path.exists(fname):
		with open(fname, 'w') as f:
			pass

	with open(fname, "a") as f:
		f.write(generate_format(rows, cols))


if __name__ == "__main__":
	generate_format_savefile(*IMSIZE_2D)
