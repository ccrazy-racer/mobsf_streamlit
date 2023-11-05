import subprocess
import time

def run_all_apps():
    # Run MobSf dcoker container.
    mobsf_command = ['docker', 'run', '-it', '-p', '8000:8000', 'opensecurity/mobile-security-framework-mobsf:latest']
    
    # Define the command to run your Flask app (replace 'flask_app.py' with your Flask script)
    flask_command = ['python', 'flask_app.py']

    # Define the command to run your Streamlit app (replace 'streamlit_app.py' with your Streamlit script)
    streamlit_command = ['streamlit', 'run', 'streamlit_app.py']

    # Use subprocess to run Flask and Streamlit apps in separate processes
    mobsf_process = subprocess.Popen(mobsf_command)
    time.sleep(30)
    flask_process = subprocess.Popen(flask_command)
    streamlit_process = subprocess.Popen(streamlit_command)

    # Wait for both processes to complete (or interrupt with Ctrl+C)
    mobsf_process.wait()
    flask_process.wait()
    streamlit_process.wait()
    
if __name__ == '__main__':
    run_all_apps()
