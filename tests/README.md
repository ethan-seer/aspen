# How to Test
You must specify the following environment variables:

```
bash
export GCP_PROJECT_NAME=[gcp-project-name]
export GLOBAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-google-service-account]
export LOCAL_GOOGLE_APPLICATION_CREDENTIALS=[path-to-google-service-account]
export GCP_BUCKET=[name-of-bucket]
export RECOMMENDER_PROJECT_ID=[project-id-for-recommender]
```

Simply run the following command in the root folder for specific modules:

```
bash
pytest -s --log-cli-level=INFO --disable-pytest-warnings -m XXXXX
```

Or you can run all tests with: 

```
bash
pytest
```