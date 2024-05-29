import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Text

def copy_srt_to_prepreprocess(root, log_widget):
    filepath = filedialog.askopenfilename(
        title="SRTファイルを選択してください",
        filetypes=(("SRT files", "*.srt"), ("All files", "*.*"))
    )
    if not filepath:
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    prepreprocess_dir = os.path.join(script_dir, "..", "prepreprocess")
    os.makedirs(prepreprocess_dir, exist_ok=True)

    dest_path = os.path.join(prepreprocess_dir, os.path.basename(filepath))
    shutil.copy(filepath, dest_path)
    messagebox.showinfo("成功", "ファイルが正常にコピーされました。")
    log_widget.insert(tk.END, f"ファイル {os.path.basename(filepath)} をコピーしました。\n")
    root.after(1000, start_processing, root, log_widget)  # 処理を開始

def start_processing(root, log_widget):
    from main import start_processing
    log_widget.insert(tk.END, "処理を開始します...\n")
    start_processing(log_widget)

def run_gui():
    root = tk.Tk()
    root.title("SRTファイルコピーと処理")
    root.geometry("500x400")

    log_widget = Text(root, height=20, width=60)
    log_widget.pack(pady=20)

    copy_button = tk.Button(root, text="SRTファイルを選択", command=lambda: copy_srt_to_prepreprocess(root, log_widget))
    copy_button.pack(expand=True)

    root.mainloop()