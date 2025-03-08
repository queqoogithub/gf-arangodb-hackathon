export BE_VERSION="v0.1.0"
export BE_SERVICE_NAME="go-soft-hack-api-10"
export BE_IMAGE="us-central1-docker.pkg.dev/vertexai1-368814/go-soft-hack-be/go-soft-hack-backend:$BE_VERSION"
export BE_REGION="us-central1"
export BE_SA="go-soft-hack-1@vertexai1-368814.iam.gserviceaccount.com"
export MIN="1"
export MAX="1"

docker build -t $BE_IMAGE .
docker tag $BE_IMAGE $BE_IMAGE
docker push $BE_IMAGE

gcloud run deploy $BE_SERVICE_NAME \
    --image=$BE_IMAGE \
    --region=$BE_REGION \
    --allow-unauthenticated \
    --min-instances=$MIN \
    --max-instances=$MAX \
    --service-account=$BE_SA \
    --set-secrets=ARANGO_HOST=projects/343673271091/secrets/ARANGO_HOST:latest \
    --set-secrets=ARANGO_PASSWORD=projects/343673271091/secrets/ARANGO_PASSWORD:latest \
    --set-secrets=GOOGLE_API_KEY=projects/343673271091/secrets/GOOGLE_API_KEY:latest \
    --set-secrets=GPT_MODEL=projects/343673271091/secrets/GPT_MODEL:latest \
    --set-secrets=OPENAI_API_KEY=projects/343673271091/secrets/OPENAI_API_KEY:latest

# gcloud auth configure-docker


	