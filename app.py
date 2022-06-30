import os
import time 
li = []

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def getLineNumbers():
    linenum = -1
    with open("/etc/emqx/emqx.conf") as search:
        for line in search:
            linenum += 1
            line = line.rstrip()  # remove '\n' at end of line
            if "allow_anonymous = true" == line:
                setAnonymus = linenum
                li.append(setAnonymus)
                #print(line, " is at ", setAnonymus)
            if "node.name = emqx@127.0.0.1" == line:
                setEmqxIp = linenum
                li.append(setEmqxIp)
                #print(line, " is at ", setEmqxIp)
            if "listener.ssl.external.keyfile = /etc/emqx/certs/key.pem" == line:
                keyfile = linenum
                li.append(keyfile)
                #print(line, " is at ", keyfile)
            if "listener.ssl.external.certfile = /etc/emqx/certs/cert.pem" == line:
                certfile = linenum
                li.append(certfile)
                #print(line, " is at ", certfile)
            if "## listener.ssl.external.cacertfile = /etc/emqx/certs/cacert.pem" == line:
                cacertfile = linenum
                li.append(cacertfile)
                #print(line, " is at ", cacertfile)
    search.close()

def install_emqx():

    os.system("echo {} | sudo -S apt update".format(password))
    os.system("sudo cp emqx-ubuntu18.04-v3.1.1_amd64.deb ~/")
    os.system("cd ~")
    os.system("wget https://www.emqx.com/en/downloads/broker/3.1.1/emqx-ubuntu18.04-v3.1.1_amd64.deb")
    time.sleep(1)
    os.system("sudo dpkg -i \'emqx-ubuntu18.04-v3.1.1_amd64.deb\'")
    time.sleep(1)
    os.system("sudo cp emqx-ubuntu18.04-v3.1.1_amd64.deb ~")
    os.system("sudo systemctl start emqx")
    os.system("sudo systemctl enable emqx")
    time.sleep(1)
    os.system("sudo ufw allow 1883")
    os.system("sudo ufw allow 8883")
    time.sleep(2)
    os.system("sudo systemctl restart emqx")
    os.system("sudo emqx ping")
    time.sleep(1)
    os.system("sudo emqx_ctl plugins load emqx_auth_username")
    os.system("sudo emqx_ctl users add \'user1\' \'pass1\'")
    time.sleep(1)
    os.system("sudo mkdir /etc/ssl_certs/")
    os.system("sudo openssl req -new -x509 -days 3650 -subj \"/C=IN/ST=KAR/L=BLR/O=NEEWEE/CN={}\" -extensions v3_ca -keyout ca.key -outform pem -passout pass:qwertyuiop -out root-ca.pem".format(ip))
    os.system("sudo openssl genrsa -out server.key 2048")
    os.system("sudo openssl req -subj \"/C=IN/ST=KAR/L=BLR/O=NEEWEE/CN={}\" -out server.csr -key server.key -new".format(ip))
    os.system("sudo openssl x509 -req -in server.csr -CA root-ca.pem -CAkey ca.key -CAcreateserial -outform pem -out server.crt -days 3650 -passin pass:qwertyuiop")
    os.system("sudo cp ca.key /etc/ssl_certs/")
    os.system("sudo cp root-ca.pem /etc/ssl_certs/")
    os.system("sudo cp root-ca.srl /etc/ssl_certs/")
    os.system("sudo cp server.crt /etc/ssl_certs/")
    os.system("sudo cp server.csr /etc/ssl_certs/")
    os.system("sudo cp server.key /etc/ssl_certs/")
    
    os.system("sudo chown -R emqx:emqx /etc/ssl_certs/server.key /etc/ssl_certs/server.crt /etc/ssl_certs/root-ca.pem /etc/ssl_certs/server.csr /etc/ssl_certs/root-ca.srl")
    os.system("sudo systemctl restart emqx")
    os.system("sudo emqx_ctl users add \'user2\' \'pass2\'")
    os.system("sudo systemctl restart emqx")

ip = input("Enter your IP address of the machine : ")
password = input("Enter the password : ")

install_emqx()
getLineNumbers()
print(li)

setEmqxIp = li[0]
setAnonymus = li[1]
keyfile = li[2]
certfile = li[3]
cacertfile = li[4]

a_file = open("/etc/emqx/emqx.conf", "r")
list_of_lines = a_file.readlines()

# print(list_of_lines[setAnonymus])
# print(list_of_lines[setEmqxIp])
# print(list_of_lines[keyfile])
# print(list_of_lines[cacertfile])
# print(list_of_lines[certfile])

#--CMDS
os.system("cd /etc/emqx/")
setAnonymus_cmd = "allow_anonymous = false\n"
setEmqxIp_cmd = "node.name = emqx@"+ip+"\n"
keyfile_cmd = "listener.ssl.external.keyfile = /etc/ssl_certs/server.key\n"
cacertfile_cmd = "listener.ssl.external.cacertfile = /etc/ssl_certs/root-ca.pem\n"
certfile_cmd = "listener.ssl.external.certfile = /etc/ssl_certs/server.crt\n"

replace_line("/etc/emqx/emqx.conf", setAnonymus, setAnonymus_cmd)
replace_line("/etc/emqx/emqx.conf", setEmqxIp, setEmqxIp_cmd)
replace_line("/etc/emqx/emqx.conf", keyfile, keyfile_cmd)
replace_line("/etc/emqx/emqx.conf", certfile, certfile_cmd)
replace_line("/etc/emqx/emqx.conf", cacertfile, cacertfile_cmd)
time.sleep(2)
os.system("sudo emqx_ctl users add \'user2\' \'pass2\'")
time.sleep(1)
os.system("sudo systemctl restart emqx")
time.sleep(1)
print("Done !!")
