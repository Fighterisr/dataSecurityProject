from PIL import Image, PngImagePlugin

def hideImage():
    info = PngImagePlugin.PngInfo()
    colorImage = Image.open("lena.png").convert('RGB')
    binaryImage = Image.open("cats.png").convert('1')
    red, green, blue = Image.Image.split(colorImage)
    newRed = [bin(i) for i in red.getdata()]
    newGreen = [bin(i) for i in green.getdata()]
    newBlue = [bin(i) for i in blue.getdata()]
    newBinary = [bin(i) for i in binaryImage.getdata()]

    for i in range(len(newBinary)):
        redLSB = int(newRed[i][-1],2)
        greenLSB = int(newGreen[i][-1], 2)
        binaryLSB = int(newBinary[i][-1], 2)
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
    binWidth, binHeight = binaryImage.size
    info.add_text('binWidth', str(binWidth))
    info.add_text('binHeight', str(binHeight))
    colorImage.save("stegoImage.png", pnginfo = info)









def extractImage():
    stegoImage = Image.open("stegoImage.png")
    secretImage = []
    red, green, blue = Image.Image.split(stegoImage)
    newRed = [bin(i) for i in red.getdata()]
    newGreen = [bin(i) for i in green.getdata()]
    newBlue = [bin(i) for i in blue.getdata()]

    for i in range(len(newBlue)):
        redLSB = int(newRed[i][-1], 2)
        greenLSB = int(newGreen[i][-1], 2)
        blueLSB = int(newBlue[i][-1], 2)
        if not blueLSB ^ greenLSB: # blue and green lsb are 00 or 11
            if not 1 ^ redLSB:
                secretImage.append(1)
            else:
                secretImage.append(0)
        else: # 01 or 10
            if 0 ^ redLSB:
                secretImage.append(0)
            else:
                secretImage.append(1)

    binWidth, binHeight = int(stegoImage.text['binWidth']), int(stegoImage.text['binHeight'])
    binPixels = binWidth * binHeight
    secretImage = secretImage[:binPixels]
    img = Image.new('1', (binWidth, binHeight))
    img.putdata(secretImage)
    img.save('secretImage.png')

