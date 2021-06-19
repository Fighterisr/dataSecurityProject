# Data Security Project

**Group members:**

* Omri Biton
* Niv Tal
* Eli Manashirov
* Ruslan Borisevich

**Prerequisites:**

* Pillow
```
pip install Pillow
```
* EasyOCR
```
pip install easyocr
```
* PyCryptodome
```
pip install pycryptodome
```
**Instructions:**
Run menu.py and choose an option from the menu by typing its number and press enter:
1. to hide a binary image in a color image
2. to extract a binary image from a steganographic image
3. to compare two secret image and find if they are same image

**Notes:**

* When asked for a file name to save an image, there is no need to type its extension, as it defaults to
.png
  * The same goes for when asked to save text file when extracting text out of an image. defaults to .txt
* Already included files for testing the features are:
    * lena.png - A color image to hide a binary image inside
    * cats.png - A binary image for hiding inside the color
    * textFile.txt - A text file with two lines of text, to hide inside a color image