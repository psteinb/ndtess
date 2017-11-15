
import pytest
import numpy as np

from . import tesselations as tess

np.random.seed(1307) #the zip code of the MPI CBG

@pytest.fixture(scope="module")
def load_synthetic():

    #populate squares, lines and circles at random positions
    img = np.zeros((16,16),dtype=np.float16)

    #a rectangle of intensity 42
    img[11:15, 1:5] = 42

    #a circle at (15,15) with radius = 10 of intensity 30
    radius = 4
    for y in range(0,16):
        for x in range(0,16):
            y_extend = y - 4
            x_extend = x - 12
            if ((x_extend**2)+(y_extend**2)) < radius**2:
                img[y,x] = 100


    #distimg can be any distribution of non-zero floating point numbers
    distimg = np.random.rand(*img.shape)*3.3
    cdi = np.zeros_like(img).astype("float32")
    cdi[:] = 3.3 #some number


    sinargs = np.linspace(0,1,num=img.size).reshape(img.shape)
    sindistimg = np.sin( sinargs ) + .1

    return { 'img' : img, 'di' : distimg, 'cdi' : cdi, 'sindi' : sindistimg }


def test_heapq_init_from_zeroes(load_synthetic):
    """
    run the tesselation on a labelled image where all objects have been identified already (null test)
    """
    di = np.zeros_like(load_synthetic["img"]).astype("float32")
    q = tess.initialize_heapq(load_synthetic["img"],di)

    # with open("py_array.txt","w") as f:
    #     for y in range(16):
    #         f.write("".join([ ("%4.0i" % int(item)) for item in list(load_synthetic["img"][y,:])] ))
    #         f.write("\n")

    assert q[0]
    assert q[0][-1] == 100.
    print("# from_0s > ",q[0], len(q))


def test_heapq_init_from_constant(load_synthetic):
    """
    run the tesselation on a labelled image where all objects have been identified already (null test)
    """

    assert load_synthetic["cdi"].shape == load_synthetic["img"].shape
    assert np.allclose(load_synthetic["cdi"], 3.3)

    q = tess.initialize_heapq(load_synthetic["img"],
                              load_synthetic["cdi"])


    assert q[0]
    assert q[0][-1] == 100.
    print("# from_constant > ",q[0], len(q))


def test_heapq_init_from_sinus(load_synthetic):
    """
    run the tesselation on a labelled image where all objects have been identified already (null test)
    """

    assert load_synthetic["cdi"].shape == load_synthetic["img"].shape

    q = tess.initialize_heapq(load_synthetic["img"],
                              load_synthetic["sindi"])


    assert q[0]
    assert q[0][-1] == 100.
    assert q[0][1] == 0
    assert q[0][2] == 10
    print("# from_sinus > ",q[0], len(q))

def test_heapq_init_from_random(load_synthetic):
    """
    run the tesselation on a labelled image where all objects have been identified already (null test)
    """

    assert load_synthetic["cdi"].shape == load_synthetic["img"].shape

    q = tess.initialize_heapq(load_synthetic["img"],
                              load_synthetic["di"])


    assert q[0]
    assert q[0][-1] == 100.
    assert q[0][1] == 7
    assert q[0][2] == 15


    for i in range(5):
        t = q.heappop()
        print("# from_random [%2i/%2i] %4f %2i %2i %4f" % i, len(q),t[0],t[1],t[2],t[3])
