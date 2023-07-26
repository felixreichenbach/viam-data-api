#! /bin/bash
curl -X POST localhost:8080 -H "Content-Type: application/json" -d '{"date_start": "2023-07-13 00:00:00", "date_end": "2023-07-14 00:00:00"}'
