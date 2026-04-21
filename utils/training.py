import numpy as np
import cv2 as cv
import pickle

cv.samples.addSamplesDataSearchPath(r"C:\Users\noahe\AppData\Local\Programs\Python\Python313\Lib\opencv\sources\samples\data")
img = cv.imread(cv.samples.findFile('digits.png'))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Split into individual digit cells (20x20 pixels)
cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]
x = np.array(cells)



# Now load the data
with np.load('knn_data.npz') as data:
    print( data.files )
    train = data['train']
    train_labels = data['train_labels']

# Labels: 250 of each digit 0–9
test_labels = np.repeat(np.arange(10), 250)[:, np.newaxis]
test = x[:, 50:100].reshape(-1, 400).astype(np.float32)

knn = cv.ml.KNearest_create()
knn.train(train, cv.ml.ROW_SAMPLE, train_labels)

ret, result, neighbours, dist = knn.findNearest(test, k=5)

accuracy = (result == test_labels).mean() * 100
print(f"Test accuracy: {accuracy:.2f}%")

# Save the data
np.savez('knn_data.npz',train=train, train_labels=train_labels)