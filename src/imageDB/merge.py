import os
import cv2
import datetime

img_array = []
size = 0
images = os.listdir('output_images/')
images.sort()
for i in images:
	#print(os.path.join('Cat2/', filename))
	img = cv2.imread(os.path.join('output_images/', i))
	#cv2.imshow('image', img)
	#cv2.waitKey(500)

	height, width, layers = img.shape
	size = (width, height)
	img_array.append(img)

ts = datetime.datetime.now()
file_name = ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%H:%M:%S")
out = cv2.VideoWriter(filename=file_name + '.avi',
					  fourcc=cv2.VideoWriter_fourcc(*'MJPG'),
					  fps=2,
					  frameSize=size)

for i in range(len(img_array)):
	out.write(img_array[i])

out.release()