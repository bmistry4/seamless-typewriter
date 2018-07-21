# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import argparse
import os


# construct the argument parse and parse the arguments
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                    help="type of preprocessing to be done")
    args = vars(ap.parse_args())
    return args


args = parse_args()


def get_original_image():
    return cv2.imread(args["image"])


def convert_to_gray_scale(image):
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


def write_grayscale_image(grayImage):
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, grayImage)
    return filename


def apply_ocr(filename):
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    # print(text)
    return text


def show_io_images(input, output):
    # show the output images
    cv2.imshow("Image", input)
    cv2.imshow("Output", output)
    cv2.waitKey(0)


if __name__ == '__main__':
    original_image = get_original_image()
    grayscale_image = convert_to_gray_scale(original_image)
    outputImage = applyPreprocessing(grayscale_image)
    greyFilename = write_grayscale_image(outputImage)
    text = apply_ocr(greyFilename)
    print("***************************************")
    print(text)
    print("***************************************")
    show_io_images(original_image, grayscale_image)
