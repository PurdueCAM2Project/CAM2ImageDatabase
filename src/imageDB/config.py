CAM_HEADER=["Camera_ID", "Country", "State", \
                "City", "Latitude", "Longtitude", \
                "Resolution_w", "Resolution_h", \
				"Ip", "Port", "Image_path", "Video_path"]

IV_HEADER=['IV_Name', 'Camera_ID', 'IV_date', 'IV_time', 'File_type', \
                'File_size', 'Minio_link', 'Dataset', 'Is_processed']

BOX_NAME_HEADER=['IV_Name', 'Feature_Name','Xmin','Xmax','Ymin','Ymax']

BOX_HEADER=['IV_ID', 'Feature_ID','Xmin','Xmax','Ymin','Ymax']

IF_HEADER=['IV_Name']

KEYSPACE='test_keyspace'

VITESS_HOST='127.0.0.1'

VITESS_PORT='15306'

VITESS_PASS='mysql_native_password'

MINIO_ENDPOINT='127.0.0.1:9001'#'play.min.io:9000'

MINIO_ACCESS_KEY='minio'#'Q3AM3UQ867SPQQA43P2F'
MINIO_SECRET_KEY='minio123'#'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
