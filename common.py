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


def _format_complex(val):
	return

def format_array_iter(prefix, generator, nrows, ncols, typestr, isexplicitconstr):
	if isexplicitconstr:
		fmt_cb = lambda v: "%s(%.4f, %.4f)" % (typestr, v.real, v.imag)
	else:
		fmt_cb = lambda v: "%.4f" % v

	if nrows > 1:
		yield "constexpr unsigned %sHeight = %d;  // Number of rows\n" % (prefix, nrows)
		yield "constexpr unsigned %sWidth = %d;  // Number of columns\n" % (prefix, ncols)
		yield 'constexpr %s %s[%sHeight][%sWidth] = {\n' % (typestr, prefix, prefix, prefix)
		yield '\t{'

		for cnt, val in enumerate(generator):
			if cnt % ncols == 0 and cnt != 0:
				yield "},\n\t{"

			yield fmt_cb(val)
			yield ", "

		yield '}\n};\n\n'
	else:
		yield "constexpr unsigned %sLength = %d;\n" % (prefix, ncols)
		yield 'constexpr %s %s[%sLength] = {' % (typestr, prefix, prefix)

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
