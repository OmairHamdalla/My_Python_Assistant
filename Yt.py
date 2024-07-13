import os
import customtkinter as ctk
from pytube import YouTube

class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("600x500")

        self.link_label = ctk.CTkLabel(self, text="YouTube Link:")
        self.link_label.pack(pady=10)

        self.link_entry = ctk.CTkEntry(self, width=400)
        self.link_entry.pack(pady=10)

        self.show_streams_button = ctk.CTkButton(self, text="Show Available Streams", command=self.show_available_streams)
        self.show_streams_button.pack(pady=10)

        self.streams_label = ctk.CTkLabel(self, text="")
        self.streams_label.pack(pady=10)

        self.download_mp3_button = ctk.CTkButton(self, text="Download MP3", command=self.download_mp3)
        self.download_mp3_button.pack(pady=10)

        self.download_mp4_label = ctk.CTkLabel(self, text="Download MP4 in Quality:")
        self.download_mp4_label.pack(pady=10)

        self.quality_var = ctk.StringVar(value="360p")
        self.quality_options = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        self.quality_menu = ctk.CTkOptionMenu(self, variable=self.quality_var, values=self.quality_options)
        self.quality_menu.pack(pady=10)

        self.download_mp4_button = ctk.CTkButton(self, text="Download MP4", command=self.download_mp4)
        self.download_mp4_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=10)

    def show_available_streams(self):
        link = self.link_entry.get()
        try:
            yt = YouTube(link)
            streams = yt.streams.filter(file_extension='mp4')
            stream_list = []

            for stream in streams:
                if stream.resolution:
                    stream_list.append(f"{stream.resolution} {stream.mime_type} {stream.fps}fps")
                else:
                    stream_list.append(f"{stream.mime_type} (Audio)")

            stream_text = "\n".join(stream_list)
            self.streams_label.configure(text=f"Available Streams:\n{stream_text}")
        except Exception as e:
            self.streams_label.configure(text=f"Error: {str(e)}")

    def download_mp3(self):
        link = self.link_entry.get()
        SAVE_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

        try:
            yt = YouTube(link)
            audio_stream = yt.streams.filter(only_audio=True).first()
            out_file = audio_stream.download(output_path=SAVE_PATH)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

            self.status_label.configure(text="MP3 downloaded successfully!")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

    def download_mp4(self):
        link = self.link_entry.get()
        SAVE_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
        quality = self.quality_var.get()

        try:
            yt = YouTube(link)
            available_streams = yt.streams.filter(file_extension='mp4')
            available_qualities = [stream.resolution for stream in available_streams if stream.resolution]

            if quality in available_qualities:
                mp4_stream = yt.streams.filter(file_extension='mp4', res=quality).first()
                self.status_label.configure(text=f"Downloading MP4 {quality}...")
                self.progress_bar.set(0)

                def on_progress(stream, chunk, bytes_remaining):
                    total_size = stream.filesize
                    bytes_downloaded = total_size - bytes_remaining
                    percentage_of_completion = bytes_downloaded / total_size
                    self.progress_bar.set(percentage_of_completion)
                    self.update_idletasks()

                yt.register_on_progress_callback(on_progress)
                mp4_stream.download(output_path=SAVE_PATH)
                self.status_label.configure(text=f"MP4 {quality} downloaded successfully!")
            else:
                self.status_label.configure(text=f"Requested quality {quality} not available. Available qualities: {', '.join(available_qualities)}")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
