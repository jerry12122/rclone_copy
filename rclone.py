#!/usr/bin/python3
import sys
import os 
import subprocess

id = ""
shell = ""
arg1s = ["-h","copy","mount"]

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

def print_help():
    print("mount:")
    print("    python3 rclone.py mount gdrive_name mount_destination")
    print("    EX:")
    print("        python3 rclone.py mount t10 /mnt/t10")
    print("copy:")
    print("    python3 rclone.py copy url gdrive_name mount_destination")
    print("    EX:")
    print("        python3 rclone.py copy https://drive.google.com/drive/folders/1XXXX t10 /mnt/t10/test")

try:
    arg1=sys.argv[1]
    if (not (arg1 in arg1s)) or  arg1 == "-h":
        print_help()
    try:
        if arg1 == "mount":
            gdrive_name = sys.argv[2]
            mount_destination = sys.argv[3]
            shell = "rclone mount \
                --allow-other \
                --cache-tmp-upload-path=/tmp/rclone/upload \
                --cache-chunk-path=/tmp/rclone/chunks \
                --cache-workers=8 \
                --cache-writes \
                --cache-dir=/tmp/rclone/vfs \
                --cache-db-path=/tmp/rclone/db \
                --no-modtime \
                --drive-use-trash \
                --stats=0 \
                --checkers=16 \
                --bwlimit=40M \
                --dir-cache-time=60m \
                --vfs-cache-mode writes \
                --cache-info-age=60m "+gdrive_name+": "+mount_destination+" &"
            #print(shell)
            print(system_call(shell))
    except:
        print("Syntax error!!!!!!")
        print("python3 rclone.py mount gdrive_name mount_destination")
    try:
        if arg1 == "copy":
            url = sys.argv[2]
            gdrive_name = sys.argv[3]
            mount_destination = sys.argv[4]
            url_split=url.split('/')
        
            if mount_destination[-1] != "/":
                mount_destination += "/"
        
            if gdrive_name[-1] == ":":
                gdrive_name=gdrive_name[0:-1]
        
            for i in url_split:
                if len(i) > 10 and i[0] == '1' :
                    id=i.split('?')[0]
        
            if "folders" in url_split:
                shell = "rclone copy "+gdrive_name+": --drive-root-folder-id "+id+" "+mount_destination+" -v"
            if "file" in url_split:
                shell = "rclone backend copyid "+gdrive_name+": "+id+" "+mount_destination+" -v"
            #print(shell)
            print(system_call(shell))
    except:
        print("Syntax error!!!!!!")
        print("python3 rclone.py copy url gdrive_name mount_destination")
except:
    print_help()