import os
import threading
import tkinter as tk
from tkinter import ttk, CENTER, DISABLED, NORMAL, RAISED, END
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from File import *
import glob
import asyncio


height = 150
width = 1000

root = tk.Tk()
root.geometry(str(width) + "x" + str(height))
root.resizable(False, False)
root.title('Client')

root.columnconfigure(2, weight=1)
root.rowconfigure(3, weight=1)


# --------------------------------------------Uploaded File Tree--------------------------------------------------------
uploaded_file_tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=5)

uploaded_file_tree.column("# 1", anchor=CENTER, width=340)
uploaded_file_tree.heading("# 1", text="File Name")
uploaded_file_tree.column("# 2", anchor=CENTER, width=40)
uploaded_file_tree.heading("# 2", text="Parts")
uploaded_file_tree.column("# 3", anchor=CENTER, width=80)
uploaded_file_tree.heading("# 3", text="Redundancy")
uploaded_file_tree.column("# 4", anchor=CENTER, width=100)
uploaded_file_tree.heading("# 4", text="Online | Offline")
uploaded_file_tree.column("# 5", anchor=CENTER, width=80)
uploaded_file_tree.heading("# 5", text="Retrievable")

# TODO load in uploaded files
#print(glob.glob(".\\Uploads\\*"))
def update_uploaded_files():
    thr = threading.Thread(target=update_uploaded_files_async, args=(), kwargs={})
    thr.start()



def update_uploaded_files_async():
    for item in uploaded_file_tree.get_children():
        uploaded_file_tree.delete(item)

    print("test")
    for file in glob.glob(".\\Uploads\\*.uploaded"):
        file_name = file
        with open(file_name, "r") as input_file:
            input = input_file.readlines()
            json_in = json.loads(input.pop())

            offline = 0
            online = 0
            retrievable = [False, False]
            for ip_row in json_in['redundant_hosts']:
                for index, ip in enumerate(ip_row):
                    try:
                        response = requests.get(url=ip + "/online", timeout=.5)
                        retrievable[index] = True
                        online += 1
                    except requests.exceptions.ConnectionError:
                        print("offline")
                        offline += 1

            for index, ip in enumerate(json_in['hosts']):
                try:
                    response = requests.get(url=ip + "/online", timeout=.5)
                    retrievable[index] = True
                    online += 1
                except requests.exceptions.ConnectionError:
                    print("offline")
                    offline += 1


            print(retrievable)
            ret = True
            for val in retrievable:
                if not val:
                    ret = False
                    break


            uploaded_file_tree.insert('', 'end', text="6",
                                  values=(file, len(json_in['part_ids']), len(json_in['redundant_hosts']), str(online) + " | " + str(offline), str(ret)))

update_uploaded_files()


def select_item(a):
    current_item = uploaded_file_tree.focus()
    print(uploaded_file_tree.item(current_item))


uploaded_file_tree.bind('<ButtonRelease-1>', select_item)
uploaded_file_tree.grid(row=0, column=0, rowspan=3)

# --------------------------------------------Upload File Button--------------------------------------------------------
def upload_file(masternode_ip):
    file_path = fd.askopenfilename()
    print(file_path)

    thr = threading.Thread(target=upload_async, args=(masternode_ip, file_path), kwargs={})
    thr.start()

def upload_async(masternode_ip, file_path):
    keys = []
    print(file_path)

    file = File(file_path, keys, 2, 2)
    uploaded_file = file.upload(masternode_ip)

    uploaded_file.serialize("./Uploads/")
    update_uploaded_files()


upload_btn = tk.Button(root, text="Upload", command=lambda: upload_file(masternode_ip.get()), width=30, height=2)
upload_btn.grid(row=1, column=1, columnspan=2)





# --------------------------------------------Download File Button------------------------------------------------------
def download_file(item):
    path = item.get('values')[0]
    print(path)
    thr = threading.Thread(target=download_file_async, args=(str(path),), kwargs={})
    thr.start()

def download_file_async(path):
    print("Download", path)

    uploaded_file = UploadedFile.load(path)

    downloaded_file = uploaded_file.download()
    if downloaded_file:
        print("File Downloaded")
    else:
        print(":(")
        return
    downloaded_file.get_file(path.replace(".uploaded", ""))



download_file_btn = tk.Button(root, text="Download Selected",
                              command=lambda: download_file(uploaded_file_tree.item(uploaded_file_tree.focus())), width=18, height=3)
download_file_btn.grid(row=2, column=1, rowspan=2)


# ---------------------------------------------Delete File Button-------------------------------------------------------
def delete_file(item):
    path = item.get('values')[0]
    os.remove(path)
    update_uploaded_files()
    # TODO Delete from nodes
    pass


download_file_btn = tk.Button(root, text="Delete Selected",
                              command=lambda: delete_file(uploaded_file_tree.item(uploaded_file_tree.focus())), width=18, height=3)
download_file_btn.grid(row=2, column=2, rowspan=2)


# --------------------------------------------Master Node Entry------------------------------------------------------
masternode_ip = tk.StringVar()
masternode_ip_entry = tk.Entry(root, textvariable=masternode_ip, font=('calibre', 10, 'normal'), width=18)


masternode_ip_entry.grid(row=0, column=2, columnspan=1)

label = tk.Label(root, text="Master Node Ip and Port", width=18)
label.grid(row=0,column=1, sticky="", columnspan=1)


# --------------------------------------------Refresh Button------------------------------------------------------
download_file_btn = tk.Button(root, text="Refresh",
                              command=lambda: update_uploaded_files(), width=90)
download_file_btn.grid(row=3, column=0)

root.mainloop()
