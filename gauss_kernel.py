import cv2
import math
import numpy as np


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


def format_iter():

	nrows, ncols = IMSIZE_2D
	yield "constexpr unsigned kGaussKernelHeight = %d;  // Number of rows\n" % nrows
	yield "constexpr unsigned kGaussKernelWidth = %d;  // Number of columns\n" % ncols
	yield 'constexpr float kGaussKernel[kGaussKernelHeight][kGaussKernelWidth] = {\n'
	yield '\t{'

	for cnt, val in enumerate(generate_iter()):
		yield "%.4ff" % val

		if cnt % IMSIZE_2D[1] == 0 and cnt != 0:
			yield "},\n\t{"
		else:
			yield ", "

	yield '}\n};'


def generate():
	return np.fromiter(generate_iter(), float).reshape(IMSIZE_2D)


def generate_format():
	return ''.join(format_iter())


def generate_format_savefile():
	formatted = generate_format()

	with open("gauss_kernel_%dx%d.hpp" % IMSIZE_2D, "w") as f:
		f.write(generate_format())


if __name__ == "__main__":
	generate_format_savefile()
