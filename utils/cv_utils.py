import cv2 as cv

"""
import numpy as np
print("OpenCV:", cv.__version__)
img = np.zeros((120, 400, 3), dtype=np.uint8)
print(type(img))
cv.putText(img, "OpenCV OK", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
# If you installed a non-headless build, you can display a window:
# cv.imshow("hello", img); cv.waitKey(0)
# Always safe (headless or not): save to file
cv.imwrite("hello.png", img)
"""


def showLiveFrame(device):
    """
    Captures and a frame using a passed VideoCapture device and displays in a window.
    """
    window = cv.namedWindow("live-feed")
    try:
        while True:
            ret, img = device.read()
            if not ret:
                print("Unable to capture image")
                continue
            img = cv.resize(img,(1280,720))
            (x1,y1),(x2,y2) = draw_centered_rectangle(img,color=(255,255,255),size=(300,200),thickness=2)
            cv.imshow("live-feed", img)
            cv.waitKey(1) #delay=1, smallest delays
    except KeyboardInterrupt:
        cv.destroyAllWindows()
    finally:
        print(f"Drew rectangle at ({x1},{y1}),({x2},{y2})")
        return (x1,y1),(x2,y2)

def capture_and_save_image(device, rpos, n=1, resolution=(1280,720)):
    """
    Captures n images using passed VideoCapture device and saves them.
    :returns: a list of the saved image Objects
    """
    images = []
    counter = 0
    try:
        for _ in range(n):
            ret, img = device.read()
            if not ret:
                print("Unable to capture image")
                continue
            x1,y1,x2,y2 = rpos[0][0],rpos[0][1],rpos[1][0],rpos[1][1]
            print(f"Cropping image to ({x1},{y1}),({x2},{y2})")
            img = cv.resize(img, resolution)
            img = img[y1:y2, x1:x2] #crop image      
            images.append(img)
            cv.imwrite(f"{counter}.png", img)
            counter += 1

    except Exception as e:
        print(e)
    finally:
        device.release()
        return images
    

def draw_centered_rectangle(image,color,size,thickness):
    blx = image.shape[1]
    bly = image.shape[0]
    w = size[0]
    h = size[1]
    rect_x1 = blx // 2 - 1 - (w // 2)
    rect_y1 = bly // 2 - 1 - (h // 2)
    rect_x2 = rect_x1 + w
    rect_y2 = rect_y1 + h
    cv.rectangle(img=image,pt1=(rect_x1,rect_y1),pt2=(rect_x2,rect_y2),color=color,thickness=thickness)
    return (rect_x1,rect_y1),(rect_x2,rect_y2)


def focus_target_area(image,rect_pos):
    pass


def get_px_rows(image,n):
    rows = []
    start = len(image) // 2 - (n // 2)
    end = len(image) // 2 + (n // 2)
    for i in range(start,end+1):
        rows.append(img[i])
    return rows


def rotate_image(image, angle):
    import numpy as np
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result

###

def capture_image():
    print("Making video device object...",end="")
    dev = cv.VideoCapture(0)
    print("DONE")

    print("Showing live feed...",end="")
    (x1,y1),(x2,y2) = showLiveFrame(device=dev)
    print("DONE")

    print("Capturing images...",end="")
    capture_and_save_image(dev,rpos=((x1,y1),(x2,y2)),n=1)
    print("DONE")




"""
img = cv.imread("0.png", cv.IMREAD_GRAYSCALE)


#img = rotate_image(img, -90)
img = cv.medianBlur(img, 5)

(thresh, blackAndWhite) = cv.threshold(img, 127, 255, cv.THRESH_BINARY) 
cv.imshow("ex", img)
cv.imshow("ex2", blackAndWhite)
"""



### sobel, otsu, blur
def sobel_demo():
    cv.namedWindow("ex")
    img = cv.imread("0.png", cv.IMREAD_GRAYSCALE)
    img = cv.medianBlur(img, 5)
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=5)
    #sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=5)
    cv.imshow("ex", sobelx)
    cv.waitKey(0)

def process_image(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return thresh


img = capture_image()
img = cv.imread('0.png')
#sobel_demo()
thresh = process_image(img)
cv.imshow("thresh", thresh )

cv.waitKey(0)




"""
rows = get_px_rows(img,3)
for row in rows:
    print(row[40:60],"...",row[-60:-40])
cv.waitKey(0)        
"""
