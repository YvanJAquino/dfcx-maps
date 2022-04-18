#! /bin/bash

docker build -t gcr.io/basic-strata-326019/dfcx-va . 
docker push gcr.io/basic-strata-326019/dfcx-va
gcloud run deploy dfcx-va \
    --project basic-strata-326019 \
    --image gcr.io/basic-strata-326019/dfcx-va \
    --timeout 15m \
    --region us-east4 \
    --platform managed \
    --min-instances 0 \
    --max-instances 5 \
    --allow-unauthenticated

# docker run --rm -e PORT=6969 gcr.io/basic-strata-326019/dfcx-va
# docker run -it --rm -e PORT=6969 gcr.io/basic-strata-326019/dfcx-va /bin/bash