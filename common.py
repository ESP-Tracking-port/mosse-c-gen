def format_array_iter(prefix, generator, nrows, ncols):
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
