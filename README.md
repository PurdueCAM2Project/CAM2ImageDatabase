# CAM2ImageDatabase - Compare Function
This function is used before uploading files to the Image Database. Once the CSV file containing all the image file information is created, this compare function will check the directory containing the image files and the CSV file for discrepencies in the file names.

It checks to make sure all the files, in the directory that is going to be uploaded, exist in the CSV and all the files in the CSV exist in the directoty.

The purpose of this is to prevent the uploading of image features without a corresponding image, and vice-versa.

##
The compare.py function will be incorporated into the ImageDB.py script. This is so that the CSV file isn't opened and iterated through multiple times, increasing efficiency.

The compare function will go in the read_data method (in ImageDB.py)
