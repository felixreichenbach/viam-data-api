#! /bin/bash

gcloud functions deploy python-http-function \
    --gen2 \
    --runtime=python311 \
    --region=us-west1 \
    --source=. \
    --entry-point=hello_http \
    --trigger-http \
    --allow-unauthenticated


gcloud functions describe python-http-function \
    --region us-west1