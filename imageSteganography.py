from PIL import Image, PngImagePlugin, ImageFont, ImageDraw
import easyocr
import hashlib

def imageEncryption():
    def hideImage(colorImage, binaryImage):
        info = PngImagePlugin.PngInfo()

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
        return colorImage, info

    while True:
        firstImageName = input("Color image name: ")
        try:
            colorImage = Image.open(firstImageName).convert('RGB')
            break
        except (FileNotFoundError, AttributeError):
            print('File name does not exist, try again.')
    isTextMode = input("To read text from txt file type 'y', else type 'n': ")
    if isTextMode in ['y', 'Y']:
        while True:
            textFileName = input("Text file name: ")
            try:
                with open(textFileName) as textFile:
                    lines = textFile.read()
                break
            except (FileNotFoundError, AttributeError):
                print('File name does not exist, try again.')
        selectedFont = ImageFont.truetype('arial.ttf')
        binaryImage = Image.new('1', (300, 300), color='white')
        image_editable = ImageDraw.Draw(binaryImage)
        image_editable.text((0, 0), lines, font=selectedFont)
    else:
        while True:
            binaryImageName = input("Binary image name: ")
            try:
                binaryImage = Image.open(binaryImageName).convert('1')
                break
            except (FileNotFoundError, AttributeError):
                print('File name does not exist, try again.')
    imageTuple = hideImage(colorImage, binaryImage)
    saveImageName = input("Enter image file name to save as: ")
    Image.Image.save(imageTuple[0],saveImageName + '.png', pnginfo= imageTuple[1])

def decryptImage():
    def extractImage(stegoImage):
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
        return img

    while True:
        stegoImageName = input("Stegonographic image file name: ")
        try:
            stegoImage = Image.open(stegoImageName)
            break
        except (FileNotFoundError, AttributeError):
            print('File name does not exist, try again.')
    secretImage = extractImage(stegoImage)
    secretImageName = input("Enter image file name to save as: ")
    secretImage.save(secretImageName + '.png')
    ocrAnswer = input("To extract text from the secret image, type 'y', else type 'n': ")
    if ocrAnswer in ['y', 'Y']:
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(secretImageName + '.png')
        textResult = ''
        if len(result):
            for i in result:
                textResult = textResult + i[1] + '\n'
            textFileName = input("Enter text file name: ")
            with open(textFileName, 'w') as textFile:
                textFile.write(textResult)
            print("The text has been extracted and written into " + textFileName)
        else:
            print("No text detected in the image")





def comprareSecretImages():
    print("Please enter file names of both images and their extension (eg: jpg, png)")
    while True:
        firstImageName = input("First image name: ")
        try:
            firstImage = Image.open(firstImageName).convert('1')
            break
        except (FileNotFoundError, AttributeError):
            print('File name does not exist, try again.')
    while True:
        secondImageName = input("second image name: ")
        try:
            secondImage = Image.open(secondImageName).convert('1')
            break
        except (FileNotFoundError, AttributeError):
            print('File name does not exist, try again.')


    originalImageHash = hashlib.blake2b(firstImage.tobytes())
    resultImageHash = hashlib.blake2b(secondImage.tobytes())

    isSameImage = originalImageHash.digest() == resultImageHash.digest()
    if isSameImage:
        print('Same image')
    else:
        print('Different images')

