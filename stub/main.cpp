#include "MosseApi.hpp"

int main(int, char **)
{
	auto kernelFft1 = Mosse::getGaussKernelFftImReal(50, 80);
	auto kernelFft2 = Mosse::getGaussKernelFft3d(50, 80);
	(void)kernelFft1;
	(void)kernelFft2;

	return 0;
}
