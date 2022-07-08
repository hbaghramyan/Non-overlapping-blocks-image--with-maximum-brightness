import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from skimage.util import view_as_blocks
import copy

def fmaxblocks(s, arr):
    """A function that finds the group of 4 non-overlapping blocks with maximum 
    sum of their means"""
    
    # arr is a 2D grayscale image
    # s is the side of the patch
    
    # getting the shape of arr
    m = arr.shape[0] 
    n = arr.shape[1]
    
    # Here, we convert an array with identical values to 
    # an array with all equal to 1. This is important, since
    # the test can be with an array with all zero entries
    if np.all(arr == np.ravel(arr)[0]):
        arr = np.ones((m, n))
    
    # Building a 4D matrix that contains all the possible sxs blocks in the original "arr" matrix
    i = 1 + (m-s)
    j = 1 + (n-s)
    arrblock = np.lib.stride_tricks.as_strided(arr, shape=(i, j, s, s), strides = arr.strides + arr.strides)

    # Finding all mean values of sxs blocks
    arrblockmean = arrblock.sum(axis = (2, 3))/s**2
    # Creating a copy of "arrblockmean"
    blockmeantemp = copy.deepcopy(arrblockmean)

    # shape of the "blockmeantemp"
    mb, nb = blockmeantemp.shape

    # sorting the "blockmeantemp". 
    # The array is reshaped into a vector and sorted.
    # It is crusial to use "mergesort",
    # otherwise the algorithm may search for the maximum at the edges of array
    # This could happen with a sparse matrix or a matrix with many identical values
    arr01 = blockmeantemp.reshape(1, -1)
    sorted1d = -np.sort(-arr01, kind='mergesort')
    # sorted2d = sorted1d.reshape(mb, nb) # sorted array

    # finding the incides for the elements in "blockmeantemp"
    # in accorandance of their appearance in "sorted1d"
    arrarg01 = np.argsort(-arr01, kind='mergesort')
    fidx = np.unravel_index(arrarg01, blockmeantemp.shape)
    blmnidx = np.asarray(fidx, dtype = int).reshape(2, mb*nb).T # orignal indices in "blockmeantemp"

    # a variable for the sum of 4 maximal means
    maxsum = 0

    # an array for the incides of maximal elements in "blockmeantemp"
    coor = np.zeros((4, 2), dtype = int)
    
    for idx, elem in enumerate(sorted1d[0]):
    
        # the candidate value variable for the sum
        candmaxsum = 0

        # counter variable to check if all coordinate checkings are done
        count = 0

        nidx = idx # the index for the next element in sorted1d[0]
        nidx += 1

        # condition to break the search if less than 3 blocks remain or 
        # the current element times 4 is less than or equal the sum
        # of the previous 4 means of non-overlapping blocks (given by maxsum)
        if nidx > (nb*mb - 3) or (elem*4 <= maxsum):
            break

        # increamenting candmaxsum
        candmaxsum += sorted1d[0][idx]

        # checking if the two patches overlap in the original "arr"
        # 2 patches in "arr" overlap if 

        # coordinates of idx'th  
        x01 = blmnidx[idx, 0]
        y01 = blmnidx[idx, 1]
        # and nidx'th 2 patches overlap in "blockmeantemp"
        x02 = blmnidx[nidx, 0]
        y02 = blmnidx[nidx, 1]

        # the loop stops when the idx'th and nidx'th blocks overlap
        while intersect02(x01, y01, x02, y02, s):

            nidx += 1

            if nidx > (nb*mb - 3):
                break

            x02 = blmnidx[nidx, 0]
            y02 = blmnidx[nidx, 1]

        # condition to break the search if less than 2 blocks remain
        if nidx > (nb*mb - 2):
            break

        # increment the count only if 2 the idx'th and nidx'th blocks do not overlap
        if not(intersect02(x01, y01, x02, y02, s)):
            count += 1

        candmaxsum += sorted1d[0][nidx]

        # passing to the next index after "nidx"
        nidx += 1

        # the candidate incides for the 3rd block
        x03 = blmnidx[nidx, 0]
        y03 = blmnidx[nidx, 1]

        # the loop stops if the first 3 blocks in a group of 4 do not overlap
        while (intersect02(x01, y01, x03, y03, s) or intersect02(x02, y02, x03, y03, s)):

            nidx += 1

            if nidx > (nb*mb - 2):
                break

            x03 = blmnidx[nidx, 0]
            y03 = blmnidx[nidx, 1]

        # condition to break the search if less than 1 block remains
        if nidx > (nb*mb - 1):
            break

        # increment the count only if the first 3 blocks in a group of 4 do not overlap 
        if not(intersect02(x01, y01, x03, y03, s) or intersect02(x02, y02, x03, y03, s)):
            count += 1

        candmaxsum += sorted1d[0][nidx]

        nidx += 1

        # the candidate incides for the 4rd block
        x04 = blmnidx[nidx, 0]
        y04 = blmnidx[nidx, 1]

        # the loop stops if all 4 blocks in a group of 4 do not overlap
        while (intersect02(x01, y01, x04, y04, s) or intersect02(x02, y02, x04, y04, s) or intersect02(x03, y03, x04, y04, s)):

            nidx += 1

            if nidx > (nb*mb - 1):
                break

            x04 = blmnidx[nidx, 0]
            y04 = blmnidx[nidx, 1]

        # condition to break the search if less than 1 block remains
        if nidx > (nb*mb - 1):
                break

        # increment the count only if all 4 blocks in a group of 4 do not overlap 
        if not(intersect02(x01, y01, x04, y04, s) or intersect02(x02, y02, x04, y04, s) or intersect02(x03, y03, x04, y04, s)):
            count += 1

        candmaxsum += sorted1d[0][nidx]

        # updating candmaxsum if it is greater than the sum of the means
        # of the previous 4 blocks and if count is 3
        if candmaxsum > maxsum and count == 3:
            # print(maxsum)
            maxsum = candmaxsum
            coor = np.array([[x01, y01], [x02, y02], [x03, y03], [x04, y04]])
            
    # original incides in "arr", and converting them to pixel coordinates
    origcoor = ((2*coor + s - 1)/2).astype(int)
    origcoor[:,[0, 1]] = origcoor[:,[1, 0]]
    
    return origcoor

