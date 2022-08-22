"""
Generates Hann windows
"""
import math
import numpy as np


def generate(rows, cols):
	generator_vert = lambda i: 0.5 * (1 - math.cos(2 * math.pi * i / (rows - 1)))
	vec_vert = np.fromiter(map(lambda i: generator_vert(i), range(rows)), float).reshape((rows, 1))
	generator_hor = lambda i: 0.5 * (1 - math.cos(2 * math.pi * i / (cols - 1)))
	vec_hor = np.fromiter(map(lambda i: generator_hor(i), range(cols)), float).reshape((1, cols))

	return np.matmul(vec_vert, vec_hor)


if __name__ == "__main__":
	generated = generate(20, 10)
	print(generated)
	print(generated.shape)
