from imageSteganography import *

print('Choose and option:')
choice = input('1. Hide a binary image inside a color image\n'
               '2. Extract a hidden binary image from a stegonographic image\n'
               '3. Compare two binary images to find if they are the same image\n')
if choice == '1':
    imageEncryption()
elif choice == '2':
    decryptImage()
elif choice == '3':
    comprareSecretImages()
else:
    print('Invalid option')