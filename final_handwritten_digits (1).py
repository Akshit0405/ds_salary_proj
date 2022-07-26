# -*- coding: utf-8 -*-
"""Final handwritten digits.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x9PVTxPtAxNnFfe6I9IpjK9irz5FWoI7

**steps that are needed to detect handwritten digits -**

1. Create a database of handwritten digits.
2. For each handwritten digit in the database, extract HOG features and train a Linear SVM.
3. Use the classifier trained in step 2 to predict digits.
"""



"""MNIST database of handwritten digits
The first step is to create a database of handwritten digits. We are not going to create a new database but we will use the popular MNIST database of handwritten digits. The MNIST database is a set of 70000 samples of handwritten digits where each sample consists of a grayscale image of size 28×28. There are a total of 70,000 samples. We will use sklearn.datasets package to download the MNIST database from mldata.org. This package makes it convenient to work with toy datasbases, you can check out the documentation of sklearn.datasets here.

The size of of MNIST database is about 55.4 MB. Once the database is downloaded, it will be cached locally in your hard drive. On my Linux system, by default it is cached in ~/scikit_learn_data/mldata/mnist-original.mat . Alternatively, you can also set the directory where the database will be downloaded.

There are approximate 7000 samples for each digit. I actually calculated the number of samples for each digit using collections.Counter class

Digits	Number of samples

* 0  6903
* 1  7877
* 2  6990
* 3  7141
* 4	6824
* 5	6313
* 6	6876
* 7	7293
* 8	6825
* 9	6958

---

We will write 2 python scripts – one for training the classifier and the second for test the classifier.

Training a Classifier
Here, we will implement the following steps –

Calculate the HOG features for each sample in the database.
Train a multi-class linear SVM with the HOG features of each sample along with the corresponding label.
Save the classifier in a file
The first step is to import the required modules –
"""

from google.colab import drive
drive.mount('/content/drive')

!ls "/content/drive/My Drive/Colab Notebooks"

# Import the modules
from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import sklearn
import numpy as np
from scipy.io import loadmat
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib.pyplot as plt
import sys

if int((sklearn.__version__).split(".")[1]) < 18:
	from sklearn.cross_validation import train_test_split
 
# otherwise we're using at lease version 0.18
else:
	from sklearn.model_selection import train_test_split

"""We will use the sklearn.externals.joblib package to save the classifier in a file so that we can use the classifier again without performing training each time. Calculating HOG features for 70000 images is a costly operation, so we will save the classifier in a file and load it whenever we want to use it. As discussed above sklearn.datasets package will be used to download the MNIST database for handwritten digits. We will use skimage.feature.hog class to calculate the HOG features and sklearn.svm.LinearSVC class to perform prediction after training the classifier. We will store our HOG features and labels in numpy arrays. The next step is to download the dataset using the sklearn.datasets.fetch_mldata function. For the first time, it will take some time as 55.4 MB will be downloaded.

Link : HOG Feature extraction - https://www.learnopencv.com/histogram-of-oriented-gradients/



if "datasets.fetch_mldata("MNIST original")"  this doesnt work
download dataset 
https://github.com/amplab/datascience-sp14/blob/master/lab7/mldata/mnist-original.mat

and use this
mnist = fetch_mldata('MNIST original', transpose_data=True, data_home='files')
"""

!wget  https://github.com/amplab/datascience-sp14/blob/master/lab7/mldata/mnist-original.mat

!ls

# Alternative method to load MNIST, if mldata.org is down
from scipy.io import loadmat
import urllib  
mnist_alternative_url = "https://github.com/amplab/datascience-sp14/raw/master/lab7/mldata/mnist-original.mat"
mnist_path = "./mnist-original.mat"
response = urllib.request.urlopen(mnist_alternative_url)
with open(mnist_path, "wb") as f:
  content = response.read()
  f.write(content)
  mnist_raw = loadmat(mnist_path)
  mnist = {
      "data": mnist_raw["data"].T,
      "target": mnist_raw["label"][0],
      "COL_NAMES": ["label", "data"],
      "DESCR": "mldata.org dataset: mnist-original",
  }
print("Success!")

#mnist = datasets.fetch_mldata('MNIST original', transpose_data=True, data_home='files')
#mnist =  datasets.fetch_mldata('MNIST original')
#mnist = datasets.load_digits()
# take the MNIST data and construct the training and testing split, using 75% of the
# data for training and 25% for testing

