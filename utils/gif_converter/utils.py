from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QLineEdit,
    QFileDialog, QMessageBox, QComboBox, QGroupBox, QPushButton
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QSize, QTimer, QRect
from PyQt5.QtGui import QMovie, QPixmap, QPainter, QPen, QColor, QImage
import os
import subprocess
import tempfile
import shutil

class VideoToGifDialog(QDialog):
    def __init__(self, mac_address, parent=None):
        super().__init__(parent)
        self.mac_address = mac_address
        self.parent = parent
        self.setWindowTitle("Video to GIF Converter")
        self.setMinimumSize(900, 700)
        
        # Variables
        self.video_path = ""
        self.ffmpeg_path = "ffmpeg"  # Assumes ffmpeg is in PATH
        self.start_time = 0
        self.end_time = 0
        self.crop_rect = QRect(0, 0, 100, 100)
        self.is_drawing = False
        self.start_point = None
        self.screenshot = None
        self.temp_gif_path = None
        
        # Initialize UI
        self.init_ui()
        
        # Timer for preview updates
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(100)
        self.update_timer.timeout.connect(self.update_preview)
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Top section: Video player
        video_group = QGroupBox("Video Player")
        video_layout = QVBoxLayout()
        
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 360)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        video_layout.addWidget(self.video_widget)
        
        # Video controls
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_video)
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)
        
        self.position_label = QLabel("00:00 / 00:00")
        
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.position_slider)
        controls_layout.addWidget(self.position_label)
        
        video_layout.addLayout(controls_layout)
        
        # Time selection
        time_layout = QHBoxLayout()
        
        self.start_time_button = QPushButton("Set Start")
        self.start_time_button.clicked.connect(self.set_start_time)
        
        self.start_time_edit = QLineEdit("0.000")
        self.start_time_edit.setFixedWidth(80)
        
        self.end_time_button = QPushButton("Set End")
        self.end_time_button.clicked.connect(self.set_end_time)
        
        self.end_time_edit = QLineEdit("0.000")
        self.end_time_edit.setFixedWidth(80)
        
        time_layout.addWidget(self.start_time_button)
        time_layout.addWidget(self.start_time_edit)
        time_layout.addWidget(self.end_time_button)
        time_layout.addWidget(self.end_time_edit)
        time_layout.addStretch()
        
        video_layout.addLayout(time_layout)
        
        video_group.setLayout(video_layout)
        main_layout.addWidget(video_group)
        
        # Middle section: Screenshot and preview
        preview_layout = QHBoxLayout()
        
        # Screenshot area
        screenshot_group = QGroupBox("Frame Selection")
        screenshot_layout = QVBoxLayout()
        
        self.screenshot_label = QLabel("Click Pause to capture a frame")
        self.screenshot_label.setMinimumSize(320, 240)
        self.screenshot_label.setAlignment(Qt.AlignCenter)
        self.screenshot_label.setStyleSheet("border: 1px solid black;")
        self.screenshot_label.setMouseTracking(True)
        self.screenshot_label.mousePressEvent = self.screenshot_mouse_press
        self.screenshot_label.mouseMoveEvent = self.screenshot_mouse_move
        self.screenshot_label.mouseReleaseEvent = self.screenshot_mouse_release
        
        screenshot_layout.addWidget(self.screenshot_label)
        
        self.crop_info_edit = QLineEdit("X:0;Y:0;100")
        self.crop_info_edit.setReadOnly(True)
        screenshot_layout.addWidget(self.crop_info_edit)
        
        screenshot_group.setLayout(screenshot_layout)
        preview_layout.addWidget(screenshot_group)
        
        # GIF Preview
        preview_group = QGroupBox("GIF Preview")
        preview_inner_layout = QVBoxLayout()
        
        self.preview_label = QLabel("GIF Preview")
        self.preview_label.setMinimumSize(320, 240)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid black;")
        
        preview_inner_layout.addWidget(self.preview_label)
        
        # Size selection
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Output Size:"))
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["16x16", "32x32", "64x64"])
        self.size_combo.setCurrentIndex(1)  # 32x32 default
        
        size_layout.addWidget(self.size_combo)
        size_layout.addStretch()
        
        preview_inner_layout.addLayout(size_layout)
        preview_group.setLayout(preview_inner_layout)
        preview_layout.addWidget(preview_group)
        
        main_layout.addLayout(preview_layout)
        
        # Bottom section: Action buttons
        button_layout = QHBoxLayout()
        
        self.load_video_button = QPushButton("Load Video")
        self.load_video_button.clicked.connect(self.load_video)
        
        self.generate_gif_button = QPushButton("Generate GIF")
        self.generate_gif_button.clicked.connect(self.generate_gif)
        
        self.save_gif_button = QPushButton("Save GIF")
        self.save_gif_button.clicked.connect(self.save_gif)
        
        self.send_to_device_button = QPushButton("Send to Device")
        self.send_to_device_button.clicked.connect(self.send_to_device)
        
        button_layout.addWidget(self.load_video_button)
        button_layout.addWidget(self.generate_gif_button)
        button_layout.addWidget(self.save_gif_button)
        button_layout.addWidget(self.send_to_device_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Disable buttons initially
        self.enable_video_controls(False)
        self.generate_gif_button.setEnabled(False)
        self.save_gif_button.setEnabled(False)
        self.send_to_device_button.setEnabled(False)
    
    def enable_video_controls(self, enabled):
        self.play_button.setEnabled(enabled)
        self.pause_button.setEnabled(enabled)
        self.position_slider.setEnabled(enabled)
        self.start_time_button.setEnabled(enabled)
        self.end_time_button.setEnabled(enabled)
    
    def load_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
            options=options
        )
        
        if file_path:
            self.video_path = file_path
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.enable_video_controls(True)
            self.play_video()
    
    def play_video(self):
        if self.media_player.state() != QMediaPlayer.PlayingState:
            self.media_player.play()
    
    def pause_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.capture_current_frame()
    
    def position_changed(self, position):
        self.position_slider.setValue(position)
        
        # Update time display
        duration = self.media_player.duration()
        if duration > 0:
            current_secs = position / 1000.0
            total_secs = duration / 1000.0
            self.position_label.setText(f"{int(current_secs//60):02d}:{int(current_secs%60):02d} / {int(total_secs//60):02d}:{int(total_secs%60):02d}")
    
    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
    
    def set_position(self, position):
        self.media_player.setPosition(position)
    
    def set_start_time(self):
        current_time = self.media_player.position() / 1000.0
        self.start_time = current_time
        self.start_time_edit.setText(f"{current_time:.3f}")
        self.generate_gif_button.setEnabled(True)
    
    def set_end_time(self):
        current_time = self.media_player.position() / 1000.0
        if current_time > float(self.start_time_edit.text()):
            self.end_time = current_time
            self.end_time_edit.setText(f"{current_time:.3f}")
            self.generate_gif_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Invalid End Time", "End time must be after start time")
    
    def capture_current_frame(self):
        if not self.video_path:
            return
        
        try:
            # Create a temporary file for the screenshot
            temp_dir = tempfile.gettempdir()
            temp_image = os.path.join(temp_dir, "temp_screenshot.png")
            
            # Get current position
            current_time = self.media_player.position() / 1000.0
            
            # Use ffmpeg to capture the frame
            subprocess.call([
                self.ffmpeg_path, '-y',
                '-ss', str(current_time),
                '-i', self.video_path,
                '-vframes', '1',
                '-q:v', '2',
                temp_image
            ])
            
            if os.path.exists(temp_image):
                # Load the image
                self.screenshot = QPixmap(temp_image)
                self.screenshot_label.setPixmap(self.screenshot.scaled(
                    self.screenshot_label.width(),
                    self.screenshot_label.height(),
                    Qt.KeepAspectRatio
                ))
                
                # Initialize crop rectangle
                self.crop_rect = QRect(0, 0, 100, 100)
                self.update_crop_preview()
                
                # Start the update timer
                self.update_timer.start()
                
                # Clean up
                try:
                    os.remove(temp_image)
                except:
                    pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to capture frame: {str(e)}")
    
    def screenshot_mouse_press(self, event):
        if self.screenshot and event.button() == Qt.LeftButton:
            self.is_drawing = True
            self.start_point = self.get_scaled_point(event.pos())
            self.update_crop_preview()
    
    def screenshot_mouse_move(self, event):
        if self.is_drawing and self.screenshot:
            current_point = self.get_scaled_point(event.pos())
            
            # Calculate square size (1:1 ratio)
            size = min(abs(current_point.x() - self.start_point.x()), 
                      abs(current_point.y() - self.start_point.y()))
            size = max(size, 100)  # Minimum size of 100 pixels
            
            # Calculate coordinates to maintain a square
            x = self.start_point.x() if current_point.x() >= self.start_point.x() else self.start_point.x() - size
            y = self.start_point.y() if current_point.y() >= self.start_point.y() else self.start_point.y() - size
            
            # Ensure the square stays within the image bounds
            img_width = self.screenshot.width()
            img_height = self.screenshot.height()
            x = max(0, min(x, img_width - size))
            y = max(0, min(y, img_height - size))
            
            # Update the rectangle
            self.crop_rect = QRect(x, y, size, size)
            
            # Update the display
            self.update_crop_preview()
            
            # Update coordinates in the textbox
            self.crop_info_edit.setText(f"X:{x};Y:{y};{size}")
    
    def screenshot_mouse_release(self, event):
        if event.button() == Qt.LeftButton:
            self.is_drawing = False
            if not self.crop_rect.isEmpty():
                self.update_preview()
    
    def get_scaled_point(self, mouse_point):
        if not self.screenshot:
            return mouse_point
        
        # Calculate the scale ratio
        pixmap_rect = self.screenshot_label.pixmap().rect()
        label_rect = self.screenshot_label.rect()
        
        # Calculate margins
        margin_left = (label_rect.width() - pixmap_rect.width()) / 2
        margin_top = (label_rect.height() - pixmap_rect.height()) / 2
        
        # Adjust coordinates
        x = int((mouse_point.x() - margin_left) * (self.screenshot.width() / pixmap_rect.width()))
        y = int((mouse_point.y() - margin_top) * (self.screenshot.height() / pixmap_rect.height()))
        
        return QPoint(x, y)
    
    def update_crop_preview(self):
        if not self.screenshot:
            return
        
        # Create a copy of the screenshot
        pixmap = QPixmap(self.screenshot)
        painter = QPainter(pixmap)
        
        # Draw the selection rectangle
        white_pen = QPen(QColor(255, 255, 255), 4)
        painter.setPen(white_pen)
        painter.drawRect(self.crop_rect)
        
        red_pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(red_pen)
        painter.drawRect(self.crop_rect)
        
        painter.end()
        
        # Update the label
        self.screenshot_label.setPixmap(pixmap.scaled(
            self.screenshot_label.width(),
            self.screenshot_label.height(),
            Qt.KeepAspectRatio
        ))
    
    def update_preview(self):
        if not self.screenshot or self.crop_rect.isEmpty():
            return
        
        try:
            # Get the selected size
            size_text = self.size_combo.currentText()
            output_size = int(size_text.split('x')[0])
            
            # Create a pixelated version of the selected area
            cropped = self.screenshot.copy(self.crop_rect)
            scaled = cropped.scaled(output_size, output_size, Qt.KeepAspectRatio, Qt.FastTransformation)
            
            # Display the preview
            self.preview_label.setPixmap(scaled.scaled(
                self.preview_label.width(),
                self.preview_label.height(),
                Qt.KeepAspectRatio
            ))
        except Exception as e:
            print(f"Error updating preview: {str(e)}")
    
    def generate_gif(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "No video loaded")
            return
        
        try:
            start_time = float(self.start_time_edit.text())
            end_time = float(self.end_time_edit.text())
            
            if start_time >= end_time:
                QMessageBox.warning(self, "Error", "Start time must be less than end time")
                return
            
            # Parse crop values
            crop_values = self.crop_info_edit.text().split(";")
            if len(crop_values) != 3:
                QMessageBox.warning(self, "Error", "Invalid crop format")
                return
            
            x = int(crop_values[0].replace("X:", ""))
            y = int(crop_values[1].replace("Y:", ""))
            size = int(crop_values[2])
            
            # Get selected output size
            output_size = int(self.size_combo.currentText().split('x')[0])
            
            # Create temporary files
            temp_dir = tempfile.gettempdir()
            palette_path = os.path.join(temp_dir, "palette.png")
            self.temp_gif_path = os.path.join(temp_dir, "temp_preview.gif")
            
            # Generate palette for better quality
            subprocess.call([
                self.ffmpeg_path, '-y',
                '-ss', str(start_time),
                '-t', str(end_time - start_time),
                '-i', self.video_path,
                '-vf', f'crop={size}:{size}:{x}:{y},palettegen',
                palette_path
            ])
            
            # Create GIF with the palette
            subprocess.call([
                self.ffmpeg_path, '-y',
                '-ss', str(start_time),
                '-t', str(end_time - start_time),
                '-i', self.video_path,
                '-i', palette_path,
                '-lavfi', f'crop={size}:{size}:{x}:{y} [x]; [x][1:v] paletteuse,scale={output_size}:{output_size}:flags=lanczos',
                '-f', 'gif',
                self.temp_gif_path
            ])
            
            # Display the GIF
            if os.path.exists(self.temp_gif_path):
                movie = QMovie(self.temp_gif_path)
                movie.setScaledSize(QSize(self.preview_label.width(), self.preview_label.height()))
                self.preview_label.setMovie(movie)
                movie.start()
                
                # Enable save and send buttons
                self.save_gif_button.setEnabled(True)
                self.send_to_device_button.setEnabled(True)
            
            # Clean up palette file
            if os.path.exists(palette_path):
                os.remove(palette_path)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate GIF: {str(e)}")
    
    def save_gif(self):
        if not self.temp_gif_path or not os.path.exists(self.temp_gif_path):
            QMessageBox.warning(self, "Error", "No GIF generated yet")
            return
        
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save GIF As", "",
            "GIF Files (*.gif)",
            options=options
        )
        
        if save_path:
            if not save_path.lower().endswith('.gif'):
                save_path += '.gif'
            
            try:
                # Copy temporary GIF to chosen location
                shutil.copy2(self.temp_gif_path, save_path)
                QMessageBox.information(self, "Success", f"GIF saved as {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save GIF: {str(e)}")
    
    def send_to_device(self):
        if not self.temp_gif_path or not os.path.exists(self.temp_gif_path):
            QMessageBox.warning(self, "Error", "No GIF generated yet")
            return
        
        try:
            # Use existing method to send GIF to device
            self.parent.run_command([
                "--address", self.mac_address,
                "--set-gif", self.temp_gif_path
            ])
            QMessageBox.information(self, "Success", "GIF sent to device")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send GIF to device: {str(e)}")