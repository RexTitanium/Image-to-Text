# Import Modules
import cv2
import pytesseract
from pytesseract import Output

# Specify location of Tesseract Optical Character Recognition Module
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

# Image Read and Convert to grayscale
img = cv2.imread('receipt.png')
gr_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Converting into Binary from Grayscale using Thresholding
th_img = cv2.threshold(gr_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

cv2.imshow('threshold image', th_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Configuring options for tesseract
config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(th_img, output_type = Output.DICT, config=config, lang='eng') # Feeding image to Tesseract

# Displaying regions detected using Tesseract
tb = len(details['text'])
for sn in range(tb):

	if int(float(details['conf'][sn])) >30:

		(x, y, w, h) = (details['left'][sn], details['top'][sn], details['width'][sn],  details['height'][sn])

		th_img = cv2.rectangle(th_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('captured text', th_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Finally Separating words according to line and space
pt = []
wl = []
lw = ''

for word in details['text']:
    if word!='':
        wl.append(word)
        lw = word
    
    if (lw!='' and word == '') or (word==details['text'][-1]):
        pt.append(wl)
        wl = []

# Importing CSV module
import csv

# Saving File in local directory
with open('image2text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(pt)

# Reading File and printing it in terminal window
f = open("image2text.txt", "r")
print(f.read())