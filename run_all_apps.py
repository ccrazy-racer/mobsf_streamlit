import subprocess
import time
import docker

def run_all_apps(is_running: bool):
    # Run MobSf dcoker container.
    if is_running == False:
        mobsf_command = ['docker', 'run', '-it', '-p', '8000:8000', 'opensecurity/mobile-security-framework-mobsf:latest']
        mobsf_process = subprocess.Popen(mobsf_command)
        time.sleep(30)
        
    
    # Define the command to run your Flask app (replace 'flask_app.py' with your Flask script)
    flask_command = ['python', 'flask_app.py']

    # Define the command to run your Streamlit app (replace 'streamlit_app.py' with your Streamlit script)
    streamlit_command = ['streamlit', 'run', 'streamlit_app.py']

    # Use subprocess to run Flask and Streamlit apps in separate processes
    
    
    flask_process = subprocess.Popen(flask_command)
    time.sleep(5)
    streamlit_process = subprocess.Popen(streamlit_command)

    # Wait for both processes to complete (or interrupt with Ctrl+C)
    mobsf_process.wait()
    flask_process.wait()
    streamlit_process.wait()
    


def is_container_running(container_name: str):
    """Verify the status of a container by it's name

    :param container_name: the name of the container
    :return: boolean or None
    """
    RUNNING = "running"
    # Connect to Docker using the default socket or the configuration
    # in your environment
    docker_client = docker.from_env()
    # Or give configuration
    # docker_socket = "unix://var/run/docker.sock"
    # docker_client = docker.DockerClient(docker_socket)

    try:
        container = docker_client.containers.get(container_name)
    except docker.errors.NotFound as exc:
        return False
    else:
        container_state = container.attrs["State"]
        return container_state["Status"] == RUNNING


if __name__ == '__main__':
    container_name = "opensecurity/mobile-security-framework-mobsf:latest"
    is_running = is_container_running(container_name)
    run_all_apps(is_running)
