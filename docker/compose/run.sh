#!/bin/bash

echo "running step 0 - clean up"
docker-compose kill
docker-compose rm -f
docker system prune --all

echo "running step 1 - first up"
docker-compose up -d

echo "running step 2 applying schema"
./lvtctl.sh ApplySchema -sql "$(cat create_test_table.sql)" test_keyspace

echo "running step 2 applying schema(again for reliability)"
./lvtctl.sh ApplySchema -sql "$(cat create_test_table.sql)" test_keyspace

echo "running step 3 final up"
docker-compose up -d

echo "running step 4 for vittese"
./client.sh

#echo "running step 5 opening browser"
#start chrome http://localhost:15000
#start chrome http://localhost:9001
