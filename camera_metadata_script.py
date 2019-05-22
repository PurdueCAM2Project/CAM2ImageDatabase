import CAM2CameraDatabaseAPIClient.client as cam2
import csv

clientID = '%s' %(cam2.Client.clientID) # placeholder
clientSecret = '%s' %(cam2.Client.clientSecret) # placeholder

db = cam2.Client(clientID, clientSecret)

cameras1 = []


def camera_metadata(file):
    try:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    cameras1.append(db.camera_by_id(row[1]))
                line_count += 1
    except Exception as e:
        if file:
            file.close()
        print(e)

    try:
        output_file = open('file2_name.csv', 'w')

        fields = ['Camera_ID', 'camera_country', 'camera_state', 'camera_city', 'camera_latitude', 'camera_longitude', 'resolution_width', 'resolution_height']
        writer = csv.writer(output_file)
        writer.writerow(fields)

        for camera in cameras1:
            camera_ID = camera['cameraID']
            camera_city = camera['city']
            camera_country = camera['country']
            camera_state = camera['state']
            camera_longitude = camera['longitude']
            camera_latitude = camera['latitude']
            camera_rwidth = camera['resolution_width']
            camera_rheight = camera['resolution_height']
            writer.writerow([camera_ID, camera_country, camera_state, camera_city, camera_latitude, camera_longitude, camera_rwidth, camera_rheight])

    except Exception as e:
        if output_file:
            output_file.close()
        print(e)

    output_file.close()


camera_metadata('file_name.csv')
