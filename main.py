import cv2
import os
import sys
import glob
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class FrameExtractorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Frame Ripper")

        # Variables
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()

        # Choose Source Folder button
        self.btn_source = tk.Button(root, text="Choose Source Folder", command=self.choose_source)
        self.btn_source.pack(pady=20)

        # Display Source Folder
        self.lbl_source = tk.Label(root, textvariable=self.source_folder)
        self.lbl_source.pack(pady=10)

        # Choose Destination Folder button
        self.btn_destination = tk.Button(root, text="Choose Destination Folder", command=self.choose_destination)
        self.btn_destination.pack(pady=20)

        # Display Destination Folder
        self.lbl_destination = tk.Label(root, textvariable=self.destination_folder)
        self.lbl_destination.pack(pady=10)

        # Start Extraction button
        self.btn_extract = tk.Button(root, text="Start Ripping", command=self.start_extraction)
        self.btn_extract.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        # Progress message
        self.progress_message = tk.StringVar(value="Please select folders and start extraction.")
        self.lbl_message = tk.Label(root, textvariable=self.progress_message)
        self.lbl_message.pack(pady=20)

    def choose_source(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_folder.set(folder_selected)

    def choose_destination(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination_folder.set(folder_selected)

    def start_extraction(self):
        source = self.source_folder.get()
        destination = self.destination_folder.get()

        if not source or not destination:
            self.progress_message.set("Both source and destination folders need to be selected.")
            return

        mp4_files = glob.glob(os.path.join(source, "*.mp4"))
        total_videos = len(mp4_files)

        if not mp4_files:
            self.progress_message.set(f"No .mp4 files found in {source}.")
            return

        self.progress_message.set(f"Found {total_videos} video(s). Starting frame ripping...")
        self.progress["maximum"] = total_videos
        self.progress["value"] = 0

        for video_file in mp4_files:
            video_name = os.path.basename(video_file).split('.')[0]
            output_folder = os.path.join(destination, video_name)
            self.extract_frames_from_video(video_file, output_folder)
            self.progress["value"] += 1

        self.progress_message.set("Frame ripping complete!")

    def extract_frames_from_video(self, video_path, output_folder):
        # Make sure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        cap = cv2.VideoCapture(video_path)

        # Check if camera opened successfully
        if not cap.isOpened():
            self.progress_message.set(f"Error opening video file {video_path}")
            return

        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            output_frame_path = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
            cv2.imwrite(output_frame_path, frame)
            frame_number += 1

        cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = FrameExtractorApp(root)
    root.mainloop()
