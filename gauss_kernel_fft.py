import gauss_kernel
import numpy as np
import random
import gauss_kernel
import common


ARRAY_PREFIX = "kGaussKernelFft"
ARRAY_SUFFIX_COMPLEX = "Complex"
ARRAY_SUFFIX_IMREAL = "ImReal"
ARRAY_SUFFIX_IMREAL_3D = "ImReal3d"
COMPLEX_TYPESTR = "std::complex<float>"
SCALED = [  # Scale, suffix
	(0.125, "3dScaled125"),
]


def test_fft():
	a = [random.random() for _ in range(100)]
	b = [random.random() for _ in range(10)] + a[10:30]
	a = np.array(a)
	b = np.array(b)
	a_fft = np.fft.fft(a)
	b_fft = np.fft.fft(b)
	assert(a.size == a_fft.size)
	assert(all(a[:10] == a[:10]))
	assert(all(b[10:] == a[10:30]))
	print(b_fft[10:])
	print(a_fft[10:30])
	assert(all(b_fft[10:] == a_fft[10:30]))


def get_gaussian_map(rows, cols):
	'''
	returns the gaussian map response
	'''

	x, y, w, h = 0, 0, cols, rows
	center_x = x + w/2
	center_y = y + h/2

	# create a rectangular grid out of two given one-dimensional arrays
	xx, yy = np.meshgrid(np.arange(x, x+w), np.arange(y, y+h))

	# calculating distance of each pixel from roi center
	dist = (np.square(xx - center_x) + np.square(yy - center_y)) \
		/ (2 * common.SIGMA)

	response = np.exp(-dist)
	# response = (response - response.min()) / (response.max() - response.min())

	return response


def generate(rows, cols):
	'''
	returns the fft2 (2D Discrete Fast Fourier Transform) of the gaussian response map
	'''

	g = get_gaussian_map(rows, cols)
	g_fft = np.fft.fft2(g)

	return g_fft.flatten()


def complex_decompose(v):
	yield v.real
	yield v.imag


def generate_format_iter(rows, cols):
	yield common.CXX_NAMESPACE_BEGIN

	generated = generate(rows, cols)

	yield ''.join(common.format_array_iter(common.make_sized_prefix(ARRAY_PREFIX, rows, cols, ARRAY_SUFFIX_COMPLEX), generated, 1, rows * cols, COMPLEX_TYPESTR, True))
	yield ''.join(common.format_array_iter(common.make_sized_prefix(ARRAY_PREFIX, rows, cols, ARRAY_SUFFIX_IMREAL), np.concatenate((generated.real, generated.imag)), 2, rows * cols, "float", False))

	generated = generated.reshape(rows * cols)
	generated = list(map(lambda v: (v.real, v.imag), generated))
	generated = list(common.iter_plain(generated))
	generated = np.array(generated)
	generated = generated.reshape(rows, cols, 2)

	yield ''.join(common.format_array_iter_nd(common.make_sized_prefix(ARRAY_PREFIX, rows, cols, ARRAY_SUFFIX_IMREAL_3D), generated, "float"))

	for scale, suffix in SCALED:
		yield ''.join(common.format_array_iter_nd(common.make_sized_prefix(ARRAY_PREFIX, rows, cols, suffix), generated * scale, "float"))

	yield common.CXX_NAMESPACE_END


def generate_format_savefile(rows, cols, fname):
	for i in generate_format_iter(rows, cols):
		common.append_file(i, fname)


if __name__ == "__main__":
	test_fft()
