#!/usr/bin/env python2.7

import numpy as np
from PIL import Image

# Faster but evals arbitrary python code
Image_array = np.array(eval(open('abc.txt').read()), dtype=np.uint8)

# Slower but safer
# Image_array = np.genfromtxt('abc.txt', dtype=np.uint8, deletechars="[]() ", delimiter=',')

print 'Image_array is {} elements long ({} pixels)'.format(len(Image_array), len(Image_array)/3)

image = Image.fromarray(Image_array.reshape((569, 929, 3)))
image.save('flag.png')
print 'Flag saved in flag.png'
