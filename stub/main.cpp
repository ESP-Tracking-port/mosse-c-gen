#include "MosseApi.hpp"

int main()
{
	auto kernelFft = Mosse::getGaussKernelFft(50, 80);
	(void)kernelFft;
}
