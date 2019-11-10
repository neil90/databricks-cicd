import os
import glob
import json
from _databricksrestclient import DatabricksRestClient

shard = os.environ["PROD_DATABRICKS_SHARD"]
token = os.environ["PROD_DATABRICKS_TOKEN"]

# Get jobs from prod
api_client = DatabricksRestClient(token=token, url=shard)

jobs_all = api_client.get("/jobs/list")  # ["jobs"]

if len(jobs_all) == 0:
    jobs = None
else:
    jobs = jobs_all["jobs"]

# Load Job Jsons
job_jsons = [f for f in glob.glob("../job-json/*", recursive=True)]

for job_json in job_jsons:
    with open(job_json) as json_file:
        job_data = json.load(json_file)

    print("Working Job Json " + job_json)

    if jobs:
        jobs_exists = False
        for job in jobs:
            if job["settings"]["name"] == job_data["name"]:
                jobs_exists = {"job_id": job["job_id"]}
                jobs_exists["new_settings"] = job_data

                print("Updating Job " + job["settings"]["name"])
                api_client.post("/jobs/reset", json_params=jobs_exists)

        if jobs_exists is False:
            print("Creating Job " + job_data["name"])
            api_client.post("/jobs/create", json_params=job_data)
    # Odd case if no jobs are created yet
    else:
        print("Creating Job " + job_data["name"])
        api_client.post("/jobs/create", json_params=job_data)

# Note to delete currently need to delete through
# UI/API then remove json job_json folder
