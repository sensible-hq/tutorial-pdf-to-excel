# Import necessary libraries
import os
import requests

# Retrieve the Sensible API key from environment variables
SENSIBLE_API_KEY = os.getenv('SENSIBLE_API_KEY')

# Define the Bearer token prefix
BEARER = "Bearer"

# Define the function to extract content from a PDF file
def extract_content(d_type: str, d_name: str, env: str) -> dict:
    # Construct the URL for the API endpoint
    url = f"https://api.sensible.so/v0/extract/{d_type}?environment={env}"

    # Define the headers for the API request
    headers = {
        "Authorization": f"{BEARER} {SENSIBLE_API_KEY}",
        "content-type": "application/pdf"
    }

    # Open the PDF file in binary mode
    with open(d_name, 'rb') as fp:
        pdf_file = fp.read()
        # Send a POST request to the API and get the response
        response = requests.post(url, headers=headers, data=pdf_file)

        print(f"Extraction Status code: {response.status_code}")
        # If the request is successful, return the JSON response
        if response.status_code == 200:
            return response.json()
        # If the request fails, print the JSON response
        else:
            print(response.json())

# Define the function to convert the extracted content to an Excel file
def convert_to_excel(ids: str) -> str:
    # Construct the URL for the API endpoint
    url = f"https://api.sensible.so/v0/generate_excel/{ids}"

    # Define the headers for the API request
    headers = {
        "accept": "application/json",
        "authorization": f"{BEARER} {SENSIBLE_API_KEY}"
    }

    # Send a GET request to the API and get the response
    response = requests.get(url, headers=headers)

    print(f"Conversion Status code: {response.status_code}")
    # If the request is successful, return the URL for the Excel file
    if response.status_code == 200:
        data = response.json()
        return data["url"]
    # If the request fails, print the JSON response
    else:
        print(response.json())

# Define the function to download the Excel file
def download_xlsx(url: str, d_name: str) -> None:
    # Send a GET request to the URL and get the response
    response = requests.get(url)
    # Define the filename for the downloaded file
    filename = f"{d_name}.xlsx"
    # Open the file in binary mode and write the response content to it
    with open(filename, "wb") as fp:
        fp.write(response.content)

    print(f"{filename} downloaded.")

# Define the document type, environment, and document name
document_type = "covid_reports"
environment = "development"
document_name = "pdfs/20230301_Weekly_Epi_Update_132.pdf"

# Extract content from the PDF file
pdf_content = extract_content(document_type, document_name, environment)

# Convert the extracted content to an Excel file
url = convert_to_excel(pdf_content["id"])

# If the URL is not None, download the Excel file
if url is not None:
    download_xlsx(url, document_name[:-4])
