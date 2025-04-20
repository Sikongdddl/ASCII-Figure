# Work Introduction

Hi there! Here is a basic implementation of ASCII figures. We use different characters to implace pixels in figure, where the thinner and smaller character meets the brighter part of a figure.

Welcome to discuss with me! I'm glad to improve my own job or make your idea come true.
# Branch Introduction
#### main:
coloful version. Input a figure and output the ASCII version. 

#### grid:
initial grid version with some interesting MSE methods. The output figure is similar both in grid brightness and in shape, which makes the output easier to be recognized.

#### realtime:
use your own camera with opencv and parse the input of camera to grid version.
You can tradeoff between FPS and resolutions by changing the block size. Bigger block size transfer a larger area of input image to a ASCII character, leading to faster parsing ,higher FPS but lower resolutions.