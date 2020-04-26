import numpy
from numba import cuda


@cuda.jit
def kernel(io_array):
    # tx = cuda.threadIdx.x
    # ty = cuda.blockIdx.x
    # bw = cuda.blockDim.x

    # pos = (ty * bw) + tx

    pos = cuda.grid(1)

    if pos < io_array.size:
        io_array[pos] *= 2


def main():
    data = numpy.ones(256)
    threadsperblock = 32
    blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock

    kernel[blockspergrid, threadsperblock](data)
    print(data)


if __name__ == "__main__":
    main()
