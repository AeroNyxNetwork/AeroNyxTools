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
    
    # version, owner, port, name, country
    parser.add_argument('--set_register', action='store_const', dest='set_register',
        const='1',
        help='register node info')

    parser.add_argument('--owner', action='store', dest='owner',
        help='setup owner of node')

    parser.add_argument('--port', action='store', dest='port',
        help='setup port of node')

    parser.add_argument('--name', action='store', dest='name',
        help='setup name of node')

    parser.add_argument('--country', action='store', dest='country',
        help='setup owncountryer of node')
        
    parser.add_argument('--register', action='store_const', dest='register',
        const='1',
        help='show register node info')

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
    if results.set_register != None:
        set_register("0.0.1", results.owner, results.port, results.name, results.country)
    if results.register != None:
        register()


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

def set_register(version, owner, port, name, country):
    country_list = ["AD","AE","AF","AG","AI","AL","AM","AO","AR","AT","AU","AZ","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BR","BS","BW","BY","BZ","CA","CF","CG","CH","CK","CL","CM","CN","CO","CR","CS","CU","CY","CZ","DE","DJ","DK","DO","DZ","EC","EE","EG","ES","ET","FI","FJ","FR","GA","GB","GD","GE","GF","GH","GI","GM","GN","GR","GT","GU","GY","HK","HN","HT","HU","ID","IE","IL","IN","IQ","IR","IS","IT","JM","JO","JP","KE","KG","KH","KP","KR","KT","KW","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","MG","ML","MM","MN","MO","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NE","NG","NI","NL","NO","NP","NR","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PR","PT","PY","QA","RO","RU","SA","SB","SC","SD","SE","SG","SI","SK","SL","SM","SN","SO","SR","ST","SV","SY","SZ","TD","TG","TH","TJ","TM","TN","TO","TR","TT","TW","TZ","UA","UG","US","UY","UZ","VC","VE","VN","YE","YU","ZA","ZM","ZR","ZW"]
    file_path = "/opt/node_docker/data/aero_nyx_sync/config.json"
    json_file = open(file_path, "w")
    json_obj = {
        "version": version, 
        "owner": owner, 
        "port": port,
        "name": name,
        "country": country
    }
    if version == None or owner == None or port==None or name == None or country==None:
        print("set register faild, must set owner,port,name,country in same time.")
    elif not port.isdigit():
        print("set register faild, port must be digit.")
    elif country not in country_list:
        print("set register faild, country must be the country code, such as 'US', 'JP'")
    else:
        json.dump(json_obj, json_file)
        print("set register success")
        
def register() :
    r = os.popen("docker exec aero_nyx_sync cat /opt/aero_nyx_sync/config.json")
    obj = json.loads(r.read())
    print(obj)

#python3 main.py --set_register --owner=0432215ed9e25b8fc3e38a6df609ce46995b418b99082d367d7999c07496373b1f5e6ee09375c4f7e423f5a53cb7fc9e75f4cf8a13c0106799a9be01f759f264a6 --port=1011 --name=name111 --country=CN
if __name__ == "__main__":
    ArgInit()



