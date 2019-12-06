

import Utils
import threading
import time
import os



#global_controller_id = Utils.startGlobal()
#agent_controller_id = Utils.startAgent("127.0.0.1")

#if(Utils.uploadPlugin()):
#    print("Plugin Uploaded to Global Controller")

os.system('cd /Users/cody/IdeaProjects/filerepo ; mvn clean package bundle:bundle')

Utils.deleteAllCADL(True)

Utils.uploadFile("/Users/cody/IdeaProjects/filerepo/target/filerepo-1.0-SNAPSHOT.jar")

jarfile, version, md5 = Utils.getListRepo("io.cresco.filerepo")

app = "{\"pipeline_id\":\"0\",\"pipeline_name\":\"tester\",\"nodes\":[{\"type\":\"dummy\",\"node_name\":\"Plugin0\",\"node_id\":0,\"isSource\":false,\"workloadUtil\":0,\"params\":{\"pluginname\":\"io.cresco.filerepo\",\"jarfile\":" + jarfile +",\"version\":" + version + ",\"md5\":" + md5 +",\"scan_repo\":\"t\",\"scan_dir\":\"\/Users\/cody\/IdeaProjects\/filerepo\/data\",\"location_region\":\"global-region\",\"location_agent\":\"global-controller\"}}],\"edges\":[]}"

Utils.addCADL(app,True)

exit(0)


def thread_function():
    applist = []
    for x in range(0, 1):
        pipeline_id = Utils.addCADL(Utils.DOUBLE_CADL, True)
        applist.append(pipeline_id)
        print("Plugin Uploaded Application to Global Controller : Id :" + pipeline_id)

    for pipeline_id in applist:
        Utils.delCADL(pipeline_id, True)

while(True):
    threads = []
    for i in range(25):
        t = threading.Thread(target=thread_function)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

exit(0)


applist = []


#pipeline_id = Utils.addCADL(DOUBLE_CADL, False)


for x in range(0, 50):

    pipeline_id = Utils.addCADL(Utils.DOUBLE_CADL, False)
    applist.append(pipeline_id)
    print("Plugin Uploaded Application to Global Controller : Id :" + pipeline_id)


#for pipeline_id in applist:
#    Utils.delCADL(pipeline_id, False)

#Utils.stopContainter(global_controller_id)
#Utils.stopContainter(agent_controller_id)
