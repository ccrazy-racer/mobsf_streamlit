# mobsf_streamlit
This repo has an implementation with UI from Streamlit, created using MobSf REST API. Run this project by running run_all_apps.py

Create a folder called reports inside the same folder where these Python files are present, or else you will get an error saying the reports folder does not exist.

And also in "flask_app.py" and "streamlit_app.py" I have marked "ADD YOUR LOCAL IP ADDR" change it to your machine's local IP ADDR so that it will work.


# MobSF Streamlit UI Integration

This repository contains an implementation with a user interface (UI) built with Streamlit, utilizing the MobSF (Mobile Security Framework) REST API. You can run this project by executing `run_all_apps.py`.

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/ccrazy-racer/mobsf-streamlit.git
   cd mobsf-streamlit

2. Create a folder named "reports" within the same directory as the Python files. This folder is necessary for the application to store reports. If you skip this step, you may encounter an error indicating that the "reports" folder does not exist.

3. Open the "flask_app.py" and "streamlit_app.py" files and locate the line marked "ADD YOUR LOCAL IP ADDR." Replace this placeholder with your machine's local IP address. This is crucial for the application to work correctly.


## Running the Application
To start the MobSF Streamlit UI Integration, run the following command with admin privilages:
```bash
python run_all_apps.py
```
The application will launch in your web browser, and you can begin using the Streamlit-based UI for MobSF.

## Usage
1. Access the UI in your web browser.

2. Use the provided interface to interact with MobSF via its REST API.

3. Perform security assessments and analyze mobile apps for vulnerabilities.

4. The application will save reports in the "reports" folder within the project directory.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow the Contribution Guidelines.

## Acknowledgments
MobSF: Mobile Security Framework
Streamlit: Streamlit - The fastest way to create web apps



### ccrazy-racer
### passowrd protection
```
at C:\Users\<username>\.streamlit create a secrets.toml file 
sample file 
# .streamlit/secrets.toml

[passwords]

alice= "lit123"
bob = "pwd2"
```
## enabling passowrd authentication 
simple change want_password=True in streamli_app.py in line 13