import os
from subprocess import run
import requests
import json

from create_stack_dash import Config


#  Appends prefix to title and all occurrences of "measurement" value in the Grafana JSON file
def __add_prefix_to_grafana_json(grafana_json, prefix):
    grafana_json["dashboard"]["title"] = prefix + ' ' + grafana_json["dashboard"]["title"]
    if 'panels' in grafana_json["dashboard"]:
        for i in grafana_json["dashboard"]['panels']:
            for j in i:
                if 'targets' in j:
                    for k in i['targets']:
                        if 'measurement' in k:
                            k['measurement'] = prefix + '_' + k['measurement']


# Modifies green info bar at the top of dashboard to display info on current test run
def __modify_dashboard_info_bar(grafana_json, total_users, duration, endpoint_url):
    if "options" in grafana_json["dashboard"]['panels'][0]:
        if "content" in grafana_json["dashboard"]['panels'][0]["options"]:
            grafana_json["dashboard"]['panels'][0]["options"][
                "content"] = "<p style=\"background-color:green;\" style=\"text-align:left;\">The endpoint for this run is: \n%s. Total users are %s. Duration of test is %s seconds  </p>    " \
                             % (endpoint_url, total_users, duration)


# Used for port forwarding to appropriate Kubernetes pod in cluster, listens on any local address (0.0.0.0)
def __run_kubectl_port_forward():
    args = ['kubectl', 'port-forward', '--address', "0.0.0.0", '-n', "common", '-r', "grafana-service", '3000:80']

    run(args)


# responsible for posting the dashboard to Grafana and returning the URL to it
def __post_grafana_dash(config):
    grafana_api_key = config.grafana_key
    grafana_template = config.grafana_file
    prefix = config.prefix
    grafana_url = "http://localhost:3000/"
    total_users = config.total_users
    duration = config.duration
    icap_server = config.icap_server

    grafana_api_url = grafana_url + 'api/dashboards/db'

    headers = {
        "Authorization": "Bearer " + grafana_api_key,
        "Content-Type": "application/json"}

    # Modify grafana JSON to display current run's info
    with open(grafana_template) as json_file:
        grafana_json = json.load(json_file)
        __add_prefix_to_grafana_json(grafana_json, prefix)
        __modify_dashboard_info_bar(grafana_json, total_users, duration, icap_server)

    # perform the Kubernetes port forwarding to allow Grafana to be accessed via localhost

    # __run_kubectl_port_forward()

    # post Grafana request to kubernetes pod
    resp = requests.post(grafana_api_url, json=grafana_json, headers=headers)
    d = eval(resp.text)
    # if the response contains a URL, use it to build a url that links directly to the newly created dashboard
    if "url" in d:
        return grafana_url + d.get('url')
    else:
        print("Dashboard creation failed: {0}".format(resp.text))


def main(config):
    created_dashboard_url = __post_grafana_dash(config)

    if created_dashboard_url:
        print("Dashboard created at: ")
        print(created_dashboard_url)


# main: Gets command line arguments, creates dashboard in grafana, outputs URL in response (if any)
if __name__ == '__main__':
    main(Config)
