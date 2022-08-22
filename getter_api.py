import common

HEADER_PREFIX = "MosseApi.hpp"
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


def _header_generate():
	return ''.join(_header_generate_iter())


def generate_format_savefile():
	generated = _header_generate()
	common.append_file(generated, HEADER_PREFIX)
