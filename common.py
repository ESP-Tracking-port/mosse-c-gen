import os
import pathlib


SIGMA = 100.0
IMSIZE_2D = (100, 100)
IMCENTER = [i // 2 for i in IMSIZE_2D]
PRECISION = 5
WINDOWS = [(80, 50), (50, 80), (95, 60), (60, 95), (70, 70), (60, 60), (50, 50), (40, 40)]
FNAME = "mosse_constants.hpp"
CXX_NAMESPACE = "Mosse"
CXX_NAMESPACE_BEGIN = "namespace %s {\n\n" % CXX_NAMESPACE
CXX_NAMESPACE_END = "}  // namespace %s\n" % CXX_NAMESPACE
ARRAY_2D_SUFFIX_ROWS = "Height"
ARRAY_2D_SUFFIX_COLUMNS = "Width"
ARRAY_1D_SUFFIX_LEN = "Length"
DEFINE_SENTINEL_PREFIX = "MOSSE"


def make_define_sentinel(filename):
	define_sentinel = "%s_%s_" % (DEFINE_SENTINEL_PREFIX, '_'.join(map(lambda s: s.upper(), (filename.split('.')))))

	return "#if !defined(%s)\n#define %s" % (define_sentinel, define_sentinel), "#endif"


def make_sized_prefix(prefix, rows, cols, suffix=None):
	res = "%s%dx%d" % (prefix, rows, cols)

	if suffix is not None:
		res += str(suffix)

	return res


def _format_complex(val):
	return

def format_array_iter(prefix, generator, nrows, ncols, typestr, isexplicitconstr):
	if isexplicitconstr:
		fmt_cb = lambda v: "%s(%.4f, %.4f)" % (typestr, v.real, v.imag)
	else:
		fmt_cb = lambda v: "%.4f" % v

	if nrows > 1:
		yield "constexpr unsigned %s%s = %d;  // Number of rows\n" % (prefix, ARRAY_2D_SUFFIX_ROWS, nrows)
		yield "constexpr unsigned %s%s = %d;  // Number of columns\n" % (prefix, ARRAY_2D_SUFFIX_COLUMNS, ncols)
		yield 'constexpr %s %s[%s%s][%s%s] = {\n' % (typestr, prefix, prefix, ARRAY_2D_SUFFIX_ROWS, prefix, ARRAY_2D_SUFFIX_COLUMNS)
		yield '\t{'

		for cnt, val in enumerate(generator):
			if cnt % ncols == 0 and cnt != 0:
				yield "},\n\t{"

			yield fmt_cb(val)
			yield ", "

		yield '}\n};\n\n'
	else:
		yield "constexpr unsigned %s%s = %d;\n" % (prefix, ARRAY_1D_SUFFIX_LEN, ncols)
		yield 'constexpr %s %s[%s%s] = {' % (typestr, prefix, prefix, ARRAY_1D_SUFFIX_LEN)

		for cnt, val in enumerate(generator):
			yield fmt_cb(val)
			yield ", "

		yield '};\n\n'


def append_file(appendix, fname=FNAME):

	if not os.path.exists(fname):
		mode = 0o774
		path = pathlib.Path(str(fname)).parent.resolve()

		if pathlib.Path(__file__).parent.resolve() != path and not os.path.exists(path):
			os.makedirs(str(path), mode)

		with open(fname, 'w') as f:
			pass

	with open(fname, "a") as f:
		f.write(appendix)
