import subprocess
import time
import requests

print("Starting catalyst serve...")
proc = subprocess.Popen(["catalyst", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
print("Waiting 20 seconds for server to boot...")
time.sleep(20)

print("Triggering migration endpoint...")
try:
    res = requests.get("http://localhost:3000/server/setu_api/api/migrate")
    print("Response Status:", res.status_code)
    try:
        print("Response JSON:", res.json())
    except:
        print("Response Text:", res.text)
except Exception as e:
    print("Error hitting endpoint:", e)
    
print("Terminating catalyst serve...")
proc.terminate()
