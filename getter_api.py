import common
import main
import hann
import gauss_kernel_fft
import pathlib


HEADER_PREFIX = "MosseApi.hpp"
CPP_PREFIX = "MosseApi.cpp"
_NL = "\n"
_DNL = "\n\n"
SOURCE_PREFIX = "MosseApi"
_MAPS_MARKER = "@MAPS@"
_NAMESPACE_MARKER = "@MOSSENAMESPACE@"


def _header_generate_iter():
	with open(str(pathlib.Path() / "stub" / "MosseApi") + ".hpp.stub", 'r') as f:
		yield f.read()


def _cpp_generate_iter():
	with open(str(pathlib.Path() / "stub" / "MosseApi") + ".cpp.stub", 'r') as f:
		content = f.read()
		maps = _cpp_generate_maps()
		content = content.replace(_MAPS_MARKER, maps)
		content = content.replace(_NAMESPACE_MARKER, common.CXX_NAMESPACE)

		yield content

def _cpp_generate_maps():
	return ''.join(_cpp_generate_maps_iter())


def _cpp_generate_maps_iter():

	make_window_size_pair = lambda rows, cols: "std::array<unsigned, 2>{%d, %d}" % (rows, cols)
	map_window_size_pair = map(lambda win: make_window_size_pair(*win), common.WINDOWS)
	window_size_pairs = ',\n\t'.join(map_window_size_pair)

	yield """\
static constexpr auto kWindowSizes = {
	%s
};

""" % window_size_pairs

	make_hann_name = lambda rows, cols: "%s" % common.make_sized_prefix(hann.ARRAY_PREFIX, rows, cols)
	map_hann_names = map(lambda win: make_hann_name(*win), common.WINDOWS)
	hann_names = ',\n\t'.join(map_hann_names)

	yield """\
static constexpr auto kHannMap = {
	%s
};

""" % hann_names

	make_gauss_kernel_fft_name = lambda rows, cols: "std::pair<float *, float *>{&%s[0][0], &%s[1][0]}" % (common.make_sized_prefix(gauss_kernel_fft.ARRAY_PREFIX, rows, cols), common.make_sized_prefix(gauss_kernel_fft.ARRAY_PREFIX, rows, cols))
	map_gauss_kernel_fft_names = map(lambda win: make_gauss_kernel_fft_name(*win), common.WINDOWS)
	gauss_kernel_fft_names = ',\n\t'.join(map_gauss_kernel_fft_names)

	yield """\
static constexpr auto kGaussKernelFftMap = {
	%s
};""" % gauss_kernel_fft_names


def _header_generate():
	return ''.join(_header_generate_iter())


def _cpp_generate():
	return ''.join(_cpp_generate_iter())


def generate_format_savefile():
	generated = _header_generate()
	common.append_file(generated, HEADER_PREFIX)
	generated = _cpp_generate()
	common.append_file(generated, CPP_PREFIX)
