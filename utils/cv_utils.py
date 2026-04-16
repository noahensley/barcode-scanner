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
RESOLUTION = (1280,720)
CROP_RECTANGLE = (RESOLUTION[0]//2,RESOLUTION[1]//2)


def showLiveFrame(device,resolution=RESOLUTION):
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
            img = cv.resize(img,resolution)
            (x1,y1),(x2,y2) = draw_centered_rectangle(img,color=(255,255,255),size=CROP_RECTANGLE,thickness=2)
            cv.imshow("live-feed", img)
            cv.waitKey(1) #delay=1, smallest delays
    except KeyboardInterrupt:
        cv.destroyAllWindows()
    finally:
        print(f"Drew rectangle at ({x1},{y1}),({x2},{y2})")
        return (x1,y1),(x2,y2)

def capture_images(device:cv.VideoCapture, rpos, n=1, resolution=RESOLUTION):
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
            #print(f"Cropping image to ({x1},{y1}),({x2},{y2})")
            img = cv.resize(img, resolution)
            img = img[y1:y2, x1:x2] #crop image
            #img = process_image(img)
            images.append(img)
            cv.imwrite(f"{counter}.png", img)
            counter += 1

    except Exception as e:
        print(e)
    finally:
        device.release()
        return images
    

def process_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return thresh
    

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
        rows.append(image[i])
    return rows


def is_horizontal(rows, color, minimum=50):
    consecutive = 0
    for row in rows:
        for x in range(len(row)):
            if row[x] == color:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == minimum:
                return True
    return False


def orient(image):
    rows = get_px_rows(image=image,n=3)
    while not is_horizontal(rows=rows,color=0):
        rotate_image(image=image,angle=1)
    rotate_image(image=image,angle=90)
    return image


def rotate_image(image, angle):
    import numpy as np
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result


print("Making video device object...",end="")
dev = cv.VideoCapture(0)
print("DONE")

print("Showing live feed...",end="")
(x1,y1),(x2,y2) = showLiveFrame(device=dev,resolution=RESOLUTION)
print("DONE")

print("Capturing images...",end="")
images = capture_images(dev,rpos=((x1,y1),(x2,y2)),n=3,resolution=RESOLUTION)
print("DONE")

cv.waitKey(0)        

