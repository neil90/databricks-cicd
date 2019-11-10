# Databricks notebook source
import json, pprint, requests

# Helper to pretty print json
def pprint_j(i):
    print(json.dumps(i, indent=4, sort_keys=True))


# This can easily be extended to work with other databricks API
# https://docs.databricks.com/api/latest/index.html
class DatabricksRestClient:
    """A class to define wrappers for the REST API
    Extend if you need additional functionality
    """

    def __init__(self, token="ABCDEFG1234", url="https://myenv.cloud.databricks.com"):
        self.__token = {"Authorization": "Bearer {0}".format(token)}
        self.__url = url

    def get(self, endpoint, json_params={}, printJson=False):
        if json_params:
            results = requests.get(
                self.__url + "/api/2.0" + endpoint,
                headers=self.__token,
                params=json_params,
            ).json()
        else:
            results = requests.get(
                self.__url + "/api/2.0" + endpoint, headers=self.__token
            ).json()
        if printJson:
            print(json.dumps(results, indent=4, sort_keys=True))
        return results

    def post(self, endpoint, json_params={}, printJson=True):
        if json_params:
            raw_results = requests.post(
                self.__url + "/api/2.0" + endpoint,
                headers=self.__token,
                json=json_params,
            )
            results = raw_results.json()
        else:
            print("Must have a payload in json_args param.")
            return {}
        if printJson:
            print(json.dumps(results, indent=4, sort_keys=True))
        # if results are empty, let's return the return status
        if results:
            results["http_status_code"] = raw_results.status_code
            return results
        else:
            return {"http_status_code": raw_results.status_code}

    def patch(self, endpoint, json_params={}, printJson=True):
        if json_params:
            raw_results = requests.patch(
                self.__url + "/api/2.0" + endpoint,
                headers=self.__token,
                json=json_params,
            )
            results = raw_results.json()
        else:
            print("Must have a payload in json_args param.")
            return {}
        if printJson:
            print(json.dumps(results, indent=4, sort_keys=True))
        # if results are empty, let's return the return status
        if results:
            results["http_status_code"] = raw_results.status_code
            return results
        else:
            return {"http_status_code": raw_results.status_code}

    def list_node_types(self, printJson=False):
        return sorted(
            map(
                lambda x: [
                    x["instance_type_id"],
                    str(x["memory_mb"] / 1024) + " GB",
                    x["num_cores"],
                ],
                client.get("/clusters/list-node-types")["node_types"],
            )
        )

    def get_cluster_list(self, alive=True):
        """ Returns an array of json objects for the running clusters. Grab the cluster_name or cluster_id """
        cl = self.get("/clusters/list", printJson=False)
        if alive:
            running = filter(lambda x: x["state"] == "RUNNING", cl["clusters"])
            for x in running:
                print(x["cluster_name"] + " : " + x["cluster_id"])
            return running
        else:
            return cl["clusters"]

    def get_spark_versions(self, printJson=False):
        versions = self.get("/clusters/spark-versions")["versions"]
        return versions

    def get_users_scim(self,):
        users = self.get("/preview/scim/v2/Users")
        return users
