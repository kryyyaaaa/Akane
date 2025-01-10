# -*- coding: utf-8 -*-

import os
import requests
import threading
import time
import ctypes
from tkinter import messagebox
import psutil
import shutil
from colorama import Fore, Style, init

cwd = os.getcwd()
akane_version = '1.0'
server_version = requests.get("https://github.com/kryyyaaaa/Akane/raw/refs/heads/main/AkaneVersion").text.splitlines()[0]

if server_version != akane_version:
    print(f"Update Akane! {akane_version} -> {server_version}\n\nhttps://github.com/kryyyaaaa/Akane")
    input()
    exit(1)

# -------+ API Code :
class Forlorn:
    ForlornVersion = "1.1.5"
    isInjected = False
    autoinject = False
    isUpdating = False


    def __init__(self):
        self.is_updating = False
        self.is_injected = False

    def start_client(self):
        try:
            lib = ctypes.CDLL(os.path.join(cwd, 'ForlornInject.dll'))  # Use full path
            lib.StartClient.argtypes = []
            lib.StartClient.restype = None
            lib.StartClient()
        except OSError as e:
            print(Fore.RED + f"[ERR] Failed to load ForlornInject.dll: {e}")

    def execute_sc(self, script_source):
        try:
            if isinstance(script_source, str):
                script_source = script_source.encode('utf-8', errors='replace')
            lib = ctypes.CDLL(os.path.join(cwd, 'ForlornInject.dll'))  # Use full path
            lib.ExecuteSC.argtypes = [ctypes.c_char_p]
            lib.ExecuteSC.restype = None
            lib.ExecuteSC(script_source)
        except OSError as e:
            print(Fore.RED + f"[ERR] Failed to load ForlornInject.dll: {e}")
        except Exception as e:
            print(Fore.RED + f"[ERR] Got an error: {e}")

    def inject_forlorn(self):
        if self.is_updating:
            return
        self.is_latest_version()
        if not os.path.exists(os.path.join(cwd, "ForlornInject.dll")):
            self.download_file("https://github.com/ForlornWindow46/ForlornApi/releases/download/api/ForlornInject.dll", "ForlornInject.dll")
        if self.is_updating or not self.is_roblox_open():
            return
        self.clean_up_old_files()
        try:
            self.start_client()
            self.is_injected = True
            print(Fore.LIGHTBLUE_EX + "[INF] Forlorn injected successfully!")
            messagebox.showinfo("Success", "Forlorn injected successfully!")
        except Exception as e:
            print(Fore.RED + f"[ERR] Failed to attach ForlornApi: {e}")
            self.is_injected = False

    def execute_script(self, script):
        if not self.is_injected:  # Use self.is_injected directly
            messagebox.showwarning("Warning", "Forlorn is not injected.")
            print(Fore.YELLOW + "[WARN] Forlorn is not injected.")
            return
        if not self.is_roblox_open():  # Use self.is_roblox_open directly
            messagebox.showwarning("Warning", "Roblox is not open.")
            print(Fore.YELLOW + "[WARN] Roblox is not open.")
            return
        try:
            print(Fore.LIGHTBLUE_EX + f"[INF] Executing script: {script}")
            self.execute_sc(script)  # Call self.execute_sc directly
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(Fore.RED + f"[ERR] An error occurred: {e}")

    def is_latest_version(self):
        self.is_updating = True
        request_uri = "https://raw.githubusercontent.com/ForlornWindow46/ForlornApi/refs/heads/main/ForlornApiVersion"
        forlorn_inject_url = "https://github.com/ForlornWindow46/ForlornApi/releases/download/api/ForlornInject.dll"
        try:
            response = requests.get(request_uri)
            if response.status_code == 200:
                version = response.text.strip()
                if version != self.ForlornVersion:
                    self.replace_file(os.path.join(cwd, "ForlornInject.dll"), ".old")
                    self.download_file(forlorn_inject_url, os.path.join(cwd, "ForlornInject.dll"))
                    messagebox.showinfo("Update", "API updated. Please reopen your executor.")
                    time.sleep(1)
                    os._exit(0)
        except requests.exceptions.RequestException as e:
            messagebox.showwarning("Error", "Failed connect to the server.")
            print(Fore.YELLOW + f"[WARN] Error checking latest version: {e}") 
        finally:
            self.is_updating = False

    def download_file(self, url, file_path):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[ERR] Error downloading file: {e}")

    def clean_up_old_files(self):
        if os.path.exists(os.path.join(cwd, "ForlornApi.old")):
            os.remove(os.path.join(cwd, "ForlornApi.old"))
        if os.path.exists(os.path.join(cwd, "ForlornInject.old")):
            os.remove(os.path.join(cwd, "ForlornInject.old"))

    def is_roblox_open(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'RobloxPlayerBeta.exe':
                return True
        return False

    def replace_file(self, file_path, backup_extension):
        backup_path = os.path.splitext(file_path)[0] + backup_extension
        if os.path.exists(backup_path):
            os.remove(backup_path)
        if not os.path.exists(file_path):
            return
        shutil.move(file_path, backup_path)

# --

forlorn = Forlorn()

def inject_forlorn():
    threading.Thread(target=forlorn.inject_forlorn).start()

def execute_script(script):
    threading.Thread(target=forlorn.execute_script, args=(script,)).start()

import webview

window = webview.create_window('Akane', r'bin/menu.html', width=520, height=350, frameless=True, on_top=True)

window.expose(execute_script, inject_forlorn)
webview.start()