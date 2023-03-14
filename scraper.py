import os
import requests


API_KEY = os.getenv('API_KEY')


def extract_content(d_type: str, d_name: str, env: str) -> dict:
    """
    Extract content from a PDF file.
    """
    url = f"https://api.sensible.so/v0/extract/{d_type}?environment={env}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/pdf"
    }

    with open(d_name, 'rb') as fp:
        pdf_file = fp.read()
        response = requests.post(url, headers=headers, data=pdf_file)

        print(f"Extraction Status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json())

def convert_to_excel(ids: str) -> str:
    url = f"https://api.sensible.so/v0/generate_excel/{ids}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers,)

    print(f"Conversion Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        return data["url"]
    else:
        print(response.json())

def download_xlsx(url: str, d_name: str) -> None:
    response = requests.get(url)
    filename = f"{d_name}.xlsx"
    with open(filename, "wb") as fp:
        fp.write(response.content)

    print(f"{filename} downloaded.")

# Extract content from a PDF file and save to Excel.

document_type = "covid_reports"
environment = "development"
document_name = "pdfs/20230301_Weekly_Epi_Update_132.pdf"

pdf_content = extract_content(document_type, document_name, environment)

url = convert_to_excel(pdf_content["id"])

if url is not None:
    download_xlsx(url, document_name[:-4])