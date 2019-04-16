README


Follow the steps below:

1. Go to the directory ./docker/compose

2. If need to stop the cluster. NOTE: you will lose all the data
	$docker-compose kill  

3. If need to stop the cluster. NOTE: you will lose all the data
	$docker-compose rm -v

4. Start the cluster
	$docker-compose up -d

5. Load the schema. Sometimes it needs to run twice, needed to fix. If it still not working, run step 4 again
	$./lvtctl.sh ApplySchema -sql "$(cat create_test_table.sql)" test_keyspace

6. Set Access Key and Secret Key for Minio Server
	$./set_minio_keys.sh

7. Start Minio Server
	$./start_minio_server_docker.sh

8. Update and complete starting the cluster
	$docker-compose up -d

9. Go to the directory ../../ImageDB

10. To see the sample test code. You can create your own
	$python test.py

11. Connect to vtgate and run queries.
	$mysql --port=15306 --host=127.0.0.1

12. More test csv and test cases details are located in the vitess_test folder




Exploring

vtctld web ui: http://localhost:15000

vttablets web ui: http://localhost:15001/debug/status http://localhost:15002/debug/status http://localhost:15003/debug/status

vtgate web ui: http://localhost:15099/debug/status


Reference: https://github.com/vitessio/vitess/tree/master/examples/compose
