from minio import Minio
from minio.error import ResponseError
from vitess_connection import VitessConn
from minio_connection import MinioConn
import pandas as pd

def exp():

    vitess = VitessConn()
    '''
    minioClient = Minio('127.0.0.1:9001',
                  access_key='minio',
                  secret_key='minio123',
                  secure=False)
    '''
    # clearing the minio database
    minio = MinioConn()
    data_dict = {}
    data_dict["File_Names"] = '09f60573-af0c-11e9-b581-1866da0ca6dd.jpg'
    data_dict["Bucket_Name"] = 'car'
    data_dict["Bucket_Link"] = '127.0.0.1:9001/none/09f60573-af0c-11e9-b581-1866da0ca6dd'
    df = pd.DataFrame(data_dict)
    minio.batch_download(minio.mc, df)


exp()
