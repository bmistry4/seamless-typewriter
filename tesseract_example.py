# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import argparse
import os

# construct the argument parse and parse the arguments
def parseArgs():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                    help="type of preprocessing to be done")
    args = vars(ap.parse_args())
    return args

args = parseArgs()

def getOriginalImage():
    return cv2.imread(args["image"])

def convertToGrayScale(image):
    # load the example image and convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def applyPreprocessing(image):
    # check to see if we should apply thresholding to preprocess the
    # image
    if args["preprocess"] == "thresh":
        image = cv2.threshold(image, 0, 255,
                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif args["preprocess"] == "blur":
        image = cv2.medianBlur(image, 3)

    return image

def writeGrayscaleImage(grayImage):

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, grayImage)
    return filename

def applyOCR(filename):
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    # print(text)
    return text

def showIOImages(input, output):
    # show the output images
    cv2.imshow("Image", input)
    cv2.imshow("Output", output)
    cv2.waitKey(0)

if __name__ == '__main__':
    originalImage = getOriginalImage()
    grayscaleImage = convertToGrayScale(originalImage)
    outputImage = applyPreprocessing(grayscaleImage)
    greyFilename = writeGrayscaleImage(outputImage)
    text = applyOCR(greyFilename)
    print("***************************************")
    print(text)
    print("***************************************")
    showIOImages(originalImage, grayscaleImage)