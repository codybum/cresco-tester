
import Utils
import time

#global_controller_id = Utils.startGlobal()
#print(Utils.getContainterIP(global_controller_id))
#Utils.stopContainter(global_controller_id)
#agent_controller_id = Utils.startAgent("127.0.0.1")

#if(Utils.uploadPlugin()):
#    print("Plugin Uploaded to Global Controller")

CADL = "{\"pipeline_id\": \"0\",\"pipeline_name\": \"singleapp\",\"nodes\": [{\"type\": \"dummy\",\"node_name\": \"Plugin 0\",\"node_id\": 0,\"isSource\": false,\"workloadUtil\": 0,\"params\": {\"pluginname\": \"io.cresco.filerepo\",\"jarfile\": \"ec9245ed-5406-4d65-80e1-572df888589d\",\"version\": \"1.0.0.SNAPSHOT-20191204-1922\",\"md5\": \"ac216b18a81f616e0bb6f9d21f274713\",\"location_region\": \"global-region\",\"location_agent\": \"global-controller\"}}],\"edges\": []}"

pipeline_id = Utils.addCADL(CADL, True)
print("Plugin Uploaded Application to Global Controller : Id :" + pipeline_id)



#Utils.delCADL(pipeline_id)