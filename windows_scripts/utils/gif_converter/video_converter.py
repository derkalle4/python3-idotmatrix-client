import os
import sys
import subprocess
import tempfile
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QFileDialog, QComboBox, QSlider, QSpinBox,
                            QCheckBox, QMessageBox, QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QRect, QPoint
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
import shutil
import cv2
from PIL import Image, ImageSequence
import numpy as np
import time
import threading

class VideoPreviewWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black; color: white;")
        self.setText("Preview Video")
        self.video_path = None
        self.cap = None
        self.current_frame_idx = 0
        self.total_frames = 0
        self.fps = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_playing = False
        self.start_frame = 0
        self.end_frame = 0
        
    def load_video(self, video_path):
        self.video_path = video_path
        if self.cap:
            self.cap.release()
        
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            QMessageBox.critical(None, "Error", "Could not open video file")
            return False
            
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.current_frame_idx = 0
        self.end_frame = self.total_frames - 1
        self.update_frame()
        return True
        
    def update_frame(self):
        if not self.cap:
            return
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_idx)
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize to fit widget size
            h, w, c = frame.shape
            aspect_ratio = w / h
            if w > h:
                new_w = 200
                new_h = int(200 / aspect_ratio)
            else:
                new_h = 200
                new_w = int(200 * aspect_ratio)
                
            frame = cv2.resize(frame, (new_w, new_h))
            
            # Create QImage and QPixmap
            qimg = QImage(frame.data, new_w, new_h, new_w * c, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Center image in widget
            self.setPixmap(pixmap)
            
            # Increment frame index if playing
            if self.is_playing:
                self.current_frame_idx += 1
                if self.current_frame_idx >= self.total_frames:
                    self.current_frame_idx = 0
        else:
            self.current_frame_idx = 0
            
    def play_pause(self):
        if not self.cap:
            return
            
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False
        else:
            self.timer.start(int(1000 / self.fps))
            self.is_playing = True
            
    def jump_backward(self, seconds=2):
        if not self.cap:
            return
        frames_to_jump = int(self.fps * seconds)
        self.current_frame_idx = max(0, self.current_frame_idx - frames_to_jump)
        self.update_frame()
        
    def jump_forward(self, seconds=2):
        if not self.cap:
            return
        frames_to_jump = int(self.fps * seconds)
        self.current_frame_idx = min(self.total_frames - 1, self.current_frame_idx + frames_to_jump)
        self.update_frame()
            
    def set_start(self):
        if not self.cap:
            return
        self.start_frame = self.current_frame_idx
        
    def set_end(self):
        if not self.cap:
            return
        self.end_frame = self.current_frame_idx
        
    def get_frame(self):
        if not self.cap:
            return None
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_idx)
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None
        
    def get_duration_seconds(self):
        if not self.cap or self.fps == 0:
            return 0
        return (self.end_frame - self.start_frame) / self.fps
        
    def get_start_time(self):
        if not self.cap or self.fps == 0:
            return 0
        return self.start_frame / self.fps
        
    def get_time_str(self, frame_idx):
        if not self.cap or self.fps == 0:
            return "00:00.000"
        seconds = frame_idx / self.fps
        minutes = int(seconds / 60)
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:06.3f}"
        
    def cleanup(self):
        if self.cap:
            self.cap.release()

