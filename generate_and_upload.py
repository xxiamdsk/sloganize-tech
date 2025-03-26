import openai
import os
import requests
from datetime import datetime
import base64

# Load environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_OWNER = "xxiamdsk"
REPO_NAME = "sloganize-tech"
BRANCH = "main"
FILENAME = "tech_slogans.txt"


def generate_slogans():
    prompt = "Generate 5 unique and creative tech slogans."
    
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    slogans = response.choices[0].text.strip()
    return slogans


def create_file_with_slogans():
    slogans = generate_slogans()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"Tech Slogans ({timestamp})\n\n{slogans}"
    
    with open(FILENAME, "w", encoding="utf-8") as file:
        file.write(content)
    
    return content


def upload_to_github():
    content = create_file_with_slogans()
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILENAME}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if the file exists in the repo
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha", "")

    # Encode content to base64 for GitHub API
    encoded_content = base64.b64encode(content.encode()).decode()

    data = {
        "message": "Update tech slogans",
        "content": encoded_content,
        "branch": BRANCH,
    }

    if sha:
        data["sha"] = sha  # Required for updating existing files

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        print("✅ File uploaded successfully!")
    else:
        print(f"❌ Failed to upload file: {response.text}")


if __name__ == "__main__":
    upload_to_github()
