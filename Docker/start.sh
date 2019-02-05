#!/usr/bin/env bash
docker-compose up -d
#run the next line incase of fresh install only.
#./lvtctl.sh ApplySchema -sql "$(cat create_test_table.sql)" test_keyspace
#docker-compose kill
#docker-compose up -d
./client.sh