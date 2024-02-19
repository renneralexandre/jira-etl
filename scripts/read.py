import json
import math
import os
import sys

# from urllib
import requests
from requests.auth import HTTPBasicAuth

import django


class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def printGreetings():
    print(Bcolors.HEADER, end="")
    print("====================")
    print("JIRA ETL version 1.0")
    print("Author: Renner")
    print("====================")
    print(Bcolors.ENDC, end="")


def djangoSetup():
    print("Loading django...", end="")
    caminho_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(caminho_projeto)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jira_etl_django_project.settings")
    django.setup()
    from jira_etl_django_apps.epic.models import Epic

    print(Bcolors.OKGREEN + "Done" + Bcolors.ENDC)


def listEpics():
    from jira_etl_django_apps.epic.models import Epic

    epics = Epic.objects.all()
    print(f"Quantidade de épicos: {Epic.objects.count()}")
    for epic in epics:
        print(epic.jiraEpicName)


def getJiraEpics():
    from jira_etl_django_apps.epic.models import Epic

    print("Retrieving Jira Epics...")
    # URL
    url = "https://skyone.atlassian.net/rest/api/3/search"

    # TOKEN
    JIRA_EMAIL = "renner.alexandre@skyone.solutions"
    JIRA_TOKEN = "ATATT3xFfGF0Ifzq4om7n_lm2YSfLO_uauuzPZ7U_TuilPO0LdU6nG0FozNWwsZ162-LSM1pUrYmuMi-t-9wan7c3CTkfsdUIN6BAUbJzdjNtUrYjLqFWULrTKPrHb-ckAkLw1BtZXyuwR8oiZgDf07sTcquRHwEkZL5gGn_EYRKHXNB7DCFZug=52F3F980"

    # HEADERS
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    # AUTH
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)

    start_at = 0
    max_results = 50
    epics = []
    page = 1

    while True:
        payload = json.dumps(
            {
                # "expand": ["names","schema","operations" ],
                "fields": [
                    "issuetype",
                    "project",
                    "summary",
                    "status",
                    "assignee",
                    "created",
                    "updated",
                    "resolutiondate",
                ],
                "fieldsByKeys": False,
                "jql": "project = AUTO AND issuetype = 'Epic' AND created >= '2022-12-01' AND created <= '2024-01-31'",
                "maxResults": max_results,
                "startAt": start_at,
            }
        )

        # REQUEST
        print(f"Retrieving page: { page } ")
        response = requests.request(
            "POST", url, data=payload, headers=headers, auth=auth
        )
        # TESTS
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

        # Check if the request was successful
        if response.status_code == 200:
            response_json = response.json()
            issues = response_json["issues"]
            total = response_json["total"]
            if page == 1:
                print(
                    Bcolors.WARNING
                    + f"Número total de registros informado pela API: {total}"
                    + Bcolors.ENDC
                )
                print(
                    Bcolors.WARNING
                    + f"Número de requisições será: {math.ceil(total/max_results)}"
                    + Bcolors.ENDC
                )
            for issue in issues:
                epic = Epic(
                    jiraIssueType=issue["fields"]["issuetype"]["name"],
                    jiraProject=issue["fields"]["project"]["name"],
                    jiraKey=issue["key"],
                    jiraEpicName=issue["fields"]["summary"],
                    jiraStatus=issue["fields"]["status"]["name"],
                    jiraAssignee=issue["fields"]
                    .get("assignee", {})
                    .get("displayName", "Unassigned"),
                    jiraCreatedDate=issue["fields"]["created"],
                    jiraUpdatedDate=issue["fields"]["updated"],
                    jiraResolvedDate=issue["fields"].get("resolutiondate"),
                )
                epics.append(epic)

            # Pagination check
            if len(issues) < max_results:
                break  # Exit loop if last page
            start_at += max_results
            page = page + 1
        else:
            print(f"Failed to retrieve epics: {response.status_code}")
            break
    # Return the list of epics
    print(f"Foram recuperados {len(epics)} registros.")
    return epics

def mergeEpics(epics_param):
    from jira_etl_django_apps.epic.models import Epic

    epic_from_api = epics_param
    # Recuperar todos os jiraKeys existentes do banco de dados
    epics_from_database = set(Epic.objects.values_list('jiraKey', flat=True))
    # print(epics_from_database)

    # Filtrar para manter apenas epics que não estão no banco de dados
    new_epics = [epic for epic in epic_from_api if epic.jiraKey not in epics_from_database]
    print(f"Foram encontrados {len(new_epics)} novos epics.")
    print(new_epics)

    # Bulk insert de novos epics
    Epic.objects.bulk_create(new_epics)
    print(f"Inserted {len(new_epics)} new epics into the database.")


if __name__ == "__main__":
    printGreetings()
    djangoSetup()
    mergeEpics(getJiraEpics())


