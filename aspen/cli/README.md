# IAM
## Get all projects
### Google Cloud Storage
```bash
export GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen-iam \
    -s cloudresourcemanager \
    -a fetch \
    -wf google_cloud_storage jsonl $GCP_BUCKET/data/iam/raw/projects/2021/09/13/data.jsonl \
    -c $GOOGLE_APPLICATION_CREDENTIALS
```

# Local
```bash
export GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen-iam 
    -s cloudresourcemanager 
    -a fetch 
    -c $GOOGLE_APPLICATION_CREDENTIALS
    -wf open jsonl $GCP_BUCKET/data/iam/raw/projects/2021/09/13/data.jsonl
```

# Get Recommendations for one project
## Google Cloud Storage
```bash
export GCP_PROJECT_NAME=[gcp-project-name]
export GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
aspen-iam \
    -s recommender \
    -a fetch \
    -c $GOOGLE_APPLICATION_CREDENTIALS
    -wf google_cloud_storage jsonl "random-bucket-12309/data/iam/raw/recommendations/$GCP_PROJECT_NAME/2021/09/27/data.jsonl" \
    -pid $GCP_PROJECT_NAME
```

# Parse Recommendations for one project
## Google Cloud Storage
```bash
export GCP_PROJECT_NAME=[gcp-project-name]
export GOOGLE_APPLICATION_CREDENTIALS=[path-to-credentials]
export GCP_BUCKET=[name-of-bucket]
aspen-iam \
    -s recommender \
    -a parse \
    -c $GOOGLE_APPLICATION_CREDENTIALS \
    -rf google_cloud_storage jsonl "$GCP_BUCKET/data/iam/raw/recommendations/$GCP_PROJECT_NAME/2021/09/27/data.jsonl" \
    -wf google_cloud_storage jsonl "$GCP_BUCKET/data/iam/parsed/recommendations/$GCP_PROJECT_NAME/2021/09/27/data.jsonl" \
    -pid "$GCP_PROJECT_NAME"
```

# Local
```bash
export GCP_PROJECT_NAME=[gcp-project-name]
aspen-iam \
    -s recommender \
    -a fetch \
    -c [path-to-credentials] \
    -wf 'google_cloud_storage jsonl data/iam/raw/recommendations/{GCP_PROJECT_NAME}/2021/09/13/data.jsonl' \
    -pid $GCP_PROJECT_NAME
```

