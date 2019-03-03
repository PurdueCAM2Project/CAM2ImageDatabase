#!/usr/bin/env bash
docker-compose up -d
./lvtctl.sh ApplySchema -sql "$(cat create_test_table.sql)" test_keyspace
./lvtctl.sh ApplySchema -sql "$(cat create_test_table.sql)" test_keyspace
python connect_vitess.py
mysql --port=15306 --host=127.0.0.1
