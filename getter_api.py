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


def _get_name_list_windows_iter(prefix=None, suffix=None, formatter=None):
	"""
	Iterates over window sizes and generates a formatted version of thos

	If formatter is none, it generates the default sized prefix following the
	naming scheme implicitly defined by `common.make_shared_prefix` method
	"""
	if formatter is None:
		formatter = lambda rows, cols: common.make_sized_prefix(prefix, rows, cols, suffix)

	make_name = lambda rows, cols: formatter(rows, cols)
	map_make_names = map(lambda win: make_name(*win), common.WINDOWS)

	return map_make_names


def _cpp_generate_maps_iter():

	tabulated_list_delimiter = ",\n\t"
	make_window_size_pair = lambda rows, cols: "std::array<unsigned, 2>{%d, %d}" % (rows, cols)
	window_size_pairs = tabulated_list_delimiter.join(_get_name_list_windows_iter(formatter=make_window_size_pair))

	yield """\
static constexpr auto kWindowSizes = makeArray(
	%s
);

""" % window_size_pairs

	hann_names = tabulated_list_delimiter.join(_get_name_list_windows_iter(hann.ARRAY_PREFIX))

	yield """\
static constexpr auto kHannMap = makeArray(
	%s
);

""" % hann_names

	gauss_kernel_fft_names = tabulated_list_delimiter.join(_get_name_list_windows_iter(gauss_kernel_fft.ARRAY_PREFIX, gauss_kernel_fft.ARRAY_SUFFIX_IMREAL))

	yield """\
static constexpr auto kGaussKernelFftMapImReal = makeArray(
	%s
);""" % gauss_kernel_fft_names


def _header_generate():
	return ''.join(_header_generate_iter())


def _cpp_generate():
	return ''.join(_cpp_generate_iter())


def generate_format_savefile():
	generated = _header_generate()
	common.append_file(generated, HEADER_PREFIX)
	generated = _cpp_generate()
	common.append_file(generated, CPP_PREFIX)
