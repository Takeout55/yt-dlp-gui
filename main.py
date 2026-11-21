# File: main.py
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTextEdit, QPushButton, QCheckBox, QComboBox
from PySide6.QtCore import QFile, QIODevice
import subprocess
import os

global ffmpeg_path
global ytdlp_path
global hasSaved

hasSaved = False

def run():
    global ffmpeg_path
    global ytdlp_path
    global hasSaved

    if os.path.exists("lib/ytdlp_path.txt"):
        with open("lib/ytdlp_path.txt", 'r') as file:
            ytdlp_path = file.read()
    else:
        ytdlp_path = "./yt-dlp.exe"
    if os.path.exists("lib/ffmpeg_path.txt"):
        with open("lib/ffmpeg_path.txt", 'r') as file:
            ffmpeg_path = file.read()
    else:
        ffmpeg_path = "./ffmpeg/bin/ffmpeg.exe"

    if hasSaved == False:
        ytdlp_path = "./yt-dlp"
        ffmpeg = ""
        ffmpeg_path = ""
    elif hasSaved == True:
        if ytdlp_path == "":
            if ffmpeg_path == "":
                ffmpeg = ""
                print("ffmpeg path empty!")
            else:
                ffmpeg = f"--ffmpeg-location"
                print("ffmpeg path found!")
            ytdlp_path = "/home/takeout55/Music/yt-dlp"
            print("default yt-dlp path!")
        else:
            if ffmpeg_path == "":
                ffmpeg = ""
                print("ffmpeg path empty!")
            else:
                ffmpeg = f"--ffmpeg-location"
                print("ffmpeg path found!")
            ytdlp_path = ytdlp_path
            print("custom yt-dlp path!")


    playlist_checked = window.findChild(QCheckBox, "playlist_checkbox").isChecked()
    if playlist_checked == False:
        playlist_args = "--no-playlist"
    elif playlist_checked == True:
        playlist_args = ""

    title = window.findChild(QTextEdit,"title_entry").toPlainText()
    title_checked = window.findChild(QCheckBox, "title_checkbox").isChecked()
    print(title)
    if title_checked == True:
        title_args = f"{title}"
    elif title_checked == False:
        title_args = ""

    link = window.findChild(QTextEdit, "link_entry").toPlainText()
    file_format = window.findChild(QComboBox,"format_dropdown").currentText()

    print(f"{ytdlp_path}",f"--output",f"{link}",f"{playlist_args}",f"-t{file_format.lower()}")

    with subprocess.Popen(
            [f"{ytdlp_path}",f"--output",f"{title_args}",f"{link}",f"{playlist_args}",f"-t{file_format.lower()}",f"{ffmpeg}",f"{ffmpeg_path}"],
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
    ) as proc:
        for line in proc.stdout:
            print(line, end="")

    print("Download complete!")

def close():
    sys.exit(app.exec())

def info_close():
    info_window.close()

def title_enable():
    if window.findChild(QCheckBox, "title_checkbox").isChecked() == True:
        window.findChild(QTextEdit,"title_entry").setEnabled(True)
    elif window.findChild(QCheckBox, "title_checkbox").isChecked() == False:
        window.findChild(QTextEdit, "title_entry").setEnabled(False)

def save():
    global ffmpeg_path
    global ytdlp_path
    global hasSaved

    ffmpeg_path = info_window.findChild(QTextEdit, "ffmpeg_entry").toPlainText()
    ytdlp_path = info_window.findChild(QTextEdit, "ytdlp_entry").toPlainText()
    hasSaved = True

    with open("lib/ffmpeg_path.txt", 'w') as file:
        file.write(ffmpeg_path)

    with open("lib/ytdlp_path.txt", 'w') as file:
        file.write(ytdlp_path)

    info_close()

def info():
    global info_window
    global hasSaved
    global ffmpeg_path
    global ytdlp_path

    info_ui_file_name = "lib/info.ui"
    info_ui_file = QFile(info_ui_file_name)
    if not info_ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {info_ui_file_name}: {info_ui_file.errorString()}")
        sys.exit(-1)
    info_loader = QUiLoader()
    info_window = info_loader.load(info_ui_file)
    info_ui_file.close()

    if hasSaved == True:
        print(ytdlp_path,ffmpeg_path)
        info_window.findChild(QTextEdit,"ytdlp_entry").setPlainText(ytdlp_path)
        info_window.findChild(QTextEdit, "ffmpeg_entry").setPlainText(ffmpeg_path)
    if hasSaved == False:
        if os.path.exists("lib/ytdlp_path.txt"):
            with open("lib/ytdlp_path.txt", 'r') as file:
                ytdlp_path = file.read()
                info_window.findChild(QTextEdit, "ytdlp_entry").setPlainText(ytdlp_path)
        if os.path.exists("lib/ffmpeg_path.txt"):
            with open("lib/ffmpeg_path.txt", 'r') as file:
                ffmpeg_path = file.read()
                info_window.findChild(QTextEdit, "ffmpeg_entry").setPlainText(ffmpeg_path)


    info_window.show()

    info_window.findChild(QPushButton,"save_button").pressed.connect(save)
    info_window.findChild(QPushButton, "cancel_button").pressed.connect(info_close)

    info_window.mainloop()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "lib/main.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)

    window.findChild(QPushButton, "continue_button").pressed.connect(run)
    window.findChild(QPushButton, "close_button").pressed.connect(close)
    window.findChild(QPushButton, "info_button").pressed.connect(info)

    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()

    window.findChild(QCheckBox,"title_checkbox").stateChanged.connect(title_enable)

    sys.exit(app.exec())