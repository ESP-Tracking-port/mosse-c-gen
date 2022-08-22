import cv2
import math
import numpy as np
import common


SIGMA = 100.0
IMSIZE_2D = (100, 100)
IMCENTER = [i // 2 for i in IMSIZE_2D]
PRECISION = 5


def euclidean_imcenter_squared(row, col):
	row_center, col_center = IMCENTER

	return (row - row_center) ** 2 + (col - col_center) ** 2


def generate_iter():
	sz_row, sz_col = IMSIZE_2D

	for row in range(sz_row):
		for col in range(sz_col):
			center_squared = euclidean_imcenter_squared(row, col)
			res = math.exp(center_squared / (-2.0 * SIGMA))

			yield res


def generate():
	return np.fromiter(generate_iter(), float).reshape(IMSIZE_2D)


def generate_format():
	return ''.join(common.format_array_iter("kGaussKernel", generate_iter, *IMSIZE_2D))


def generate_format_savefile():
	formatted = generate_format()

	with open("gauss_kernel_%dx%d.hpp" % IMSIZE_2D, "w") as f:
		f.write(generate_format())


if __name__ == "__main__":
	generate_format_savefile()
