from PIL import Image




colorImage = Image.open("lena.png").convert('RGB')
binaryImage = Image.open("cats.png").convert('1')
red, green, blue = Image.Image.split(colorImage)
newRed = [bin(i) for i in red.getdata()]
newGreen = [bin(i) for i in green.getdata()]
newBlue = [bin(i) for i in blue.getdata()]
newBinary = [bin(i) for i in binaryImage.getdata()]
bcopy = blue.copy()
rcopy = red.copy()

for i in range(len(newBinary)):
    redLSB = int(newRed[i][-1],2)
    greenLSB = int(newRed[i][-1], 2)
    binaryLSB = int(newRed[i][-1], 2)
    if not binaryLSB ^ redLSB: # when both lsb are 00 or 11
        if not 1 ^ greenLSB:
            newBlue[i] = newBlue[i][:-1] + '1'
        else:
            newBlue[i] = newBlue[i][:-1] + '0'
    else: # when lsb are 01 or 10
        if 0 ^ greenLSB:
            newBlue[i] = newBlue[i][:-1] + '0'
        else:
            newBlue[i] = newBlue[i][:-1] + '1'
newBlue = [int(i,2) for i in newBlue]
blue.putdata(newBlue)
colorImage = Image.merge(colorImage.mode, (red,green,blue))
colorImage.show()

