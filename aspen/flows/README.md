
# IAM 
## Get all project recommendations
```
bash
export GOOGLE_APPLICATION_CREDENTIALS
python3 -m flows.iam \
    -f all-project-recommendations \
    -c [path-to-credentials] \
    -pwrf google_cloud_storage jsonl iam-raw/projects/20210913/data.jsonl \
    -rrf google_cloud_storage jsonl iam-raw/recommendations/20210913/{{project_id}}.jsonl \
    -rwpf google_cloud_storage jsonl iam-parsed/recommendations/20210913/{{project_id}}.jsonl
```