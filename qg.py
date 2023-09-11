import requests
import base64
import os
from collections import defaultdict

project_key = "vddmvddm_go-web-app"
api_token = "7c52861a7dc76ff56d46553b04ab94f6986a0028"

api_endpoint = "https://api.openai.com/v1/completions"
api_key = os.getenv("OPENAI_API_KEY")
llm_model = "text-davinci-003"

headers = {
    "Authorization": "Basic " + base64.b64encode((api_token + ":").encode()).decode()
}

def communicate_with_ai(api_endpoint, api_key, file_content, issue):
    request_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    request_data = {
        "model": f"{llm_model}",
        "prompt": f"Please fix SonarQube issues for this file: {file_content} \n It has such issues: {issue}. No text, no description , no explanations, only code.\n Every possible text as a comment",
        "max_tokens": 1500,
        "temperature": 0.7
    }

    response = requests.post(api_endpoint, headers=request_headers, json=request_data)

    if response.status_code == 200:
        error_fix = response.json()["choices"][0]["text"]
        return error_fix
    else:
        return None

# Get project quality gate status
status_url = "https://sonarcloud.io/api/qualitygates/project_status?projectKey=" + project_key
status_response = requests.get(status_url, headers=headers).json()

quality_gate_status = status_response["projectStatus"]["status"]
print(f"Quality Gate Status: {quality_gate_status}")

if quality_gate_status != "OK":
    issues_url = "https://sonarcloud.io/api/issues/search?projects=" + project_key + "&statuses=OPEN,REOPENED,CONFIRMED"
    issues_response = requests.get(issues_url, headers=headers).json()

    issues_by_file = defaultdict(list)

    for issue in issues_response["issues"]:
        component = issue["component"]
        file_path = [comp["path"] for comp in issues_response["components"] if comp["key"] == component][0]
        message = issue["message"]
        issues_by_file[file_path].append(message)

    for file_path, issues in issues_by_file.items():
        print(f"File: {file_path}")

        # Read file content
        try:
            with open(file_path, "r") as file:
                file_content = file.read()
        except FileNotFoundError:
            print("  - File not found in the specified directory.")
            continue

        # Iterate through issues
        for issue in issues:
            print(f"  - Issue: {issue}")
            error_fix = communicate_with_ai(api_endpoint, api_key, file_content, issue)
            if error_fix:
                print(f"  - Suggested fix: {error_fix}")
            else:
                print("  - No suggested fix was provided.")
else:
    print("Quality gate passed.")
