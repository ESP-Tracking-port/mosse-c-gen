SIGMA = 100.0
IMSIZE_2D = (100, 100)
IMCENTER = [i // 2 for i in IMSIZE_2D]
PRECISION = 5
WINDOWS = [(80, 50), (50, 80), (95, 60), (60, 95), (70, 70), (60, 60), (50, 50), (40, 40)]
FNAME = "mosse_constants.hpp"


def format_array_iter(prefix, generator, nrows, ncols):
	if nrows > 1:
		yield "constexpr unsigned %sHeight = %d;  // Number of rows\n" % (prefix, nrows)
		yield "constexpr unsigned %sWidth = %d;  // Number of columns\n" % (prefix, ncols)
		yield 'constexpr float %s[%sHeight][%sWidth] = {\n' % (prefix, prefix, prefix)
		yield '\t{'

		for cnt, val in enumerate(generator()):
			yield "%.4ff" % val

			if cnt % ncols == 0 and cnt != 0:
				yield "},\n\t{"
			else:
				yield ", "

		yield '}\n};'
	else:
		yield "constexpr unsigned %sLength = %d;  //\n" % (prefix, ncols)
		yield 'constexpr float %s[%sLength] = {' % (prefix, prefix)

		for cnt, val in enumerate(generator()):
			yield "%.4ff" % val
			yield ", "

		yield '};\n'
