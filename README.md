# AeroNyxTools
Tools for deploying AeroNyxNode services.

# Deploy
## Download source
```shell
git clone https://github.com/AeroNyxNetwork/AeroNyxTools.git
cd AeroNyxTools/
```

## Deploy Environment
```shell
python3 main.py -I
```

## Register node
```shell
python3 main.py --set_register --owner=04778899 --port=10003 --name=node_name --country=US
```
- owner--Onwer of node (You can copy the pubkey from the AeroNyx client as the owner of the node)
- port--Port of node
- name--Name of node
- country--Country code of node

## Run service
```sheel
python3 main.py --start
```

# More
```
-h, --help     show this help message and exit
-I, --install  install dependent environment
-U, --update   update all
-p, --private  show private key
-P, --public   show public key
--start        start the service
--stop         stop the service
-v, --version  show program's version number and exit
```
