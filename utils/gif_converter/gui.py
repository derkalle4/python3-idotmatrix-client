from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class GifConverterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.mac_address = parent.mac_address if hasattr(parent, 'mac_address') else None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("GIF Converter")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Button to convert video to GIF
        convert_button = QPushButton("Convert Video to GIF")
        convert_button.clicked.connect(self.convert_video)
        layout.addWidget(convert_button)
        
        self.setLayout(layout)
    
    def convert_video(self):
        try:
            from utils.gif_converter.video_converter import VideoToGifDialog
            dialog = VideoToGifDialog(self.mac_address, self)
            dialog.exec_()
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Could not load video converter: {str(e)}")
