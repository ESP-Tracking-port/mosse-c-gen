import gauss_kernel
import numpy as np
import random
import gauss_kernel
import common


ARRAY_PREFIX = "kGaussKernelFft"
ARRAY_SUFFIX_COMPLEX = "Complex"
ARRAY_SUFFIX_IMREAL = "ImReal"
COMPLEX_TYPESTR = "std::complex<float>"


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


def generate(rows, cols):
	kernel = np.fromiter(gauss_kernel.generate_iter(rows, cols), float)

	return np.fft.fft(kernel)


def generate_format_iter(rows, cols):
	yield common.CXX_NAMESPACE_BEGIN

	generated = generate(rows, cols)

	yield ''.join(common.format_array_iter(common.make_sized_prefix(ARRAY_PREFIX, cols, rows, ARRAY_SUFFIX_COMPLEX), generated, 1, rows * cols, COMPLEX_TYPESTR, True))
	yield ''.join(common.format_array_iter(common.make_sized_prefix(ARRAY_PREFIX, cols, rows, ARRAY_SUFFIX_IMREAL), np.concatenate((generated.real, generated.imag)), 2, rows * cols, "float", False))
	yield common.CXX_NAMESPACE_END


def generate_format_savefile(rows, cols, fname):
	for i in generate_format_iter(rows, cols):
		common.append_file(i, fname)


if __name__ == "__main__":
	test_fft()