def intersect02(x01, y01, x02, y02, s):
    """to check if the patches overlap"""
    # x01, y01, x02, y02 are the coordinates of the patches in the 
    if (np.abs(x01 - x02) < s) and (np.abs(y01 - y02) < s):
        return True
    else:
        return False
    
def plot_area(s, arr, fname):
    """To plot the red quadrilaterl on the image"""
    
    # arr is a 2D grayscale image
    # s is the side of the patch
    
    # getting the shape of arr
    m = arr.shape[0] 
    n = arr.shape[1]
    
    if m*n < 4*s**2 or m < s or n < s:
        print(f"The image cannot have 4 {s}x{s} non-overlapping patches.")
        return
    
    # getting the corners of the quadrilateral from the function fmaxblocks
    points = fmaxblocks(s, arr)
    # sorting the corners, so that cv2.fillPoly will iterate over them row-wise 
    points = points[points[:, 0].argsort(kind='mergesort')]
    # taking the first 3 corners
    points01 = points[:3,:]
    # taking the last 3 corners
    points02 = points[1:4,:]
    # converting the 2D grayscale into 3D
    imgbw3D = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    # plotting two triangles
    imgconv = cv2.fillPoly(imgbw3D, pts=[points01], color=(255, 0, 0))
    imgconv = cv2.fillPoly(imgbw3D, pts=[points02], color=(255, 0, 0))
    # Displaying the image
    plt.axis('off')
    plt.imshow(imgconv);
    # Saving the image in png formate
    plt.savefig(fname+'_patch.png');
    # Calculating the area in pixels by counting all the red points.
    area = (imgconv.reshape(-1, 3) == [255, 0, 0]).prod(axis = 1).sum()
    print(f"The area in pixels is: {area}")
    print(f"The points as pixel coordinates are: \n{points}")