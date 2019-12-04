import time
import docker
import Utils

client = docker.from_env()

global_controller_env = "test"
global_container = client.containers.run("docker.io/crescoedgecomputing/quickstart", environment=["is_global=true","region_name=" + global_controller_env], detach=True, auto_remove=True)
global_container.reload()

global_container_ip = global_container.attrs['NetworkSettings']['IPAddress']

print("Starting Global Controller")
if Utils.isStarted(global_container):
    print("Global Controller Started")
    #global_container.stop()


