def isStarted(container):
    isStarted = False
    startString = "[agent: io.cresco.agent.core][o.c.StaticPluginLoader] Starting SYSINFO : Status Active: true Status State: GLOBAL'"

    while (not isStarted):
        for line in container.logs(stream=True):
            if startString in str(line.strip()):
                isStarted = True
                break
            else:
                print(str(line))

    return True
