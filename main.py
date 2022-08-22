import common
import gauss_kernel_fft
import gauss_kernel
import hann


GAUSS_KERNEL_GENERATE = False


def main():
	if GAUSS_KERNEL_GENERATE:
		gauss_kernel.generate_format_savefile(*common.IMSIZE_2D, common.FNAME)

	for window in common.WINDOWS:
		gauss_kernel_fft.generate_format_savefile(*window, common.FNAME)
		hann.generate_format_savefile(*window, common.FNAME)


if __name__ == "__main__":
	main()
