# CAM2ImageDatabase - Compare Function

This function is used before uploading files to the database. Once the CSV file containing all the image file information is created, this compare function will check the directory containing the image files and the CSV file for discrepencies.

It checks to make sure all files, that are in the directory that is going to be uploaded, exist in the CSV and all files in the CSV exist in the directory.

The purpose of this is to prevent the uploading of image features without an image that corresponds to it, and vice-versa.
