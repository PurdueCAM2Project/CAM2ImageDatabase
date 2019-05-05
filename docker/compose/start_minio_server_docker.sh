#Author: Haoran Wang
#Purpose: Start / Stop Minio server in a Docker container

#!/bin/zsh

# Parameters
# folder path that contains the images
folder="$(pwd)/minio_test_server"
# minio path, if installed correctly, should be $HOME/.minio
minio="$HOME/.minio"

echo "Has a Minio server been set up in this container? Y or N"
read response

if [ $response == 'N' ];
then
	echo "A new Minio server is being set up in this container..."
	docker run -p 9000:9000 --name CAM2Minio \
  		-e "MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY" \
  		-e "MINIO_SECRET_KEY=$MINIO_SECRET_KEY" \
  		-v $folder:$folder \
  		-v $minio:$minio \
  		minio/minio server $folder 
else
	container_id=$(docker container ls -a | grep CAM2Minio | cut -d' ' -f 1)
	echo "Starting Minio server with container id $container_id"
	docker start $container_id
	echo "Your Minio server is up, its container id is $container_id"
fi

container_id=$(docker container ls -a | grep CAM2Minio | cut -d' ' -f 1)
echo "Enter STOP if you want to stop Minio server $container_id"
read stop

if [ $stop == 'STOP' ];
then
	echo "Shutting down server $container_id"
	docker stop $container_id
	echo "Minio server $container_id has been shut down"
fi

