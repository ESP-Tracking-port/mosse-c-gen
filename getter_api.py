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


def _header_generate_iter():
	with open(str(pathlib.Path() / "stub" / "MosseApi") + ".hpp.stub", 'r') as f:
		yield f.read()


def _cpp_generate_iter():
	with open(str(pathlib.Path() / "stub" / "MosseApi") + ".cpp.stub", 'r') as f:
		content = f.read()
		maps = _cpp_generate_maps()
		content = content.replace(_MAPS_MARKER, maps)

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
};
""" % gauss_kernel_fft_names


def _cpp_generate_iter_():
	yield '#include "GetterApi.hpp"' + _NL
	yield '#include "%s%s"' % (common.GEN_DIR_PREFIX, main.MAIN_HEADER_PREFIX) + _NL
	yield '#include <array>' + _NL
	yield '#include <limits>' + _NL
	yield '#include <cstdlib>'
	yield _DNL

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
};

""" % gauss_kernel_fft_names

	yield """\
void getClosestWindow(unsigned &aRows, unsigned &aCols)
{
	auto prevDiff = std::numeric_limits<unsigned>::max();
	const auto area = aRows * aCols;
	int minCounter = 0;
	int counter = 0;

	for (const window : kWindowSizes) {
		auto diff = abs(window[0] * window[1] - area);

		if (diff < prevDiff) {
			prevDiff = diff;
			minCounter = counter;
		}

		++counter;
	}

	aRows = kWindowSizes[counter][0];
	aCols = kWindowSizes[counter][1];
}

"""

	yield """\
static int checkWindowExists(unsigned aRows, unsigned aCols)
{
	int counter = 0;

	for (const auto size : kWindowSizes) {
		if (aRows == size[0] && aCols == size[1]) {
			return counter;
		}

		counter += 1;
	}

	return -1;
}

"""

	yield """\
static float *getHann(unsigned aRows, unsigned aCols)
{
	int id = checkWindowExists(aRows, aCols);

	if (id < 0) {
		return nullptr;
	}

	return kHannMap[id];
}

std::pair<float *, float *> getGaussKernelFft(unsigned aRows, unsigned aCols)
{
	int id = checkWindowExists(aRows, aCols);

	if (id < 0) {
		return {nullptr, nullptr};
	}

	return kGaussKernelFftMap[id];
}

"""

def _header_generate():
	return ''.join(_header_generate_iter())


def _cpp_generate():
	return ''.join(_cpp_generate_iter())


def generate_format_savefile():
	generated = _header_generate()
	common.append_file(generated, HEADER_PREFIX)
	generated = _cpp_generate()
	common.append_file(generated, CPP_PREFIX)
