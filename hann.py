"""
Generates Hann windows
"""
import math
import numpy as np
import common


ARRAY_PREFIX = "kHann"


def generate(rows, cols):
	generator_vert = lambda i: 0.5 * (1 - math.cos(2 * math.pi * i / (rows - 1)))
	vec_vert = np.fromiter(map(lambda i: generator_vert(i), range(rows)), float).reshape((rows, 1))
	generator_hor = lambda i: 0.5 * (1 - math.cos(2 * math.pi * i / (cols - 1)))
	vec_hor = np.fromiter(map(lambda i: generator_hor(i), range(cols)), float).reshape((1, cols))

	return np.matmul(vec_vert, vec_hor)


def generate_format_iter(rows, cols):
	yield common.CXX_NAMESPACE_BEGIN

	generated = generate(rows, cols).reshape((1, rows * cols))[0]

	yield ''.join(common.format_array_iter(common.make_sized_prefix(ARRAY_PREFIX, rows, cols), generated, rows, cols, "float", False))
	yield common.CXX_NAMESPACE_END


def generate_format_savefile(rows, cols, fname):
	for i in generate_format_iter(rows, cols):
		common.append_file(i, fname)


if __name__ == "__main__":
	generated = generate(20, 10)
	print(generated)
	print(generated.shape)
