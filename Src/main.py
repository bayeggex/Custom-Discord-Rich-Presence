import tkinter as tk
from tkinter import ttk
from pypresence import Presence
import requests
import json
import time

def save_to_json(client_id, details, state, large_image_id, small_image_id):
    data = {
        "client_id": client_id,
        "details": details,
        "state": state,
        "large_image_id": large_image_id,
        "small_image_id": small_image_id
    }
    with open("presence_details.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    status_label.config(text="Saved to presence_details.json")

def update_presence():
    client_id = client_id_entry.get()
    details = details_entry.get()
    state = state_entry.get()
    start = time.time()

    large_image_id = large_image_combobox.get()
    small_image_id = small_image_combobox.get()

    save_to_json(client_id, details, state, large_image_id, small_image_id)

    RPC = Presence(client_id)
    try:
        RPC.connect()
        RPC.update(
            details=details,
            state=state,
            start=start,
            large_image=large_image_id,
            small_image=small_image_id,
            large_text="Büyük resim metni", 
            small_text="Küçük resim metni"
        )
        status_label.config(text="Presence Güncellendi!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def fetch_image_ids(client_id):
    url = f"https://discord.com/api/oauth2/applications/{client_id}/assets"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        image_ids = [asset["id"] for asset in data if asset["type"] == 1]
        return image_ids
    else:
        return []

def fetch_image_ids(client_id):
    url = f"https://discord.com/api/oauth2/applications/{client_id}/assets"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        image_ids = [asset["id"] for asset in data if asset["type"] == 1]
        return image_ids
    else:
        return []

def update_combobox(client_id):
    image_ids = fetch_image_ids(client_id)
    large_image_combobox['values'] = image_ids
    small_image_combobox['values'] = image_ids

root = tk.Tk()
root.title("Discord Custom Rich Presence")

tk.Label(root, text="Client ID:").grid(row=0, column=0)
client_id_entry = tk.Entry(root)
client_id_entry.grid(row=0, column=1, columnspan=2)

tk.Label(root, text="Details:").grid(row=1, column=0)
details_entry = tk.Entry(root)
details_entry.grid(row=1, column=1, columnspan=2)

tk.Label(root, text="State:").grid(row=2, column=0)
state_entry = tk.Entry(root)
state_entry.grid(row=2, column=1, columnspan=2)

tk.Label(root, text="large_image_ ID:").grid(row=3, column=0)
large_image_combobox = ttk.Combobox(root)
large_image_combobox.grid(row=3, column=1, columnspan=2)

tk.Label(root, text="small_image_ ID:").grid(row=4, column=0)
small_image_combobox = ttk.Combobox(root)
small_image_combobox.grid(row=4, column=1, columnspan=2)

update_combobox_button = tk.Button(root, text="update ID's", command=lambda: update_combobox(client_id_entry.get()))
update_combobox_button.grid(row=5, columnspan=3)

update_button = tk.Button(root, text="Update Presence & Load Presence", command=update_presence)
update_button.grid(row=6, columnspan=3)

status_label = tk.Label(root, text="")
status_label.grid(row=7, columnspan=3)

root.mainloop()