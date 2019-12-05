
import Utils

global_controller_id = Utils.startGlobal()
agent_controller_id = Utils.startAgent("127.0.0.1")

if(Utils.uploadPlugin()):
    print("Plugin Uploaded to Global Controller")

applist = []

SINGLE_CADL = "{\"pipeline_id\": \"0\",\"pipeline_name\": \"singleapp\",\"nodes\": [{\"type\": \"dummy\",\"node_name\": \"Plugin 0\",\"node_id\": 0,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"global-controller\"}}],\"edges\": []}"
DOUBLE_CADL = "{\"pipeline_id\": \"0\",\"pipeline_name\": \"singleapp\",\"nodes\": [{\"type\": \"dummy\",\"node_name\": \"Plugin 0\",\"node_id\": 0,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"global-controller\"}},{\"type\": \"dummy\",\"node_name\": \"Plugin 1\",\"node_id\": 1,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"agent-controller\"}}],\"edges\": []}"

pipeline_id = Utils.addCADL(DOUBLE_CADL, False)

'''
for x in range(0, 1):

    pipeline_id = Utils.addCADL(DOUBLE_CADL, True)
    applist.append(pipeline_id)
    print("Plugin Uploaded Application to Global Controller : Id :" + pipeline_id)


for pipeline_id in applist:
    Utils.delCADL(pipeline_id, True)

Utils.stopContainter(global_controller_id)
Utils.stopContainter(agent_controller_id)
'''