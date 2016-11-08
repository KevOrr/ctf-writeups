#!/usr/bin/env python3

from PIL import Image

STRIP_WIDTH = 504
STRIP_HEIGHT = 8
SHIFT_PER_LINE = 8

in_img = Image.open('warp_speed.jpg')
straightened_img = Image.new(in_img.mode, in_img.size)
collated_img = Image.new(in_img.mode, (in_img.size[0] // 2, in_img.size[1] * 2))


# Straighten out image
x_shift = 0
top_edge = 0
while x_shift < in_img.size[1]:

    # On the right in challenge, originally left
    left_strip = in_img.crop((x_shift, top_edge, in_img.size[0], top_edge + STRIP_HEIGHT))
    left_strip.load()
    straightened_img.paste(left_strip, (0, top_edge, in_img.size[0] - x_shift, top_edge + STRIP_HEIGHT))

    # On the left in challenge, orignally right
    right_strip = in_img.crop((0, top_edge, x_shift, top_edge + STRIP_HEIGHT))
    right_strip.load()
    straightened_img.paste(right_strip, (in_img.size[0] - x_shift, top_edge, in_img.size[0], top_edge + STRIP_HEIGHT))

    x_shift = (x_shift + SHIFT_PER_LINE) % in_img.size[0]
    top_edge += STRIP_HEIGHT

# Collate rows
line = 0
top_edge = 0
while top_edge < straightened_img.size[1]:
    left_edge = 0 if line % 2 == 0 else STRIP_WIDTH
    strip = straightened_img.crop((left_edge, top_edge, left_edge + STRIP_WIDTH, top_edge + STRIP_HEIGHT))
    strip.load()
    collated_img.paste(strip, (0, line * STRIP_HEIGHT, STRIP_WIDTH, (line+1) * STRIP_HEIGHT))

    line += 1
    top_edge = top_edge + STRIP_HEIGHT if line % 2 == 0 else top_edge

# Finally rotate
final_img = collated_img.rotate(90)

final_img.save('new_im.png')

