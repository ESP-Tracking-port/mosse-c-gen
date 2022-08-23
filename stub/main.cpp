#include "MosseApi.hpp"

int main(int, char **)
{
	auto kernelFft = Mosse::getGaussKernelFft(50, 80);
	(void)kernelFft;

	return 0;
}
