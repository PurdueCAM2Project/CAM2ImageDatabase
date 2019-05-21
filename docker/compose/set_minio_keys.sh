#Author: Haoran Wang
#Purpose: set AccessKey and SecretKey of Minio as environment variables

#!/bin/zsh

echo "Please set Access Key for Minio server"
read access
export MINIO_ACCESS_KEY=$access
echo "Access Key has been set to $MINIO_ACCESS_KEY"

echo ""

echo "Please set Secret Key for Minio server"
read secret
export MINIO_SECRET_KEY=$secret
echo "Secret Key has been set to $MINIO_SECRET_KEY"
