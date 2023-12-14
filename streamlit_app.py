import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import webbrowser
import time
from datetime import date
import os

today = date.today()

tab1, tab2 = st.tabs(["Scan App", " 🕓 Recent Scans"])
want_password=True

# Define the path to the directory where reports are stored
reports_directory = 'reports'  # Replace with your actual directory path

# Function to get a list of apps
def get_apps():
    app_list = os.listdir(reports_directory)
    return app_list

# Function to get a list of reports for a specific app
def get_reports(app_name):
    app_reports = []
    app_dir = os.path.join(reports_directory, app_name)
    if os.path.exists(app_dir):
        app_reports = sorted(os.listdir(app_dir), reverse=True)
    return app_reports


# Function to create or check the existence of a folder for the app
def create_or_check_app_folder(app_name):
    app_dir = os.path.join(reports_directory, app_name)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    return app_dir

def streamlit():
    
    # Define the API key and server URL
    SERVER_URL = 'http://ADD YOUR LOCAL IP ADDR:81'
    tab1.title("File Upload and Scan")

    # Initialize session_state
    if 'api_data' not in st.session_state:
        st.session_state.api_data = None
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    if 'uploaded' not in st.session_state:
        st.session_state.uploaded = None


    
    
    # Upload file
    uploaded_file = tab1.file_uploader("Choose a file:")

    if uploaded_file:
        tab1.write("File selected successfully")

        # Define the "Upload and Scan" button
        if tab1.button("Upload"):
            # Perform file upload and scan
            tab1.write("Uploading the file...")

            multipart_data = MultipartEncoder(fields={'file': (uploaded_file.name, uploaded_file, 'application/octet-stream')})
            headers = {'Content-Type': multipart_data.content_type}
            response = requests.post(f'{SERVER_URL}/api/v1/upload', data=multipart_data, headers=headers)
            
            if response.status_code == 200:
                tab1.write("Upload completed successfully.")
                resp = json.loads(response.text)
                st.session_state.api_data = resp['hash']
                st.session_state.file_name = resp['file_name']
                st.session_state.uploaded = True
            else:
                tab1.write(f"Upload failed: {response.text}")

        # Scan file
        if st.session_state.uploaded == True:
            if tab1.button("Scan"):
                tab1.write("Scanning the file...")
                headers = {'Content-Type': 'application/json'}
                scan_response = requests.get(f'{SERVER_URL}/api/v1/scan/{st.session_state.api_data}', headers=headers)        
                if scan_response.status_code == 200:
                    print(scan_response.text)
                    tab2.write("Wait for 2 minutes do not refresh page... later press on download...")
                else:
                    tab1.write(f"Scan failed: {scan_response.text}")

            # Download report button
            if tab1.button("Download Report"):
                    tab1.write("Downloading report...")
                    
                    # Define the report download URL and save the report locally
                    download_url = f'{SERVER_URL}/api/v1/download_pdf/{st.session_state.api_data}'
                    response = requests.get(download_url, stream=True)

                    if response.status_code == 200:
                        app_folder = create_or_check_app_folder(st.session_state.file_name)
                        with open(os.path.join(app_folder,f"{st.session_state.file_name}_report_{today.strftime('%b-%d-%Y')}.pdf"), "wb") as pdf_file:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    pdf_file.write(chunk)
                        tab1.write("Report downloaded as report.pdf")
                    else:
                        tab1.write(f"Report download failed: {response.text}")
                        
                        
    # Streamlit UI
    # st.title("Recent Scans")

    # Button to view recent scans
    tab2.title("Recent Scans")
    tab2.header("Apps")
    app_list = get_apps()
    selected_app = tab2.selectbox("Select an App", app_list, index=None, placeholder="Select an app...",)

    if selected_app:
        tab2.header(f"Reports for {selected_app}")
        app_reports = get_reports(selected_app)
        
        if not app_reports:
            tab2.write(f"No reports found for {selected_app}.")
        else:
            tab2.write("Select a report to view or download:")
            selected_report = tab2.selectbox("Select a Report", app_reports, index=None, placeholder="Select any report...",)
            if selected_report:
                report_path = os.path.join(reports_directory, selected_app, selected_report)

                if selected_report.lower().endswith('.pdf'):
                    # Provide a download button for the PDF
                    with open(report_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()
                    tab2.download_button(label="Download report", data= PDFbyte, file_name= selected_report)
                else:
                    tab2.write("This report is not a PDF file and cannot be displayed.")
                    




#----------------
# streamlit_app.py

import hmac


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

if(want_password):
    if not check_password():
        st.stop()

# Main Streamlit app starts here


#---------------

if __name__ == '__main__':
    streamlit()
