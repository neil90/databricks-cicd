import os
import glob
import json
from _databricksrestclient import DatabricksRestClient

shard = os.environ['PROD_DATABRICKS_SHARD']
token = os.environ['PROD_DATABRICKS_TOKEN']

# Get jobs from prod
api_client = DatabricksRestClient(token=token, url=shard)

jobs = api_client.get("/jobs/list")["jobs"]

# Load Job Jsons
job_jsons = [f for f in glob.glob("../job-json/*", recursive=True)]

for job_json in job_jsons:
    with open(job_json) as json_file:
        job_data = json.load(json_file)

    job_exists = False
    for job in jobs:
        # print(job["settings"]["name"], job_data["name"])
        if job["settings"]["name"] == job_data["name"]:
            job_exists = {"job_id": job["job_id"]}

            if job_exists:
                job_exists["new_settings"] = job_data

                print("Updating Job " + job["settings"]["name"])
                api_client.post("/jobs/reset", json_params=job_exists)
    if job_exists == False :
        print("Creating Job " + job_data["name"])
        api_client.post("/jobs/create", json_params=job_data)
