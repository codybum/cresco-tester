import time
import docker

def isStarted(container):
    isStarted = False
    startString = "[agent: io.cresco.agent.core][o.c.StaticPluginLoader] Starting SYSINFO"

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
        print("Global Controller Started ID: " + global_container.id)
        # global_container.stop()

    return global_container.id

def startAgent(controllerIP):
    client = docker.from_env()

    cresco_image = "docker.io/crescoedgecomputing/quickstart"
    # global_controller_env = ["CRESCO_region_name=test", "CRESCO_agent_name=global"]

    agent_controller_env = {
        "CRESCO_regionname": "global-region",
        "CRESCO_agentname": "agent-controller",
        "regional_controller_host": controllerIP,
        "CRESCO_is_agent": "true",
        "CRESCO_discovery_secret_global": "gsec",
        "CRESCO_discovery_secret_region": "rsec",
        "CRESCO_discovery_secret_agent": "asec"
    }

    agent_container = client.containers.run(cresco_image, environment=agent_controller_env, detach=True, auto_remove=True)
    print("Starting Agent Controller")
    if isStarted(agent_container):
        print("Agent Controller Started ID: " + agent_container.id)
        # global_container.stop()

    return agent_container.id

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

def uploadPlugin():
    jarfile = "filerepo-1.0-SNAPSHOT.jar"

    import requests

    data = open(jarfile, 'rb').read()
    res = requests.post(url='http://localhost:8181/dashboard/plugins/uploadplugin',
                        data=data,
                        headers={'Content-Type': 'application/java-archive', "X-Auth-API-Service-Key": "BDB"})
    status = res.status_code
    res.close()

    if status == 200:
        return True
    else:
        return False


def addCADL(CADL, block):

    data = {"tenant_id": "0", "pipeline": CADL}

    import requests

    res = requests.post(url='http://localhost:8181/dashboard/applications/add',
                        data=data,
                        headers={'Content-Type': 'application/x-www-form-urlencoded', "X-Auth-API-Service-Key": "BDB"})
    status = res.status_code
    json_response = res.json()
    pipeline_id = json_response['gpipeline_id']
    res.close()

    if status != 200:
        print("Error uploading addCADL")

    if block:
        while getStatus(pipeline_id) != "10":
            time.sleep(.5)

    return pipeline_id

def getStatus(pipeline_id):

    import requests
    response = requests.get(url='http://localhost:8181/dashboard/applications/list',headers={'Content-Type': 'application/x-www-form-urlencoded', "X-Auth-API-Service-Key": "BDB"})
    #print(response.status_code)
    #print(response.json())
    json_response = response.json()
    for pipeline in json_response['pipelines']:
        #print(pipeline)
        if pipeline['pipeline_id'] == pipeline_id:
            #print(pipeline['status_code'])
            return pipeline['status_code']

def delCADL(pipeline_id, block):

    import requests
    url = 'http://localhost:8181/dashboard/applications/delete/' + pipeline_id
    #print(url)
    response = requests.get(url=url,headers={'Content-Type': 'application/x-www-form-urlencoded', "X-Auth-API-Service-Key": "BDB"})
    #print(response.status_code)
    #print(response.text)
    #json_response = response.json()
    #print(json_response)
    status = response.status_code
    response.close()

    if status != 200:
        print("Error uploading addCADL")

    if block:
        while getStatus(pipeline_id) != None:
            time.sleep(.5)
