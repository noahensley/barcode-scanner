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
            (x1,y1),(x2,y2) = draw_centered_rectangle(img,color=(255,255,255),size=(300,150),thickness=2)
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


print("Making video device object...",end="")
dev = cv.VideoCapture(0)
print("DONE")

print("Showing live feed...",end="")
(x1,y1),(x2,y2) = showLiveFrame(device=dev)
print("DONE")

print("Capturing images...",end="")
capture_and_save_image(dev,rpos=((x1,y1),(x2,y2)),n=1)
print("DONE")


