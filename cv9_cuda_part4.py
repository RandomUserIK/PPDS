import numpy
import math
from numba import cuda, float32

TPB = 16


@cuda.jit
def kernel(A, B, C):

    sA = cuda.shared.array(shape=(TPB, TPB), dtype=float32)
    sB = cuda.shared.array(shape=(TPB, TPB), dtype=float32)

    x, y = cuda.grid(2)

    if x >= C.shape[0] or y >= C.shape[1]:
        return

    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y

    tmp = 0.0

    for i in range(int(A.shape[1] / TPB)):
        sA[tx, ty] = A[x, ty + i * TPB]
        sB[tx, ty] = B[tx + i * TPB, y]

        cuda.syncthreads()

        for k in range(TPB):
            tmp += sA[tx, k] * sB[k, ty]

        cuda.syncthreads()

        C[x, y] = tmp


def main():
    A = numpy.full((TPB*2, TPB*3), 3, numpy.float)
    B = numpy.full((TPB*3, TPB*1), 4, numpy.float)

    A_global_mem = cuda.to_device(A)
    B_global_mem = cuda.to_device(B)

    C_global_mem = cuda.device_array((A.shape[0], B.shape[1]))

    threadsperblock = (TPB, TPB)
    blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(math.ceil(B.shape[1] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    kernel[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem)

    C = C_global_mem.copy_to_host()

    print(C)


if __name__ == "__main__":
    main()
