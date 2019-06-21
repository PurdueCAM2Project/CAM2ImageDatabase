# README


## Instructions

1. Clean up. NOTE: you will lose all the data

	`$ docker-compose kill`
	
	`$ docker-compose rm -f`
	
	`$ docker system prune --all`

2. Start the cluster.

	`$ docker-compose up -d`

3. Load the schema. Sometimes it needs to run twice, needed to fix. If it still not working, run step 4 again

	`$ ./src/docker/lvtctl.sh ApplySchema -sql "$(cat src/docker/create_test_table.sql)" test_keyspace`

4. Update and complete starting the cluster

	`$ docker-compose up -d`

5. Connect the Vitess client

	`$ ./src/docker/client.sh`

6. Connect to vtgate and run queries.

	`$ mysql --port=15306 --host=127.0.0.1`
	
7. Vitess Web UI

	vtctld: 
	
	`http://localhost:15000`
	
	vttablets: 
	
	`http://localhost:15001/debug/status`
	
	`http://localhost:15002/debug/status`
	
	`http://localhost:15003/debug/status`
	
	vtgate: 
	
	`http://localhost:15099/debug/status`
	
8. Minio Web UI

	`http://localhost:9001`


## CAM2ImageDatabase - Compare Function
This function is used before uploading files to the Image Database. Once the CSV file containing all the image file information is created, this compare function will check the directory containing the image files and the CSV file for discrepencies in the file names.

It checks to make sure all the files, in the directory that is going to be uploaded, exist in the CSV and all the files in the CSV exist in the directoty.

The purpose of this is to prevent the uploading of image features without a corresponding image, and vice-versa.

##
The compare.py function will be incorporated into the ImageDB.py script. This is so that the CSV file isn't opened and iterated through multiple times, increasing efficiency.

The compare function will go in the read_data method (in ImageDB.py)

## CAM2ImageDatabase - Extract image and camera metdata

To run the program:
The 2 python scripts (image_metadata_script.py and camera_metadata_script.py) are standalone applications which can be run by simply copying them into an IDE

To run the image_metadata_script.py:
To the image_metadata function, pass the path to the 'results' folder. 
The 'results' folder contains sub directories each named after the camera ID of the individual cameras. Each of these sub directories contains the images from that particular camera.
This will create the image metadata csv file.

To run the camera_metadata_script.py:
The camera_metadata function accepts teh image metadata csv file generated in the previous step. Therefore, run the image_metadata_script.py before running this file.
This will create the camera metadata csv file.


## Reference

` https://github.com/vitessio/vitess/tree/master/examples/compose `


