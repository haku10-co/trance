# main.py
import tkinter as tk
import threading
from edit import process_srt_files
from file_utils import process_text_files
from gui import run_gui

def update_progress(progress, log_widget):
    def update_gui():
        log_widget.insert(tk.END, f'Progress: {progress:.2f}%\n')
        log_widget.see(tk.END)  # スクロールして最新のログが見えるようにする

    log_widget.after(0, update_gui)  # メインスレッドで GUI を更新

def start_processing(log_widget):
    def processing_thread():
        process_srt_files()
        output_file_paths = process_text_files(lambda progress: update_progress(progress, log_widget))
        log_widget.insert(tk.END, "処理が完了しました。\n出力ファイルパス:\n")
        for path in output_file_paths:
            log_widget.insert(tk.END, f"{path}\n")

    thread = threading.Thread(target=processing_thread)
    thread.start()

if __name__ == "__main__":
    run_gui()