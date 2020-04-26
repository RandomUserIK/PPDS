import numpy
from numba import cuda
from pylab import imshow, show
from timeit import default_timer as timer

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    c = complex(x, y)
    z = 0.0j

    for i in range(max_iters):
        z = z * z + c
        if(z.real * z.real + z.imag * z.imag) >= 4:
            return i
    return max_iters


@cuda.jit
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    startX, startY = cuda.grid(2)
    gridX = cuda.gridDim.x * cuda.blockDim.x
    gridY = cuda.gridDim.y * cuda.blockDim.y

    for x in range(startX, width, gridX):
        real = min_x + x * pixel_size_x

        for y in range(startY, height, gridY):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color


def main():
    image = numpy.zeros((1080, 1920), dtype=numpy.uint8)
    blockdim = (32, 8)
    griddim = (32, 8)

    d_image = cuda.to_device(image)

    start = timer()
    create_fractal[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, d_image, 20)
    df = timer() - start

    d_image.to_host()

    print(f'Time duration using CUDA: {df:.5f}')

    imshow(image)
    show()


if __name__ == "__main__":
    main()
