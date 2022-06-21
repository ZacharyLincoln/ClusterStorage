import tkinter as tk
from tkinter import ttk, CENTER, DISABLED, NORMAL, RAISED
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from File import *

height = 125
width = 1100

root = tk.Tk()
root.geometry(str(width) + "x" + str(height))
root.resizable(False, False)
root.title('Client')

root.columnconfigure(2, weight=1)
root.rowconfigure(3, weight=1)


# --------------------------------------------Uploaded File Tree--------------------------------------------------------
uploaded_file_tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', height=5)

uploaded_file_tree.column("# 1", anchor=CENTER)
uploaded_file_tree.heading("# 1", text="File Name")
uploaded_file_tree.column("# 2", anchor=CENTER)
uploaded_file_tree.heading("# 2", text="Parts")
uploaded_file_tree.column("# 3", anchor=CENTER)
uploaded_file_tree.heading("# 3", text="Redundancy")
uploaded_file_tree.column("# 4", anchor=CENTER)
uploaded_file_tree.heading("# 4", text="Online | Offline nodes")

# TODO load in uploaded files


uploaded_file_tree.insert('', 'end', text="5", values=("C:\\Users\\Zach\\Desktop\\Center.stl", 'Stephan', 'Heyward', "5"))


def select_item(a):
    current_item = uploaded_file_tree.focus()
    print(uploaded_file_tree.item(current_item))


uploaded_file_tree.bind('<ButtonRelease-1>', select_item)
uploaded_file_tree.grid(row=0, column=0, rowspan=4)

# --------------------------------------------Upload File Button--------------------------------------------------------
def upload_file(file_path, masternode_ip):
    print(file_path)

    keys = []

    file = File(file_path, keys, 2, 2)
    uploaded_file = file.upload(masternode_ip)

    uploaded_file.serialize("./Uploads/")


upload_btn = tk.Button(root, text="Upload", command=lambda: upload_file(upload_file_path.get(), masternode_ip.get()))
upload_btn.grid(row=2, column=2)




# ---------------------------------------------Upload File Entry--------------------------------------------------------
def upload_input_clicked(element):
    filename = fd.askopenfilename()
    print(filename)
    element.config(state=NORMAL)
    element.insert(0, str(filename))
    element.config(state=DISABLED)


upload_file_path = tk.StringVar()
upload_file_path_entry = tk.Entry(root, textvariable=upload_file_path, font=('calibre', 10, 'normal'), state=DISABLED)
upload_file_path_entry.bind('<Button-1>', lambda a: upload_input_clicked(upload_file_path_entry))

upload_file_path_entry.grid(row=2, column=1)


# --------------------------------------------Download File Button------------------------------------------------------
def download_file(item):
    path = item.get('values')[0]

    uploaded_file = UploadedFile.load(path)

    downloaded_file = uploaded_file.download()
    downloaded_file.get_file(path.replace(".uploaded", ""))


download_file_btn = tk.Button(root, text="Download Selected",
                              command=lambda: download_file(uploaded_file_tree.item(uploaded_file_tree.focus())))
download_file_btn.grid(row=3, column=1)


# ---------------------------------------------Delete File Button-------------------------------------------------------
def delete_file(item):
    path = item.get('values')[0]
    # TODO Delete from nodes
    pass


download_file_btn = tk.Button(root, text="Delete Selected",
                              command=lambda: download_file(uploaded_file_tree.item(uploaded_file_tree.focus())))
download_file_btn.grid(row=3, column=2)


# --------------------------------------------Master Node Entry------------------------------------------------------
masternode_ip = tk.StringVar()
masternode_ip_entry = tk.Entry(root, textvariable=masternode_ip, font=('calibre', 10, 'normal'))


masternode_ip_entry.grid(row=1, column=1, columnspan=2)


label = tk.Label(root, text="Master Node Ip", )
label.grid(row=0,column=1, columnspan=2, sticky="")

root.mainloop()
