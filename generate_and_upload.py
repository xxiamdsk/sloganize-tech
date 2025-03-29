import os
from openai import OpenAI
from datetime import datetime
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
REPO_NAME = "xxiamdsk/sloganize-tech"  # Replace with your repo

def generate_slogans():
    """Generate tech slogans using OpenAI API."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = "Generate 5 unique and creative tech slogans."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    slogans = response.choices[0].message.content.strip()
    return slogans

def create_file_with_slogans():
    """Create a text file with generated slogans."""
    slogans = generate_slogans()
    filename = f"slogans_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    
    with open(filename, "w") as f:
        f.write(slogans)
    
    return filename

def upload_to_github():
    """Upload the file to GitHub."""
    filename = create_file_with_slogans()
    
    with open(filename, "rb") as f:
        content = f.read().decode("utf-8")
    
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{filename}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "message": f"Add new slogans file {filename}",
        "content": content.encode("utf-8").decode("utf-8")
    }

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"File {filename} uploaded successfully!")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    upload_to_github()
