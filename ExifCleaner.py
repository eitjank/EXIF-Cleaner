import os
import json
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path

exiftool_path = None
stop_flag = False

APP_DIR = Path(os.getenv("APPDATA")) / "ExifCleaner"
CONFIG_FILE = APP_DIR / "config.json"

# ensure folder exists
APP_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# CONFIG FILE HANDLING
# -------------------------------------------------------
def load_config():
    global exiftool_path
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                cfg = json.load(f)
                exiftool_path = cfg.get("exiftool_path")
        except:
            pass


def save_config():
    global exiftool_path
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"exiftool_path": exiftool_path}, f, indent=2)
    except Exception as e:
        messagebox.showerror("Config Error", f"Could not save config:\n{e}")


# -------------------------------------------------------
# CLEANING FUNCTION (runs in thread)
# -------------------------------------------------------
def clean_exif(folder, ui):
    global stop_flag, exiftool_path

    stop_flag = False

    if not exiftool_path:
        ui.log("❌ ExifTool path not selected!")
        ui.set_idle()
        return

    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    total = len(files)

    if total == 0:
        messagebox.showinfo("No Images", "No JPG/PNG files found.")
        ui.set_idle()
        return

    ui.progress["maximum"] = total

    for i, filename in enumerate(files):
        if stop_flag:
            ui.log("⛔ Cancelled.")
            break

        path = os.path.join(folder, filename)
        ui.log(f"[{i+1}/{total}] Cleaning {path}")

        # -------------------------
        # Build exiftool args
        # -------------------------
        args = [exiftool_path]

        # Backup toggle
        if ui.backup_var.get():
            args += ["-overwrite_original_in_place"]
        else:
            args += ["-overwrite_original"]

        # If ALL EXIF is selected → override others, but keep backup choice
        if ui.all_var.get():
            args += ["-all="]
        else:
            if ui.serial_var.get():
                args += ["-SerialNumber=", "-InternalSerialNumber=", "-BodySerialNumber="]

            if ui.model_var.get():
                args += ["-Model=", "-LensModel="]

            if ui.gps_var.get():
                args += ["-GPS:all="]

            if ui.date_var.get():
                args += ["-DateTimeOriginal=", "-CreateDate=", "-ModifyDate="]

            if ui.software_var.get():
                args += ["-Software="]

        args.append(path)

        subprocess.run(args, capture_output=True, text=True)

        ui.progress["value"] = i + 1

    ui.set_idle()
    ui.log("✔ Done.")


# -------------------------------------------------------
# GUI
# -------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("EXIF Cleaner")

        tk.Button(root, text="Select exiftool.exe", command=self.select_exiftool).pack(pady=5)

        self.exiftool_label = tk.Label(root, text="", fg="green")
        self.exiftool_label.pack()
        self.update_exiftool_label()

        tk.Button(root, text="Select Folder", command=self.select_folder).pack(pady=5)

        self.serial_var = tk.BooleanVar(value=True)
        self.model_var = tk.BooleanVar()
        self.gps_var = tk.BooleanVar()
        self.date_var = tk.BooleanVar()
        self.software_var = tk.BooleanVar()
        self.all_var = tk.BooleanVar()
        self.backup_var = tk.BooleanVar()

        self.checks = [
            tk.Checkbutton(root, text="Remove Serial Numbers", variable=self.serial_var),
            tk.Checkbutton(root, text="Remove Camera Model", variable=self.model_var),
            tk.Checkbutton(root, text="Remove GPS", variable=self.gps_var),
            tk.Checkbutton(root, text="Remove Date/Time", variable=self.date_var),
            tk.Checkbutton(root, text="Remove Software Tag", variable=self.software_var),
            tk.Checkbutton(root, text="Remove ALL EXIF", variable=self.all_var),
            tk.Checkbutton(root, text="Create Backup of Originals", variable=self.backup_var),
        ]

        for c in self.checks:
            c.pack(anchor="w")

        self.progress = ttk.Progressbar(root, length=300)
        self.progress.pack(pady=10)

        self.cancel_btn = tk.Button(root, text="Cancel", command=self.cancel, state="disabled")
        self.cancel_btn.pack()

        self.log_box = tk.Text(root, height=10, width=60)
        self.log_box.pack(pady=10)

    # -------------------------
    def update_exiftool_label(self):
        if exiftool_path:
            self.exiftool_label.config(text=f"ExifTool: {exiftool_path}", fg="green")
        else:
            self.exiftool_label.config(text="ExifTool: NOT SELECTED", fg="red")

    def cancel(self):
        global stop_flag
        stop_flag = True
        self.log("⛔ Cancelling...")

    def select_exiftool(self):
        global exiftool_path
        path = filedialog.askopenfilename(
            title="Select exiftool.exe",
            filetypes=[("Executable", "*.exe")]
        )
        if path:
            exiftool_path = path
            save_config()
            self.update_exiftool_label()
            self.log(f"Selected exiftool: {path}")

    def select_folder(self):
        if not exiftool_path:
            messagebox.showerror("Missing ExifTool", "Please select exiftool.exe first.")
            return

        folder = filedialog.askdirectory()
        if not folder:
            return

        self.log(f"Folder: {folder}")
        self.set_running()

        thread = threading.Thread(target=clean_exif, args=(folder, self), daemon=True)
        thread.start()

    def set_running(self):
        for c in self.checks:
            c.config(state="disabled")
        self.cancel_btn.config(state="normal")

    def set_idle(self):
        for c in self.checks:
            c.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        print(text)


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
load_config()

root = tk.Tk()
app = App(root)
root.mainloop()
