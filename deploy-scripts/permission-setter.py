import sys
import glob
import json
import yaml
import requests

shard = os.environ["PROD_DATABRICKS_SHARD"]
token = os.environ["PROD_DATABRICKS_TOKEN"]
PROD_DIR_ID = 2456

# Parse Yaml to get groups
with open("./permissions.yaml") as file:
    permissions = yaml.load(file, Loader=yaml.FullLoader)
    
read_prod_dir_grp = permissions['read-prod-dir']
view_prod_jobs_grp = permissions['view-prod-jobs']

############################################################################
# Notebook ACL Update
############################################################################

# Create Notebooks ACL as Json
dir_acl_list = []
for group in read_prod_dir_grp:
  dir_acl_list.append({'group_name': group, 'permission_level': 'CAN_READ'})
  
full_dir_acl_json = {
  "access_control_list":dir_acl_list
}

# Updating the Production folder
print("Giving Read On Prod Folder to the following Groups...")
print(read_prod_dir_grp)
requests.put(f"{shard}/api/2.0/preview/permissions/directories/{PROD_DIR_ID}", auth=('token', token), data=json.dumps(full_dir_acl_json))
print("Updated Permissions on Prod Folder")

############################################################################
############################################################################
############################################################################


############################################################################
# Jobs ACL Update
############################################################################

# Generating ACL Json
jobs_acl_list = []
for group in view_prod_jobs_grp:
  jobs_acl_list.append({'group_name': group, 'permission_level': 'CAN_VIEW'})
  
full_jobs_acl_json = {
  "access_control_list":jobs_acl_list
}

# Load Job Jsons and Get Job Names
job_jsons = [f for f in glob.glob("../job-json/*", recursive=True)]

job_name = []
for job_json in job_jsons:
    with open(job_json) as json_file:
        job_name.append(json.load(json_file)["name"])

print("Getting List of Jobs on Shard...")
jobs_list = requests.get(f"{shard}/api/2.0/jobs/list", auth = ('token', token)).json()
if not jobs_list:
  print("No jobs available, exiting...")
  sys.exit()

print("Giving View On Jobs to the following Groups...")
print(view_prod_jobs_grp)  
for job in jobs_list['jobs']:
  if job["settings"]["name"] in job_name:
    job_id = job["job_id"]
    requests.put(f"{shard}/api/2.0/preview/permissions/jobs/{job_id}", auth=('token', token), data=json.dumps(full_jobs_acl_json))
    print("Updated Permissions on Job " + job["settings"]["name"] +", Job ID: " + job_id)

############################################################################
############################################################################
############################################################################