class GifPreviewWidget(QLabel):
    selection_changed = pyqtSignal(tuple)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black; color: white;")
        self.setText("Preview GIF")
        self.frames = []
        self.current_frame_idx = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.selection_rect = None
        self.selection_start = None
        self.selection_active = False
        self.force_square = True
        self.original_image_size = (0, 0)
        self.image_offset = (0, 0)
        self.pixmap_size = (0, 0)
        
    def set_frames(self, frames, fps=10):
        self.frames = frames
        self.current_frame_idx = 0
        if frames:
            # Store original image size for accurate selection
            self.original_image_size = (frames[0].shape[1], frames[0].shape[0])
            self.update_frame()
            self.timer.start(int(1000 / fps))
        
    def update_frame(self):
        if not self.frames:
            return
            
        frame = self.frames[self.current_frame_idx]
        h, w, c = frame.shape
        
        # Resize to fit widget size
        aspect_ratio = w / h
        if w > h:
            new_w = 200
            new_h = int(200 / aspect_ratio)
        else:
            new_h = 200
            new_w = int(200 * aspect_ratio)
            
        frame = cv2.resize(frame, (new_w, new_h))
        
        # Calculate image offset for centering
        self.image_offset = ((200 - new_w) // 2, (200 - new_h) // 2)
        self.pixmap_size = (new_w, new_h)
        
        # Create QImage and QPixmap
        qimg = QImage(frame.data, new_w, new_h, new_w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        
        # Draw selection rectangle if active
        if self.selection_rect:
            painter = QPainter(pixmap)
            pen = QPen(QColor(255, 255, 255))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)
            painter.end()
        
        # Center image in widget
        self.setPixmap(pixmap)
        
        # Increment frame index
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
        
    def mousePressEvent(self, event):
        if not self.frames:
            return
            
        # Calculate coordinates relative to the image
        pixmap = self.pixmap()
        if not pixmap:
            return
            
        # Get image position within widget
        offset_x, offset_y = self.image_offset
        
        # Check if click is within the image
        if (event.x() < offset_x or event.x() >= offset_x + pixmap.width() or
            event.y() < offset_y or event.y() >= offset_y + pixmap.height()):
            return
            
        # Store start position relative to image
        self.selection_start = QPoint(event.x() - offset_x, event.y() - offset_y)
        self.selection_active = True
        self.selection_rect = QRect(self.selection_start.x(), self.selection_start.y(), 1, 1)
        self.update_frame()
        
    def mouseMoveEvent(self, event):
        if not self.selection_active or not self.frames:
            return
            
        # Calculate coordinates relative to the image
        pixmap = self.pixmap()
        if not pixmap:
            return
            
        # Get image position within widget
        offset_x, offset_y = self.image_offset
        
        # Calculate current position relative to image
        x = max(0, min(event.x() - offset_x, pixmap.width() - 1))
        y = max(0, min(event.y() - offset_y, pixmap.height() - 1))
        
        # Calculate width and height
        width = abs(x - self.selection_start.x())
        height = abs(y - self.selection_start.y())
        
        # Force square if needed
        if self.force_square:
            size = max(width, height)
            width = size
            height = size
            
        # Calculate top-left corner
        if x < self.selection_start.x():
            x1 = x
        else:
            x1 = self.selection_start.x()
            
        if y < self.selection_start.y():
            y1 = y
        else:
            y1 = self.selection_start.y()
            
        # Adjust for square
        if self.force_square:
            if self.selection_start.x() < x:
                x2 = x1 + width
            else:
                x2 = x1
                x1 = x2 - width
                
            if self.selection_start.y() < y:
                y2 = y1 + height
            else:
                y2 = y1
                y1 = y2 - height
        else:
            x2 = x1 + width
            y2 = y1 + height
            
        # Ensure rectangle stays within image bounds
        x1 = max(0, min(x1, pixmap.width() - 1))
        y1 = max(0, min(y1, pixmap.height() - 1))
        x2 = max(0, min(x2, pixmap.width() - 1))
        y2 = max(0, min(y2, pixmap.height() - 1))
        
        # Update selection rectangle
        self.selection_rect = QRect(int(x1), int(y1), int(x2 - x1), int(y2 - y1))
        
        # Update display
        self.update_frame()
        
    def mouseReleaseEvent(self, event):
        if self.selection_active and self.selection_rect:
            self.selection_active = False
            # Emit signal with selection coordinates
            crop_rect = self.get_selection_rect()
            if crop_rect:
                self.selection_changed.emit(crop_rect)
        
    def get_selection_rect(self):
        if not self.selection_rect or not self.frames:
            return None
            
        # Convert widget coordinates to original image coordinates
        pixmap = self.pixmap()
        if not pixmap:
            return None
            
        # Calculate scale factors
        scale_x = self.original_image_size[0] / self.pixmap_size[0]
        scale_y = self.original_image_size[1] / self.pixmap_size[1]
        
        # Convert selection rectangle to original image coordinates
        x1 = int(self.selection_rect.left() * scale_x)
        y1 = int(self.selection_rect.top() * scale_y)
        x2 = int(self.selection_rect.right() * scale_x)
        y2 = int(self.selection_rect.bottom() * scale_y)
        
        # Ensure coordinates are within bounds
        x1 = max(0, min(x1, self.original_image_size[0] - 1))
        y1 = max(0, min(y1, self.original_image_size[1] - 1))
        x2 = max(0, min(x2, self.original_image_size[0] - 1))
        y2 = max(0, min(y2, self.original_image_size[1] - 1))
        
        return (x1, y1, x2, y2)

class PixelPreviewWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: blue; color: white;")
        self.setText("Final Rendering")
        self.pixel_size = 16
        self.frames = []
        self.current_frame_idx = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.crop_rect = None
        
    def set_frames(self, frames, pixel_size=16, fps=10, crop_rect=None):
        self.frames = frames
        self.pixel_size = pixel_size
        self.crop_rect = crop_rect
        self.current_frame_idx = 0
        if frames:
            self.update_frame()
            self.timer.start(int(1000 / fps))
        
    def update_frame(self):
        if not self.frames:
            return
            
        frame = self.frames[self.current_frame_idx].copy()
        
        # Apply cropping if specified
        if self.crop_rect:
            x1, y1, x2, y2 = self.crop_rect
            # Ensure coordinates are valid
            h, w, _ = frame.shape
            x1 = max(0, min(x1, w-1))
            y1 = max(0, min(y1, h-1))
            x2 = max(0, min(x2, w-1))
            y2 = max(0, min(y2, h-1))
            
            # Crop the image
            if x2 > x1 and y2 > y1:
                frame = frame[y1:y2, x1:x2]
        
        # Resize to desired pixel size
        frame_small = cv2.resize(frame, (self.pixel_size, self.pixel_size), 
                                interpolation=cv2.INTER_AREA)
        
        # Resize for display
        frame_display = cv2.resize(frame_small, (200, 200), 
                                  interpolation=cv2.INTER_NEAREST)
        
        # Create QImage and QPixmap
        h, w, c = frame_display.shape
        qimg = QImage(frame_display.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        
        # Center image in widget
        self.setPixmap(pixmap)
        
        # Increment frame index
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
        
    def set_pixel_size(self, size):
        self.pixel_size = size
        if self.frames:
            self.update_frame()
            
    def set_crop_rect(self, crop_rect):
        self.crop_rect = crop_rect
        if self.frames:
            self.update_frame()

class ConversionThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str, str)  # Now returns both original and resized GIF paths
    error_signal = pyqtSignal(str)
    
    def __init__(self, input_file, output_file, fps, size, start_time, duration, crop_rect=None):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.fps = fps
        self.size = size
        self.start_time = start_time
        self.duration = duration
        self.crop_rect = crop_rect
        
    def run(self):
        try:
            # Create temporary directory for images
            temp_dir = tempfile.mkdtemp()
            
            # Calculate output paths for both original size and resized GIFs
            base_name, ext = os.path.splitext(self.output_file)
            original_size_gif = f"{base_name}_original{ext}"
            resized_gif = self.output_file
            
            # Extract images from video
            ffmpeg_path = "ffmpeg"  # Make sure ffmpeg is in your PATH
            
            # Command for extracting images
            time_args = []
            if self.start_time > 0:
                time_args.extend(["-ss", str(self.start_time)])
            if self.duration > 0:
                time_args.extend(["-t", str(self.duration)])
                
            # Progress monitoring setup
            self.progress_signal.emit(10)
                
            # Extract frames at original resolution
            extract_cmd = [
                ffmpeg_path, "-i", self.input_file, 
                *time_args,
                "-vf", f"fps={self.fps}",
                f"{temp_dir}/frame_%04d.png"
            ]
            
            process = subprocess.Popen(extract_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.error_signal.emit(f"Error extracting frames: {stderr.decode()}")
                return
                
            self.progress_signal.emit(30)
                
            # Count extracted images
            frames = [f for f in os.listdir(temp_dir) if f.endswith('.png')]
            frames.sort()
            
            if not frames:
                self.error_signal.emit("No frames were extracted from the video")
                return
                
            # Create original size GIF
            self.progress_signal.emit(40)
            
            # Apply cropping if specified
            crop_filter = ""
            if self.crop_rect:
                x1, y1, x2, y2 = self.crop_rect
                width = x2 - x1
                height = y2 - y1
                crop_filter = f",crop={width}:{height}:{x1}:{y1}"
                
            # Create original size GIF (with cropping if specified)
            original_gif_cmd = [
                ffmpeg_path, "-i", f"{temp_dir}/frame_%04d.png",
                "-vf", f"fps={self.fps}{crop_filter}",
                "-loop", "0",
                original_size_gif
            ]
            
            process = subprocess.Popen(original_gif_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.error_signal.emit(f"Error creating original size GIF: {stderr.decode()}")
                return
                
            self.progress_signal.emit(70)
                
            # Create resized GIF
            resize_filter = f"{crop_filter},scale={self.size}:{self.size}:force_original_aspect_ratio=decrease,pad={self.size}:{self.size}:(ow-iw)/2:(oh-ih)/2"
            
            resized_gif_cmd = [
                ffmpeg_path, "-i", f"{temp_dir}/frame_%04d.png",
                "-vf", f"fps={self.fps}{resize_filter}",
                "-loop", "0",
                resized_gif
            ]
            
            process = subprocess.Popen(resized_gif_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.error_signal.emit(f"Error creating resized GIF: {stderr.decode()}")
                return
                
            self.progress_signal.emit(90)
                
            # Cleanup
            shutil.rmtree(temp_dir)
            
            self.progress_signal.emit(100)
            self.finished_signal.emit(original_size_gif, resized_gif)
            
        except Exception as e:
            self.error_signal.emit(f"Error during conversion: {str(e)}")

class SendToDeviceThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, parent, mac_address, gif_file, size):
        super().__init__()
        self.parent = parent
        self.mac_address = mac_address
        self.gif_file = gif_file
        self.size = size
        
    def run(self):
        try:
            self.progress_signal.emit(10)
            
            # Simulate progress updates
            for i in range(20, 100, 10):
                time.sleep(0.2)  # Simulate work
                self.progress_signal.emit(i)
                
            # Use parent's run_command method (DevicePage)
            if hasattr(self.parent, 'run_command'):
                self.progress_signal.emit(90)
                
                # Run the command to send GIF to device
                self.parent.run_command([
                    "--address", self.mac_address,
                    "--set-gif", self.gif_file,
                    "--process-gif", self.size
                ])
                
                self.progress_signal.emit(100)
                self.finished_signal.emit("GIF sent to device successfully")
            else:
                self.error_signal.emit("Cannot send to device: parent object does not have run_command method")
                
        except Exception as e:
            self.error_signal.emit(f"Failed to send GIF to device: {str(e)}")

class VideoToGifDialog(QDialog):
    def __init__(self, mac_address=None, parent=None):
        super().__init__(parent)
        self.mac_address = mac_address
        self.parent = parent
        self.video_file = None
        self.output_file = None
        self.original_size_gif = None
        self.resized_gif = None
        self.temp_gif_file = None
        self.frames = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Convert Video to GIF")
        self.setMinimumWidth(700)
        
        layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No video selected")
        file_button = QPushButton("Select Video")
        file_button.clicked.connect(self.select_video)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(file_button)
        layout.addLayout(file_layout)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Video trackbar
        trackbar_layout = QHBoxLayout()
        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setMinimum(0)
        self.video_slider.setMaximum(100)  # Will be updated when video is loaded
        self.video_slider.valueChanged.connect(self.slider_changed)
        
        self.time_label = QLabel("00:00.000 / 00:00.000")
        
        trackbar_layout.addWidget(self.video_slider)
        trackbar_layout.addWidget(self.time_label)
        layout.addLayout(trackbar_layout)
        
        # Preview area
        preview_layout = QHBoxLayout()
        
        # Video preview
        video_preview_layout = QVBoxLayout()
        self.video_preview = VideoPreviewWidget()
        video_preview_layout.addWidget(self.video_preview)
        
        # Video controls
        video_controls_layout = QHBoxLayout()
        play_pause_button = QPushButton("Play/Pause")
        play_pause_button.clicked.connect(self.play_pause)
        video_controls_layout.addWidget(play_pause_button)
        
        # Jump backward/forward buttons
        jump_back_button = QPushButton("-2s")
        jump_back_button.clicked.connect(lambda: self.video_preview.jump_backward(2))
        video_controls_layout.addWidget(jump_back_button)
        
        jump_forward_button = QPushButton("+2s")
        jump_forward_button.clicked.connect(lambda: self.video_preview.jump_forward(2))
        video_controls_layout.addWidget(jump_forward_button)
        
        set_start_button = QPushButton("Set Start")
        set_start_button.clicked.connect(self.set_start)
        video_controls_layout.addWidget(set_start_button)
        
        set_end_button = QPushButton("Set End")
        set_end_button.clicked.connect(self.set_end)
        video_controls_layout.addWidget(set_end_button)
        
        video_preview_layout.addLayout(video_controls_layout)
        
        # Time info display
        time_info_layout = QHBoxLayout()
        self.start_time_label = QLabel("Start: 00:00.000")
        self.end_time_label = QLabel("End: 00:00.000")
        time_info_layout.addWidget(self.start_time_label)
        time_info_layout.addWidget(self.end_time_label)
        video_preview_layout.addLayout(time_info_layout)
        
        preview_layout.addLayout(video_preview_layout)
        
        # GIF preview
        gif_preview_layout = QVBoxLayout()
        self.gif_preview = GifPreviewWidget()
        self.gif_preview.selection_changed.connect(self.selection_changed)
        gif_preview_layout.addWidget(self.gif_preview)
        
        gif_label = QLabel("TempGif [Start:End]")
        gif_label.setAlignment(Qt.AlignCenter)
        gif_preview_layout.addWidget(gif_label)
        
        preview_layout.addLayout(gif_preview_layout)
        
        # Pixel preview
        pixel_preview_layout = QVBoxLayout()
        self.pixel_preview = PixelPreviewWidget()
        pixel_preview_layout.addWidget(self.pixel_preview)
        
        # Size and FPS options
        options_layout = QHBoxLayout()
        
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["16x16", "32x32", "64x64"])
        self.size_combo.currentIndexChanged.connect(self.update_pixel_preview)
        size_layout.addWidget(self.size_combo)
        
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)  # Increased max FPS to 60
        self.fps_spin.setValue(10)
        self.fps_spin.valueChanged.connect(self.update_pixel_preview)
        fps_layout.addWidget(self.fps_spin)
        
        options_layout.addLayout(size_layout)
        options_layout.addLayout(fps_layout)
        
        pixel_preview_layout.addLayout(options_layout)
        preview_layout.addLayout(pixel_preview_layout)
        
        layout.addLayout(preview_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_video)
        self.convert_button.setEnabled(False)
        
        self.send_button = QPushButton("Send to Device")
        self.send_button.clicked.connect(self.send_to_device)
        self.send_button.setEnabled(False)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.convert_button)
        buttons_layout.addWidget(self.send_button)
        buttons_layout.addWidget(close_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # Timer to update slider during playback
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_slider)
        self.update_timer.start(100)  # Update every 100ms
        
    def select_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "", 
            "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv);;All Files (*)", 
            options=options
        )
        
        if file_path:
            self.video_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            
            # Load video in preview
            if self.video_preview.load_video(file_path):
                self.convert_button.setEnabled(True)
                
                # Update slider
                self.video_slider.setMaximum(self.video_preview.total_frames - 1)
                self.video_slider.setValue(0)
                
                # Update time labels
                self.update_time_labels()
                
                # Create temporary GIF
                self.create_temp_gif()
            
    def slider_changed(self):
        if not self.video_preview.cap:
            return
            
        # Update frame index
        self.video_preview.current_frame_idx = self.video_slider.value()
        self.video_preview.update_frame()
        
        # Update time label
        self.update_time_labels()
        
    def update_slider(self):
        if not self.video_preview.cap or not self.video_preview.is_playing:
            return
            
        # Update slider without triggering valueChanged
        self.video_slider.blockSignals(True)
        self.video_slider.setValue(self.video_preview.current_frame_idx)
        self.video_slider.blockSignals(False)
        
        # Update time label
        self.update_time_labels()
        
    def update_time_labels(self):
        if not self.video_preview.cap:
            return
            
        # Update current time label
        current_time = self.video_preview.get_time_str(self.video_preview.current_frame_idx)
        total_time = self.video_preview.get_time_str(self.video_preview.total_frames - 1)
        self.time_label.setText(f"{current_time} / {total_time}")
        
        # Update start and end time labels
        start_time = self.video_preview.get_time_str(self.video_preview.start_frame)
        end_time = self.video_preview.get_time_str(self.video_preview.end_frame)
        self.start_time_label.setText(f"Start: {start_time}")
        self.end_time_label.setText(f"End: {end_time}")
        
    def play_pause(self):
        self.video_preview.play_pause()
        
    def set_start(self):
        self.video_preview.set_start()
        self.update_time_labels()
        self.create_temp_gif()
        
    def set_end(self):
        self.video_preview.set_end()
        self.update_time_labels()
        self.create_temp_gif()
        
    def selection_changed(self, crop_rect):
        # Update pixel preview with new crop rectangle
        self.update_pixel_preview()
        
    def create_temp_gif(self):
        if not self.video_file:
            return
            
        # Create temporary GIF for preview
        try:
            # Extract frames for preview
            cap = cv2.VideoCapture(self.video_file)
            if not cap.isOpened():
                return
                
            start_frame = self.video_preview.start_frame
            end_frame = self.video_preview.end_frame
            
            # Calculate total frames to extract
            total_frames = end_frame - start_frame + 1
            
            # Use actual FPS for preview to match final output
            fps = self.fps_spin.value()
            
            # Calculate frame step to maintain timing
            # For preview, we'll use fewer frames but maintain timing
            max_preview_frames = 20
            step = max(1, total_frames // max_preview_frames)
            
            frames = []
            for i in range(start_frame, end_frame + 1, step):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame)
                    
            cap.release()
            
            if frames:
                self.frames = frames
                self.gif_preview.set_frames(frames, fps)
                self.update_pixel_preview()
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create temporary GIF: {str(e)}")
            
    def update_pixel_preview(self):
        if not self.frames:
            return
            
        size = int(self.size_combo.currentText().split('x')[0])
        crop_rect = self.gif_preview.get_selection_rect()
        self.pixel_preview.set_frames(self.frames, size, self.fps_spin.value(), crop_rect)
            
    def convert_video(self):
        if not self.video_file:
            QMessageBox.warning(self, "Error", "Please select a video file first")
            return
            
        # Ask user for output directory
        options = QFileDialog.Options()
        output_dir = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", "", options=options
        )
        
        if not output_dir:
            return  # User cancelled
            
        # Ask user for output filename
        default_filename = os.path.splitext(os.path.basename(self.video_file))[0] + ".gif"
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save GIF As", os.path.join(output_dir, default_filename), 
            "GIF Files (*.gif)", options=options
        )
        
        if not file_name:
            return  # User cancelled
            
        if not file_name.lower().endswith('.gif'):
            file_name += '.gif'
                
        self.output_file = file_name
        size = int(self.size_combo.currentText().split('x')[0])
        fps = self.fps_spin.value()
        start_time = self.video_preview.get_start_time()
        duration = self.video_preview.get_duration_seconds()
        
        # Get crop rectangle if available
        crop_rect = self.gif_preview.get_selection_rect()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.convert_button.setEnabled(False)
        self.status_label.setText("Converting video to GIF...")
        
        self.conversion_thread = ConversionThread(
            self.video_file, self.output_file, 
            fps, size, start_time, duration, crop_rect
        )
        self.conversion_thread.progress_signal.connect(self.update_progress)
        self.conversion_thread.finished_signal.connect(self.conversion_finished)
        self.conversion_thread.error_signal.connect(self.conversion_error)
        self.conversion_thread.start()
            
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def conversion_finished(self, original_gif, resized_gif):
        self.progress_bar.setValue(100)
        self.convert_button.setEnabled(True)
        self.send_button.setEnabled(True)
        self.original_size_gif = original_gif
        self.resized_gif = resized_gif
        self.status_label.setText(f"GIF created successfully")
        
        message = (f"GIFs created successfully:\n\n"
                  f"Original size: {os.path.basename(original_gif)}\n"
                  f"Resized ({self.size_combo.currentText()}): {os.path.basename(resized_gif)}")
        
        QMessageBox.information(self, "Success", message)
        
    def conversion_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.convert_button.setEnabled(True)
        self.status_label.setText(f"Error: {error_message}")
        QMessageBox.critical(self, "Error", error_message)
        
    def send_to_device(self):
        if not self.resized_gif or not self.mac_address:
            QMessageBox.warning(self, "Error", "No GIF available to send or no device connected")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.send_button.setEnabled(False)
        self.status_label.setText("Sending GIF to device...")
        
        size = self.size_combo.currentText().split('x')[0]
        
        self.send_thread = SendToDeviceThread(
            self.parent, self.mac_address, self.resized_gif, size
        )
        self.send_thread.progress_signal.connect(self.update_progress)
        self.send_thread.finished_signal.connect(self.send_finished)
        self.send_thread.error_signal.connect(self.send_error)
        self.send_thread.start()
            
    def send_finished(self, message):
        self.progress_bar.setValue(100)
        self.send_button.setEnabled(True)
        self.status_label.setText("GIF sent to device successfully")
        QMessageBox.information(self, "Success", message)
        
    def send_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.send_button.setEnabled(True)
        self.status_label.setText(f"Error: {error_message}")
        QMessageBox.critical(self, "Error", error_message)
            
    def closeEvent(self, event):
        # Clean up resources
        self.video_preview.cleanup()
        self.update_timer.stop()
        event.accept()
