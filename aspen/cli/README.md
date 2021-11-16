# IAM
## Get all projects
### Google Cloud Storage
```bash
export GLOBAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export LOCAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen \
    -s cloudresourcemanager \
    -m fetch \
    -ws google_cloud_storage jsonl $GCP_BUCKET/iam/raw/projects/2021/11/02/data.jsonl $LOCAL_GOOGLE_APPLICATION_CREDENTIALS \
    -gc $GLOBAL_GOOGLE_APPLICATION_CREDENTIALS
```

# Local
```bash
export GLOBAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen 
    -s cloudresourcemanager 
    -m fetch 
    -gc $GLOBAL_GOOGLE_APPLICATION_CREDENTIALS
    -ws open jsonl $GCP_BUCKET/iam/raw/projects/2021/11/01/data.jsonl
```

# Get Recommendations for one project
## Google Cloud Storage
```bash
export GCP_PROJECT_NAME=[gcp-project-name]
export GLOBAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
aspen \
    -s recommender \
    -m fetch \
    -p "{\"project_id\": \"${GCP_PROJECT_NAME}\"}" \
    -gc $GLOBAL_GOOGLE_APPLICATION_CREDENTIALS \
    -ws google_cloud_storage jsonl "$GCP_BUCKET/iam/raw/recommendations/$GCP_PROJECT_NAME/2021/11/01/data.jsonl" $LOCAL_GOOGLE_APPLICATION_CREDENTIALS
```

# Parse Recommendations for one project
## Google Cloud Storage
```bash
export GCP_PROJECT_NAME=[gcp-project-name]
export GLOBAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen \
    -s recommender \
    -m parse \
    -gc $GLOBAL_GOOGLE_APPLICATION_CREDENTIALS \
    -rs google_cloud_storage jsonl "$GCP_BUCKET/iam/raw/recommendations/$GCP_PROJECT_NAME/2021/11/01/data.jsonl" $LOCAL_GOOGLE_APPLICATION_CREDENTIALS \
    -ws google_cloud_storage jsonl "$GCP_BUCKET/iam/parsed/recommendations/$GCP_PROJECT_NAME/2021/11/01/data.jsonl" $LOCAL_GOOGLE_APPLICATION_CREDENTIALS
```

# Query BigQuery and Save to Cloud Storage
## Google Cloud Storage
```bash
export GLOBAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen \
    -s storageclient \
    -m read_to_write \
    -gc  $LOCAL_GOOGLE_APPLICATION_CREDENTIALS \
    -rs google_bigquery str 'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` LIMIT 20' \
    -ws google_cloud_storage jsonl random-bucket-12309/2021/11/01/saved_data.jsonl $LOCAL_GOOGLE_APPLICATION_CREDENTIALS
```

