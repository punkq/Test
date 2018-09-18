# -*- coding:utf-8 -*-

import os
import redis

def main():
    redis_docker_name = 'bft-smart_redis_1'
    NODES_NUM = 4

    REDIS_IP = getDockerIP(redis_docker_name)
    r = redis.Redis(REDIS_IP, 6379)

    pipe = r.pipeline()
    pipe_size = 100000

    length = 0
    key_list = []
    print(r.pipeline())
    keys = r.keys()
    for key in keys:
        key_list.append(key)
        pipe.get(key)
        if length < pipe_size:
            length += 1
        else:
            for (k, v) in zip(key_list, pipe.execute()):
                print(k, v)
            length = 0
            key_list = []

    for (k, v) in zip(key_list, pipe.execute()):
        print(k, v)
    node_num = 4

def getDockerIP(dockerid):
    cmd = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + dockerid
    return os.popen(cmd, 'r', 20).read()

if __name__ == '__main__':
    main()
