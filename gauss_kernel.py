import cv2
import math
import numpy as np
from common import *
import os


ARRAY_PREFIX = "kGaussKernel"


def euclidean_imcenter_squared(row, col, sz_row, sz_col):
	row_center, col_center = sz_col // 2, sz_row // 2

	return (row - row_center) ** 2 + (col - col_center) ** 2


def generate_iter(sz_row=None, sz_col=None):
	if sz_row is None or sz_col is None:
		sz_row, sz_col = IMSIZE_2D

	for row in range(sz_row):
		for col in range(sz_col):
			center_squared = euclidean_imcenter_squared(row, col, sz_row, sz_col)
			res = math.exp(center_squared / (-2.0 * SIGMA))

			yield res


def generate(rows, cols):
	return np.fromiter(generate_iter(cols, rows), float).reshape((rows, cols))


def generate_format(rows, cols):
	return ''.join(format_array_iter(ARRAY_PREFIX, generate_iter(cols, rows), rows, cols, "float", False))


def generate_format_savefile(rows, cols, fname):
	append_file(CXX_NAMESPACE_BEGIN, fname)
	formatted = generate_format(rows, cols)
	append_file(formatted, fname)
	append_file(CXX_NAMESPACE_END, fname)


def main():
	generate_format_savefile(*IMSIZE_2D)


if __name__ == "__main__":
	main()
