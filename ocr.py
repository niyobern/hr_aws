# # text recognition
# import cv2
# import pytesseract

# # read image
# img = cv2.imread('quotes.jpg')

# # configurations
# config = ('-l eng --oem 1 --psm 3')

# # pytessercat
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# text = pytesseract.image_to_string(img, config=config)

# # print text
# text = text.split('\n')
# print(text)