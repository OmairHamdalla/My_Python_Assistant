import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.video = None

    def fetch_video(self):
        try:
            self.video = YouTube(self.url)
        except Exception as e:
            print(f"Error fetching video: {e}")
            return None
        return self.video

    def get_streams(self):
        if not self.video:
            return []
        streams = self.video.streams.filter(progressive=True).all()
        return streams

    def download(self, stream, download_path):
        try:
            stream.download(output_path=download_path)
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False

class YouTubeDownloaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x400")

        self.url_label = ttk.Label(root, text="YouTube URL:")
        self.url_label.pack(pady=10)

        self.url_entry = ttk.Entry(root, width=70)
        self.url_entry.pack(pady=10)

        self.fetch_button = ttk.Button(root, text="Fetch Video", command=self.fetch_video)
        self.fetch_button.pack(pady=10)

        self.streams_listbox = tk.Listbox(root, width=70, height=10)
        self.streams_listbox.pack(pady=10)

        self.download_button = ttk.Button(root, text="Download", command=self.download_video)
        self.download_button.pack(pady=10)

        self.downloader = None

    def fetch_video(self):
        url = self.url_entry.get()
        self.downloader = YouTubeDownloader(url)
        video = self.downloader.fetch_video()
        if video:
            self.update_streams_listbox()
        else:
            messagebox.showerror("Error", "Failed to fetch video")

    def update_streams_listbox(self):
        streams = self.downloader.get_streams()
        print(streams)
        self.streams_listbox.delete(0, tk.END)
        for stream in streams:
            self.streams_listbox.insert(tk.END, f"{stream.mime_type} {stream.resolution}")

    def download_video(self):
        selected_index = self.streams_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a stream")
            return

        stream = self.downloader.get_streams()[selected_index[0]]
        download_path = os.path.join(os.path.expanduser("~"), "Desktop")
        success = self.downloader.download(stream, download_path)
        if success:
            messagebox.showinfo("Success", "Video downloaded successfully")
        else:
            messagebox.showerror("Error", "Failed to download video")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderUI(root)
    root.mainloop()
