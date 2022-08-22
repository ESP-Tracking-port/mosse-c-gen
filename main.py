import common
import gauss_kernel_fft
import gauss_kernel
import hann


def main():
	gauss_kernel.generate_format_savefile(*common.IMSIZE_2D)

	for window in common.WINDOWS:
		gauss_kernel_fft.generate_format_savefile(*window)
		hann.generate_format_savefile(*window)


if __name__ == "__main__":
	main()
