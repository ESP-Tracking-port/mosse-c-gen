import common
import gauss_kernel_fft
import gauss_kernel
import hann


GEN_DIR_PREFIX = "Mosse/"
GAUSS_KERNEL_GENERATE = False
HANN_PREFIX = GEN_DIR_PREFIX + "Hann"
GAUSS_PREFIX = GEN_DIR_PREFIX + "GaussKernel"
GAUSS_FFT_PREFIX = GEN_DIR_PREFIX + "GaussKernelFft"
WINDOW_SIZES_ROWS_COLS = common.WINDOWS
MAIN_HEADER_PREFIX = GEN_DIR_PREFIX + "MosseTables.hpp"


def _make_filename(prefix, windowsize):
	return "%s%dx%d.hpp" % (prefix, *windowsize)


def main_header_generate_format_iter():
	prefixes = [HANN_PREFIX, GAUSS_FFT_PREFIX]

	if GAUSS_KERNEL_GENERATE:
		prefixes.append(GAUSS_PREFIX)

	for prefix in prefixes:
		for windowsize in WINDOW_SIZES_ROWS_COLS:
			yield "#include \"%s\"\n" % _make_filename(prefix, windowsize)

	yield "\n"


def main_header_generate_format_savefile():
	generated = ''.join(main_header_generate_format_iter())
	common.append_file(generated, MAIN_HEADER_PREFIX)


def main():
	main_header_generate_format_savefile()

	if GAUSS_KERNEL_GENERATE:
		gauss_kernel.generate_format_savefile(*common.IMSIZE_2D, GAUSS_PREFIX)

	for window in WINDOW_SIZES_ROWS_COLS:
		gauss_kernel_fft.generate_format_savefile(*window, _make_filename(GAUSS_FFT_PREFIX, window))
		hann.generate_format_savefile(*window, _make_filename(HANN_PREFIX, window))


if __name__ == "__main__":
	main()
