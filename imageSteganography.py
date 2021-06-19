from PIL import Image, PngImagePlugin, ImageFont, ImageDraw
import easyocr
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

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
    isTextMode = input("To read text from txt file type 'y', else type 'n' to use a binary image: ")
    if isTextMode in ['y', 'Y']:
        while True:
            textFileName = input("Text file name: ")
            try:
                with open(textFileName) as textFile:
                    lines = textFile.read()
                break
            except (FileNotFoundError, AttributeError):
                print('File name does not exist, try again.')
        selectedFont = ImageFont.truetype('arial.ttf', 20)
        binaryImage = Image.new('1', (400, 400), color='white')
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
    stegoImage, info = hideImage(colorImage, binaryImage)
    isStegoEncrypt = input("To encrypt the stegonographic image, type 'y', else type 'n': ")
    if isStegoEncrypt in ['y', 'Y']:
        key = Random.new().read(AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        stegoBytes = stegoImage.tobytes()
        stegoBytes = cipher.encrypt(stegoBytes)
        stegoImage.frombytes(stegoBytes)
        info.add_text('key', key.decode('latin1')) # latin1 is compatible with aes key
        info.add_text('iv', iv.decode('latin1'))
    if isTextMode in ['y', 'Y']: info.add_text('ocr', 'yes') # Ask if to do ocr only if necessary
    saveImageName = input("Enter image file name to save as (without extension): ")
    Image.Image.save(stegoImage, saveImageName + '.png', pnginfo = info)

def decryptImage():
    def extractImage(stegoImage):
        if 'key' in stegoImage.text:
            print('Encrypted stegonographic image has been detected. Decrypting...')
            key, iv = stegoImage.text['key'].encode('latin1'), stegoImage.text['iv'].encode('latin1')
            cipher = AES.new(key, AES.MODE_CFB, iv)
            stegoBytes = stegoImage.tobytes()
            stegoBytes = cipher.decrypt(stegoBytes)
            stegoImage.frombytes(stegoBytes)
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
    secretImageName = input("Enter image file name to save as (without extension): ")
    secretImage.save(secretImageName + '.png')
    if 'ocr' in stegoImage.text:
        ocrAnswer = input("To extract text from the secret image, type 'y', else type 'n': ")
        if ocrAnswer in ['y', 'Y']:
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext(secretImageName + '.png')
            textResult = ''
            if len(result):
                for i in result:
                    textResult = textResult + i[1] + '\n'
                textFileName = input("Enter text file name (without txt extension): ")
                with open(textFileName + '.txt', 'w') as textFile:
                    textFile.write(textResult)
                print("The text has been extracted and written into " + textFileName + ".txt")
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

