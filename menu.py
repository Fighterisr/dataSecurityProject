from imageSteganography import *

print('Choose and option:')
choice = input('1. Hide a binary image inside a color image\n'
               '2. Extract a hidden binary image from a stegonographic image\n')
if choice == '1':
    hideImage()
elif choice == '2':
    extractImage()