import time
import docker

def isStarted(container):
    isStarted = False
    startString = "[agent: io.cresco.agent.core][o.c.StaticPluginLoader] Starting SYSINFO : Status Active: true Status State: GLOBAL'"

    while (not isStarted):
        for line in container.logs(stream=True):
            if startString in str(line.strip()):
                print(str(line.strip()))
                isStarted = True
                break
            else:
                print(str(line))

    return True


def startGlobal():
    client = docker.from_env()

    cresco_image = "docker.io/crescoedgecomputing/quickstart"
    # global_controller_env = ["CRESCO_region_name=test", "CRESCO_agent_name=global"]
    global_controller_env = {
        "CRESCO_regionname": "global-region",
        "CRESCO_agentname": "global-controller",
        "CRESCO_is_global": "true",
        "CRESCO_discovery_secret_global": "gsec",
        "CRESCO_discovery_secret_region": "rsec",
        "CRESCO_discovery_secret_agent":  "asec"
    }

    global_controller_ports = {
        '8181/tcp': 8181,
        '32005/tcp': 32005,
        '32005/udp': 32005,
        '32010/tcp': 32010
    }

    global_container = client.containers.run(cresco_image, environment=global_controller_env, ports=global_controller_ports, detach=True, auto_remove=True)
    print("Starting Global Controller")
    if isStarted(global_container):
        print("Global Controller Started")
        # global_container.stop()

    return global_container.id

def startAgent(controllerIP):
    client = docker.from_env()

    cresco_image = "docker.io/crescoedgecomputing/quickstart"
    # global_controller_env = ["CRESCO_region_name=test", "CRESCO_agent_name=global"]

    global_controller_env = {
        "CRESCO_regionname": "global-region",
        "CRESCO_agentname": "agent-controller",
        "regional_controller_host": controllerIP,
        "CRESCO_is_agent": "true",
        "CRESCO_discovery_secret_global": "gsec",
        "CRESCO_discovery_secret_region": "rsec",
        "CRESCO_discovery_secret_agent": "asec"
    }

    global_container = client.containers.run(cresco_image, environment=global_controller_env, detach=True, auto_remove=True)
    print("Starting Global Controller")
    if isStarted(global_container):
        print("Global Controller Started")
        # global_container.stop()

    return global_container.id

def getContainterIP(container_id):
    client = docker.from_env()
    return client.containers.get(container_id).attrs['NetworkSettings']['IPAddress']

def stopContainter(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    while container.status == 'running':
        container.reload()
        time.sleep(1)
        print("Waiting on container " + container_id + " to stop : status=" + container.status)