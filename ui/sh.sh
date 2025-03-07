export FE_SERVICE_NAME="go-soft-hack-ui-9"
export FE_IMAGE="us-central1-docker.pkg.dev/vertexai1-368814/go-soft-hack-be/go-soft-hack-backend:v0.0.9"
export FE_REGION="us-central1"
export FE_SA="go-soft-hack-1@vertexai1-368814.iam.gserviceaccount.com"
export MIN="1"
export max="1"

docker build -t $FE_IMAGE .
docker tag $FE_IMAGE $FE_IMAGE
docker push $FE_IMAGE

gcloud run deploy $FE_SERVICE_NAME \
    --image=$FE_IMAGE \
    --region=$FE_REGION \
    --allow-unauthenticated \
    --min-instances=$MIN \
    --max-instances=$MAX \
    --service-account=$FE_SA

# gcloud auth configure-docker

