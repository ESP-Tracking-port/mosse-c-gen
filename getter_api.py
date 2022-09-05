import common
import main
import hann
import gauss_kernel_fft
import pathlib
import log_matrix


HEADER_PREFIX = common.OUTPUT_DIR + "MosseApi.hpp"
CPP_PREFIX = common.OUTPUT_DIR + "MosseApi.cpp"
HEADER_DEBUG_PREFIX = common.OUTPUT_DIR + "MosseApiDebug.hpp"
SOURCE_PREFIX = "MosseApi"
_MAPS_MARKER = "@MAPS@"
_NAMESPACE_MARKER = "@MOSSENAMESPACE@"
_GAUSS_KERNEL_GETTERS_DECL = "@GAUSS_KERNEL_SCALED_GETTERS_DECL@"
_GAUSS_KERNEL_GETTERS_DEF_MARKER = "@GAUSS_KERNEL_GETTERS_DEF@"
_MARKER_DICT = {
	"@DEBUGSELECT@" : common.DEBUG_SELECT,
	_NAMESPACE_MARKER: common.CXX_NAMESPACE,
	"@LOG_TABLE_RAW@": log_matrix.ARRAY_PREFIX,
	_GAUSS_KERNEL_GETTERS_DECL: "",
}
_GAUSS_KERNEL_GETTER_PREFIX = "getGaussKernelFft"


def _header_generate_iter():
	_header_gauss_kernel_getters_generate()
	path = str(pathlib.Path() / "stub" / "MosseApi") + ".hpp.stub"
	res = common.file_configure_append(path, _MARKER_DICT)

	yield res


def _header_gauss_kernel_getters_generate_iter():
	_MARKER_DICT[_GAUSS_KERNEL_GETTERS_DECL] = ""

	for scale, suffix in gauss_kernel_fft.SCALED:
		yield "const float *%s%s(unsigned aRows, unsigned aCols);\n" % (_GAUSS_KERNEL_GETTER_PREFIX, suffix)


def _header_gauss_kernel_getters_generate():
	_MARKER_DICT[_GAUSS_KERNEL_GETTERS_DECL] = ''.join(
		_header_gauss_kernel_getters_generate_iter())


def _header_debug_generate():
	path = common.file_configure_append("stub/MosseApiDebug.hpp.stub", _MARKER_DICT, HEADER_DEBUG_PREFIX)


def _cpp_generate_iter():
	filename = str(pathlib.Path() / "stub" / "MosseApi") + ".cpp.stub"
	maps = _cpp_generate_maps()
	_MARKER_DICT[_MAPS_MARKER] = maps
	_MARKER_DICT[_GAUSS_KERNEL_GETTERS_DEF_MARKER] =_cpp_generate_getters()

	yield common.file_configure_append(filename, _MARKER_DICT)


def _cpp_generate_getters():

	def _cpp_generate_getters_iter():
		for scale, suffix in gauss_kernel_fft.SCALED:
			yield """\
const float *%s%s(unsigned &aRows, unsigned &aCols)
{
	int id = checkWindowExists(aRows, aCols);

	if (id < 0) {
		return nullptr;
	}

	return %s%s[id];
}

""" % (_GAUSS_KERNEL_GETTER_PREFIX, suffix, gauss_kernel_fft.ARRAY_PREFIX, suffix)

	return ''.join(_cpp_generate_getters_iter())


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

	hann_names = tabulated_list_delimiter.join(_get_name_list_windows_iter(hann.ARRAY_PREFIX, common.ARRAY_SUFFIX_RAW))

	yield """\
static constexpr auto kHannMap = makeArray(
	%s
);

""" % hann_names

	for scale, suffix in gauss_kernel_fft.SCALED:
		gauss_kernel_fft_names_scaled = tabulated_list_delimiter.join(
			_get_name_list_windows_iter(gauss_kernel_fft.ARRAY_PREFIX, suffix + common.ARRAY_SUFFIX_RAW)
		)

		yield """\
static constexpr auto %s%s = makeArray(
	%s
);

""" % (gauss_kernel_fft.ARRAY_PREFIX, suffix, gauss_kernel_fft_names_scaled)

	make_gauss_fft_name = lambda rows, cols: common.make_sized_prefix(gauss_kernel_fft.ARRAY_PREFIX, rows, cols, gauss_kernel_fft.ARRAY_SUFFIX_IMREAL)
	make_gauss_fft_pair = lambda rows, cols: "std::pair<const float *, const float *>{&%s[0][0], &%s[1][0]}" % (make_gauss_fft_name(rows, cols), make_gauss_fft_name(rows, cols))
	gauss_kernel_fft_names = tabulated_list_delimiter.join(_get_name_list_windows_iter(formatter=make_gauss_fft_pair))

	yield """\
static constexpr auto kGaussKernelFftMapImReal = makeArray(
	%s
);

""" % gauss_kernel_fft_names

	make_gauss_fft_name = lambda rows, cols: common.make_sized_prefix(gauss_kernel_fft.ARRAY_PREFIX, rows, cols, gauss_kernel_fft.ARRAY_SUFFIX_IMREAL_3D + common.ARRAY_SUFFIX_RAW)
	make_gauss_fft_pair = lambda rows, cols: "%s" % (make_gauss_fft_name(rows, cols))
	gauss_kernel_fft_names = tabulated_list_delimiter.join(_get_name_list_windows_iter(formatter=make_gauss_fft_pair))

	yield """\
static constexpr auto kGaussKernelFftMapImReal3d = makeArray(
	%s
);
""" % gauss_kernel_fft_names


def _header_generate():
	return ''.join(_header_generate_iter())


def _cpp_generate():
	return ''.join(_cpp_generate_iter())


def generate_format_savefile():
	generated = _header_generate()
	common.append_file(generated, HEADER_PREFIX)
	generated = _cpp_generate()
	common.append_file(generated, CPP_PREFIX)
	_header_debug_generate()
