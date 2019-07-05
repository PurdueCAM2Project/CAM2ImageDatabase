from minio import Minio
from minio.error import ResponseError

def clear():
    minioClient = Minio('127.0.0.1:9001',
                  access_key='minio',
                  secret_key='minio123',
                  secure=False)

    # clearing the minio database
    clear = True

    buckets = minioClient.list_buckets()
    for bucket in buckets:
        print(bucket.name)

        objects = minioClient.list_objects_v2(bucket.name, prefix=None, recursive=True)
        i = 0
        for obj in objects:
            if clear == True:
                minioClient.remove_object(bucket.name, obj.object_name)
            i = i + 1
        print(i)

        if clear == True:
            try:
                minioClient.remove_bucket(bucket.name)
            except ResponseError as err:
                print(err)

        print("++++++++++++++++++++++++++++")

clear()