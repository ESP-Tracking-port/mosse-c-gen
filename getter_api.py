import common
import main
import hann
import gauss_kernel_fft

HEADER_PREFIX = "MosseApi.hpp"
CPP_PREFIX = "MosseApi.cpp"
_NL = "\n"
_DNL = "\n\n"


def _header_generate_iter():
	define_before, define_after = common.make_define_sentinel(HEADER_PREFIX)

	yield define_before
	yield "#include <utility>" + _NL
	yield _NL
	yield common.CXX_NAMESPACE_BEGIN
	yield _NL
	yield "float *getHann(unsigned rows, unsigned cols);" + _NL
	yield "std::pair<float *, float *> getGaussKernelFft(unsigned rows, unsigned cols);" + _NL
	yield "void getClosestWindow(unsigned &aRows, unsigned &aCols);" + _NL
	yield _NL
	yield common.CXX_NAMESPACE_END + _NL
	yield define_after


def _cpp_generate_iter():
	yield '#include "GetterApi.hpp"' + _NL
	yield '#include "%s%s"' % (common.GEN_DIR_PREFIX, main.MAIN_HEADER_PREFIX) + _NL
	yield '#include <array>' + _NL
	yield '#include <limits>' + _NL
	yield '#include <cstdlib>'
	yield _DNL

	make_window_size_pair = lambda rows, cols: "{%d, %d}" % (rows, cols)
	map_window_size_pair = map(lambda win: make_window_size_pair(*win), common.WINDOWS)
	window_size_pairs = ',\n\t'.join(map_window_size_pair)

	yield """\
static constexpr std::array<unsigned, 2> kWindowSizes[] = {
	%s
};

""" % window_size_pairs

	make_hann_name = lambda rows, cols: "&%s[0][0]" % common.make_sized_prefix(hann.ARRAY_PREFIX, rows, cols)
	map_hann_names = map(lambda win: make_hann_name(*win), common.WINDOWS)
	hann_names = ',\n\t'.join(map_hann_names)

	yield """\
static constexpr float *kHannMap[] = {
	%s
};

""" % hann_names

	make_gauss_kernel_fft_name = lambda rows, cols: "{&%s[0][0], &%s[1][0]}" % (common.make_sized_prefix(gauss_kernel_fft.ARRAY_PREFIX, rows, cols), common.make_sized_prefix(gauss_kernel_fft.ARRAY_PREFIX, rows, cols))
	map_gauss_kernel_fft_names = map(lambda win: make_gauss_kernel_fft_name(*win), common.WINDOWS)
	gauss_kernel_fft_names = ',\n\t'.join(map_gauss_kernel_fft_names)

	yield """\
static constexpr std::pair<float *, float *> kGaussKernelFftMap[] = {
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