(trainData, testData, trainLabels, testLabels) = train_test_split(np.array(mnist["data"]),
	mnist["target"], test_size=0.25, random_state=42)

# now, let's take 10% of the training data and use that for validation
(trainData, valData, trainLabels, valLabels) = train_test_split(trainData, trainLabels,
	test_size=0.1, random_state=84)

# show the sizes of each data split
print("training data points: {}".format(len(trainLabels)))
print("validation data points: {}".format(len(valLabels)))
print("testing data points: {}".format(len(testLabels)))
print(type(trainData[0]))

for i in (np.random.randint(0,270,6)):
  two_d = (np.reshape(testData[i], (28, 28)) * 255).astype(np.uint8)
  plt.title('label: {0}'. format(testLabels[i]))
  plt.imshow(two_d, interpolation='nearest', cmap='gray')
  plt.show()

#clf = LinearSVC()
clf_linear_without_hog = svm.LinearSVC()

clf_linear_without_hog.fit(trainData, trainLabels)

joblib.dump(clf_linear_without_hog, "clf_linear_without_hog.pkl", compress=3)

svm_score1 = clf_linear_without_hog.score(testData, testLabels)
svm_score1

features = np.array(trainData,'int16')
labels = np.array(trainLabels, 'int')
list_hog_fd = []
for feature in trainData:
    fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1), visualise=True)
    list_hog_fd.append(fd)
    print(fd[1].shape)
    plt.imshow(fd[1], cmap=plt.cm.gray)
#   plt.set_title(‘Histogram of Oriented Gradients’)
    plt.show()
    sys.exit()
hog_features = np.array(list_hog_fd, 'float64')



ax2.axis(‘off’)
ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
ax2.set_title(‘Histogram of Oriented Gradients’)
plt.show()

#clf = LinearSVC()
clf_linear = svm.LinearSVC()

clf_linear.fit(hog_features, labels)



clf = svm.SVC(gamma='scale', decision_function_shape='ovo')

clf.fit(hog_features, labels)

joblib.dump(clf, "digits_cls_scale.pkl", compress=3)

test_features = np.array(testData,'int16')
label = np.array(testLabels,'int')
test_hog_fd = []
for features in test_features:
    fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    test_hog_fd.append(fd)
    #print("test :",test_hog_features)
    print("hog",type(test_hog_features))   
    print("hog",test_hog_features.shape)   

    exit()
#test_hog_features = np.array(test_hog_fd, 'float64')

svm_score1 = clf_linear.score(test_hog_features, label)
svm_score1

#pred = clf.predict(test_hog_features)

#print(type(label))
svm_score = clf.score(test_hog_features, label)
svm_score

joblib.dump(clf, "/content/drive/My Drive/Colab Notebooks/digits_cls_svm.pkl", compress=3)

kVals = range(1, 30, 2)
accuracies = []
# loop over various values of `k` for the k-Nearest Neighbor classifier
for k in range(1, 30, 2):
	# train the k-Nearest Neighbor classifier with the current value of `k`
	model = KNeighborsClassifier(n_neighbors=k)
	model.fit(trainData, trainLabels)
 
	# evaluate the model and update the accuracies list
	score = model.score(valData, valLabels)
	print("k=%d, accuracy=%.2f%%" % (k, score * 100))
	accuracies.append(score)

model = KNeighborsClassifier(n_neighbors=kVals[i])



# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import matplotlib.pyplot as plt

# Load the classifier
clf = joblib.load("/content/drive/My Drive/Colab Notebooks/digits_cls.pkl")

# Read the input image 
im = cv2.imread('/content/drive/My Drive/Colab Notebooks/digit_test.jpg')
print("Image type",type(im))
# Convert to grayscale and apply Gaussian filtering
#im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

# Threshold the image
ret, im_th = cv2.threshold(im_gray, 70, 255, cv2.THRESH_BINARY_INV)
#print("Thresh ",im_th)

# Find contours in the image
orignalimg,ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

# For each rectangular region, calculate HOG features and predict
# the digit using Linear SVM.
for rect in rects:
    # Draw the rectangles
    cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
    # Make the rectangular region around the digit
    leng = int(rect[3] * 1.6)
    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
    #print("ROI ",roi)
    # Resize the image
    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    roi = cv2.dilate(roi, (3, 3))
    # Calculate the HOG features
    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

plt.imshow(im)

