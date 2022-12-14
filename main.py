import common
import gauss_kernel_fft
import gauss_kernel
import hann
import getter_api
import os
import cmakelists
import log_matrix


GAUSS_KERNEL_GENERATE = False
HANN_PREFIX = "Hann"
GAUSS_PREFIX = "GaussKernel"
GAUSS_FFT_PREFIX = "GaussKernelFft"
WINDOW_SIZES_ROWS_COLS = common.WINDOWS
MAIN_HEADER_PREFIX = "MosseTables.hpp"


def _make_filename(prefix, windowsize):
	return "%s%dx%d.hpp" % (prefix, *windowsize)


def main_header_generate_format_iter():
	prefixes = [HANN_PREFIX, GAUSS_FFT_PREFIX]
	define_before, define_after = common.make_define_sentinel(MAIN_HEADER_PREFIX)

	yield define_before

	if GAUSS_KERNEL_GENERATE:
		prefixes.append(GAUSS_PREFIX)

	yield "#include <complex>\n"

	for prefix in prefixes:
		for windowsize in WINDOW_SIZES_ROWS_COLS:
			yield "#include \"%s\"\n" % (_make_filename(prefix, windowsize))

	yield "#include \"%s\"\n" % log_matrix.INCLUDE_PATH
	yield "\n"
	yield define_after
	yield "\n"


def main_header_generate_format_savefile():
	generated = ''.join(main_header_generate_format_iter())
	common.append_file(generated, common.GEN_DIR_PREFIX + MAIN_HEADER_PREFIX)


def main():
	main_header_generate_format_savefile()
	getter_api.generate_format_savefile()
	cmakelists.generate_format_savefile()
	log_matrix.generate_format_savefile()

	if GAUSS_KERNEL_GENERATE:
		gauss_kernel.generate_format_savefile(*common.IMSIZE_2D, GAUSS_PREFIX)

	for window in WINDOW_SIZES_ROWS_COLS:
		gauss_kernel_fft.generate_format_savefile(*window, _make_filename(common.GEN_DIR_PREFIX + GAUSS_FFT_PREFIX, window))
		hann.generate_format_savefile(*window, _make_filename(common.GEN_DIR_PREFIX + HANN_PREFIX, window))


if __name__ == "__main__":
	main()
