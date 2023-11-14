

import argparse
import os
import json
# decode args
def ArgInit():
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--install', action='store_const', dest='install',
        const='1',
        help='install dependent environment')
    parser.add_argument('-U', '--update', action='store_const', dest='update',
        const='1',
        help='update all')
    parser.add_argument('-p', '--private', action='store_const', dest='private',
        const='1',
        help='show private key')
    parser.add_argument('-P', '--public', action='store_const', dest='public',
        const='1',
        help='show public key')
    parser.add_argument('--start', action='store_const', dest='start',
        const='1',
        help='start the service')
    parser.add_argument('--stop', action='store_const', dest='stop',
        const='1',
        help='stop the service')
    parser.add_argument('-v', '--version', action='version', version='v0.1.1')

    results = parser.parse_args()
    
    if results.install != None:
        install()
    if results.update != None:
        update()
    if results.private != None:
        private()
    if results.public != None:
        public()
    if results.start != None:
        start()
    if results.stop != None:
        stop()

# color output
def red_str(str):
    return "\033[1;31m"+str+"\033[0m"
def green_str(str):
    return "\033[1;32m"+str+"\033[0m"
def check_su():
    res = os.geteuid()
    if res != 0:
        print(red_str("This command must be used with root privileges"))
        exit()

def install():
    print("Installing...")
    check_su()
    os.system("curl -fsSL https://test.docker.com -o test-docker.sh")
    os.system("sh test-docker.sh")
    os.system("apt update")
    os.system("apt install docker-compose -y")
    os.system("apt install git -y")
    os.system("git clone https://github.com/AeroNyxNetwork/NodeDocker.git /opt/node_docker")
    os.system("chmod a+rw /opt/node_docker/data/aero_nyx_db/logs")
    os.system("docker-compose -f /opt/node_docker/docker-compose.yml pull")
    print("Result:"+green_str("success"))
    
def update():
    print("update")
    #  
    
def private():
    r = os.popen("docker exec aero_nyx_node cat /opt/server_config.json")
    obj = json.loads(r.read())
    print("private key:0x" + obj["pri_key"])
    
def public():
    r = os.popen("docker exec aero_nyx_node cat /opt/server_config.json")
    obj = json.loads(r.read())
    print("public key:0x" + obj["pub_key"])
    
def start():
    print("starting...")
    os.system("docker-compose -f /opt/node_docker/docker-compose.yml  up -d")
    
def stop():
    print("stopping...")
    os.system("docker-compose -f /opt/node_docker/docker-compose.yml  down")

if __name__ == "__main__":
    ArgInit()
