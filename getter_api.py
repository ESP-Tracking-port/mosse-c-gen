import common

HEADER_PREFIX = "MosseApi.hpp"
CPP_PREFIX = "MosseApi.cpp"
_NL = "\n"
_DNL = "\n\n"


def _header_generate_iter():
	define_before, define_after = common.make_define_sentinel(HEADER_PREFIX)

	yield define_before
	yield "#include <utility>" + _NL
	yield common.CXX_NAMESPACE_BEGIN
	yield "float *getHann(unsigned rows, unsigned cols);" + _NL
	yield "std::pair<float *, float *> getGaussKernelFft(unsigned rows, unsigned cols);" + _DNL
	yield common.CXX_NAMESPACE_END + _NL
	yield define_after


def _cpp_generate_iter():
	yield '#include "GetterApi.hpp"' + _DNL

	make_window_size_pair = lambda rows, cols: "{%d, %d}" % (rows, cols)
	map_window_size_pair = map(lambda win: make_window_size_pair(*win), common.WINDOWS)
	window_size_pairs = ',\n\t'.join(map_window_size_pair)

	yield """\
static constexpr unsigned kWindowSizes[][2] = {
	%s
};
""" % window_size_pairs


def _header_generate():
	return ''.join(_header_generate_iter())


def _cpp_generate():
	return ''.join(_cpp_generate_iter())


def generate_format_savefile():
	generated = _header_generate()
	common.append_file(generated, HEADER_PREFIX)
	generated = _cpp_generate()
	common.append_file(generated, CPP_PREFIX)
