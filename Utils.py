

def isStarted(container):
    import docker
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
    import docker
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
    import docker
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
    import docker
    client = docker.from_env()
    return client.containers.get(container_id).attrs['NetworkSettings']['IPAddress']

def stopContainter(container_id):
    import docker
    import time

    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    while container.status == 'running':
        container.reload()
        time.sleep(1)
        print("Waiting on container " + container_id + " to stop : status=" + container.status)

def uploadPlugin():
    import requests

    jarfile = "filerepo-1.0-SNAPSHOT.jar"

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

def uploadFile(jarfile):
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
    import requests
    import time

    data = {"tenant_id": "0", "pipeline": CADL}

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
        status = getStatus(pipeline_id)
        while (status != "10") and (status != "50"):
            time.sleep(.5)
            status = getStatus(pipeline_id)
            #print(status)

    return pipeline_id


def getListRepo(pluginname):
    import requests

    response = requests.get(url='http://localhost:8181/dashboard/plugins/listrepo',headers={'Content-Type': 'application/x-www-form-urlencoded', "X-Auth-API-Service-Key": "BDB"})
    #print(response.status_code)
    #print(response.json())
    json_response = response.json()
    for pipeline in json_response['plugins']:
        #print(pipeline)
        if pipeline['pluginname'] == pluginname:
            #print(pipeline['pluginname'])
            return pipeline['jarfile'], pipeline['version'], pipeline['md5']

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
    import time

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

def deleteAllCADL(block):
    import requests

    response = requests.get(url='http://localhost:8181/dashboard/applications/list',headers={'Content-Type': 'application/x-www-form-urlencoded', "X-Auth-API-Service-Key": "BDB"})
    #print(response.status_code)
    #print(response.json())
    json_response = response.json()
    for pipeline in json_response['pipelines']:
        #print(pipeline)
        if pipeline['status_code'] == "10":
            delCADL(pipeline['pipeline_id'], block)

SINGLE_CADL = "{\"pipeline_id\": \"0\",\"pipeline_name\": \"singleapp\",\"nodes\": [{\"type\": \"dummy\",\"node_name\": \"Plugin 0\",\"node_id\": 0,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"global-controller\"}}],\"edges\": []}"
DOUBLE_CADL = "{\"pipeline_id\": \"0\",\"pipeline_name\": \"singleapp\",\"nodes\": [{\"type\": \"dummy\",\"node_name\": \"Plugin 0\",\"node_id\": 0,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"global-controller\"}},{\"type\": \"dummy\",\"node_name\": \"Plugin 1\",\"node_id\": 1,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"agent-controller\"}}],\"edges\": []}"
