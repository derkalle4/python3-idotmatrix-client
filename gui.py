import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageSequence
import imageio
import numpy



from utils.utils import digits,patterns, colors, api_key
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget,
    QPlainTextEdit, QHBoxLayout, QMessageBox, QListWidgetItem, QGridLayout,
    QDialog, QLineEdit, QListWidget, QInputDialog, QCheckBox, QDialogButtonBox,
    QComboBox, QColorDialog, QSlider, QMenu, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QProcess, QSettings, pyqtSignal
import sys, re, copy

# --- Dialog Classes ---
class ClockStyleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Clock Style')
        self.layout = QVBoxLayout(self)

        # Available clock styles
        self.clock_styles = ['Default', 'Christmas', 'Racing', 'Inverted Full Screen', 'Animated Hourglass', 'Frame 1', 'Frame 2', 'Frame 3']
        self.selected_color = None  # Variable to hold the selected color

        # Clock style selection
        self.clock_style_label = QLabel('Select Clock Style:')
        self.clock_style_combo = QComboBox(self)
        self.clock_style_combo.addItems(self.clock_styles)
        
        # Checkboxes for additional options
        self.show_date_checkbox = QCheckBox('Show Date', self)
        self.show_24hr_checkbox = QCheckBox('24-Hour Format', self)
        
        # Color picker button
        self.color_picker_button = QPushButton('Choose Color', self)
        self.color_picker_button.clicked.connect(self.open_color_dialog)
        
        # Dialog button box (OK and Cancel)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Add widgets to the layout
        self.layout.addWidget(self.clock_style_label)
        self.layout.addWidget(self.clock_style_combo)
        self.layout.addWidget(self.show_date_checkbox)
        self.layout.addWidget(self.show_24hr_checkbox)
        self.layout.addWidget(self.color_picker_button)
        self.layout.addWidget(self.button_box)

    def open_color_dialog(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.selected_color = color_dialog.selectedColor()
            self.color_picker_button.setStyleSheet(f"background-color: {self.selected_color.name()}")

    def get_options(self):
        if self.exec_() == QDialog.Accepted:
            clock_style = self.clock_style_combo.currentText()
            show_date = self.show_date_checkbox.isChecked()
            show_24hr = self.show_24hr_checkbox.isChecked()
            return clock_style, show_date, show_24hr, self.selected_color, True
        else:
            return None, None, None, None, False


class CustomInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Input')
        self.layout = QVBoxLayout(self)

        self.label = QLabel('Name this device?', self)
        self.layout.addWidget(self.label)

        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)

        self.button_layout = QHBoxLayout()
        self.yes_button = QPushButton('Yes', self)
        self.no_button = QPushButton('No', self)
        self.button_layout.addWidget(self.yes_button)
        self.button_layout.addWidget(self.no_button)
        self.layout.addLayout(self.button_layout)

        self.yes_button.clicked.connect(self.accept)
        self.no_button.clicked.connect(self.reject)

    def get_input(self):
        if self.exec_() == QDialog.Accepted:
            return self.line_edit.text(), True
        else:
            return '', False

class SizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Pixel Display Size")
        layout = QVBoxLayout()
        self.size_combo = QComboBox()
        self.size_combo.addItems(["16x16", "32x32"])
        layout.addWidget(self.size_combo)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def get(self):
        if self.exec_() == QDialog.Accepted:
            return self.size_combo.currentText().split("x")[0], True
        else:
            return "16", False



class TextStyleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Text Settings')
        self.layout = QVBoxLayout(self)

        # Initialize selected colors
        self.selected_text_color = None
        self.selected_bg_color = None

        # Text input
        self.text_label = QLabel('Enter Text:')
        self.text_input = QLineEdit(self)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.text_input)

        # Text Size
        self.text_size_label = QLabel('Text Size:')
        self.text_size_combo = QComboBox(self)
        self.text_size_combo.addItems(["16", "32"])
        self.layout.addWidget(self.text_size_label)
        self.layout.addWidget(self.text_size_combo)

        # Text Mode
        self.text_mode_label = QLabel('Text Style:')
        self.text_mode_combo = QComboBox(self)
        self.text_mode_combo.addItems(["", "Left", "Right", "Up", "Down", "Blink", "Breathe", "Snowflake", "Laser"])
        self.layout.addWidget(self.text_mode_label)
        self.layout.addWidget(self.text_mode_combo)

        # Text Speed
        self.text_speed_label = QLabel('Text Speed:')
        self.text_speed_slider = QSlider(Qt.Horizontal)
        self.text_speed_slider.setRange(0, 100)
        self.layout.addWidget(self.text_speed_label)
        self.layout.addWidget(self.text_speed_slider)

        # Text Color Mode
        self.text_color_mode_label = QLabel('Text Color Effect:')
        self.text_color_mode_combo = QComboBox(self)
        self.text_color_mode_combo.addItems(["", "Solid", "Rainbow", "Sunset", "Neon", "Calm"])
        self.layout.addWidget(self.text_color_mode_label)
        self.layout.addWidget(self.text_color_mode_combo)

        # Text Color
        self.text_color_button = QPushButton('Choose Text Color')
        self.text_color_button.clicked.connect(self.choose_text_color)
        self.layout.addWidget(self.text_color_button)

        # Text Background Mode
        self.text_bg_mode_label = QLabel('Background Style:')
        self.text_bg_mode_combo = QComboBox(self)
        self.text_bg_mode_combo.addItems(["None", "Solid"])
        self.layout.addWidget(self.text_bg_mode_label)
        self.layout.addWidget(self.text_bg_mode_combo)

        # Text Background Color
        self.text_bg_color_button = QPushButton('Choose Background Color')
        self.text_bg_color_button.clicked.connect(self.choose_bg_color)
        self.layout.addWidget(self.text_bg_color_button)

        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def choose_text_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.selected_text_color = color_dialog.selectedColor()
            self.text_color_button.setStyleSheet(f"background-color: {self.selected_text_color.name()}")

    def choose_bg_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.selected_bg_color = color_dialog.selectedColor()
            self.text_bg_color_button.setStyleSheet(f"background-color: {self.selected_bg_color.name()}")

    def get_settings(self):
        if self.exec_() == QDialog.Accepted:
            return (
                self.text_input.text(),
                int(self.text_size_combo.currentText()),
                self.text_mode_combo.currentIndex(),
                self.text_speed_slider.value(),
                self.text_color_mode_combo.currentIndex(),
                self.selected_text_color,
                self.text_bg_mode_combo.currentIndex(),
                self.selected_bg_color,
            )
        else:
            return None

class ColorControlDialog(QDialog):
    accepted = pyqtSignal(str, bool)

    def __init__(self, parent=None, mac_address=None):
        super().__init__(parent)
        self.setWindowTitle('Color Control')
        self.mac_address = mac_address
        self.layout = QVBoxLayout(self)

        # Initialize buttons
        self.fullscreen_color_button = QPushButton('Fullscreen Color')
        self.pixel_paint_button = QPushButton('Pixel Paint')

        # Connect buttons to their respective slots
        self.fullscreen_color_button.clicked.connect(lambda: self.choose_color(False))
        self.pixel_paint_button.clicked.connect(self.open_pixel_paint_dialog)

        # Add buttons to layout
        self.layout.addWidget(self.fullscreen_color_button)
        self.layout.addWidget(self.pixel_paint_button)

        # Dialog button box (OK and Cancel)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        # Initialize variables for selected color and mode
        self.selected_color = None
        self.is_pixel_paint = False

    def choose_color(self, is_pixel_paint):
        color_dialog = QColorDialog(self)
        if is_pixel_paint:
            color_dialog.setOption(QColorDialog.ShowAlphaChannel)
        if color_dialog.exec_() == QDialog.Accepted:
            self.selected_color = color_dialog.selectedColor()
            self.is_pixel_paint = is_pixel_paint

    def open_pixel_paint_dialog(self):
        dialog = PixelPaintDialog(self.mac_address)
        dialog.exec_()

    def accept(self):
        if self.selected_color and not self.is_pixel_paint:
            self.accepted.emit(self.selected_color.name(), self.is_pixel_paint)
        super().accept()

class PixelPaintDialog(QDialog):
    
    FAVORITES_KEY = "PixelPaintFavorites"
    
    def __init__(self, mac_address):
        super().__init__()
        self.mac_address = mac_address
        self.init_ui()
        self.load_favorites()
        self.finished.connect(self.save_favorites)

    def init_ui(self):
        self.setWindowTitle('Pixel Paint')
        self.setGeometry(100, 100, 800, 800)

        self.current_color = QColor(0, 0, 0)
        self.grid_size = 32
        self.cell_size = 20
        self.grid = [[QColor(255, 255, 255) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.undo_stack = []
        self.current_stroke = []
        self.setWindowIcon(QIcon('gui/idmc.ico'))

        layout = QVBoxLayout()
        
        toolbar_layout = QHBoxLayout()
        self.color_buttons = []
        common_colors = [  
            ((254, 254, 254), "White"), 
            ((255, 0, 0), "Red"), 
            ((0, 255, 0), "Green"), 
            ((0, 0, 255), "Blue"),
            ((255, 255, 0), "Yellow"), 
            ((0, 255, 255), "Cyan"), 
            ((255, 0, 255), "Magenta") 
        ]

        for color, label_text in common_colors:
            button = QPushButton(label_text)
            button.setProperty('color_data', color)
            button.setStyleSheet(f"background-color: rgb{color}; border: 2px solid transparent;")
            button.clicked.connect(lambda _, col=color: self.set_current_color(QColor(*col)))
            toolbar_layout.addWidget(button)
            self.color_buttons.append(button)
        
        erase_button = QPushButton("Erase")
        erase_button.setProperty('color_data', (255, 255, 255))
        erase_button.setStyleSheet("background-color: white; border: 2px solid transparent;")
        erase_button.clicked.connect(self.erase_cell)
        toolbar_layout.addWidget(erase_button) 
        self.color_buttons.append(erase_button)
        
        color_picker_button = QPushButton('Pick Color')
        color_picker_button.clicked.connect(self.pick_color)
        toolbar_layout.addWidget(color_picker_button)
        
        layout.addLayout(toolbar_layout)

        self.favorites_list = QListWidget()
        self.favorites_list.setMaximumWidth(200)
        self.favorites_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.favorites_list.customContextMenuRequested.connect(self.show_favorites_context_menu)
        
        button_layout = QHBoxLayout()
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_grid)
        button_layout.addWidget(save_button)
        
        load_button = QPushButton('Load')
        load_button.clicked.connect(self.load_grid)
        button_layout.addWidget(load_button)
        
        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.clear_grid)
        button_layout.addWidget(clear_button)
        
        undo_button = QPushButton('Undo')
        undo_button.clicked.connect(self.undo)
        button_layout.addWidget(undo_button)
        
        layout.addLayout(button_layout)

        self.grid_widget = QGridLayout()
        self.grid_widget.setSpacing(0)
        self.grid_labels = []
        for row in range(self.grid_size):
            row_labels = []
            for col in range(self.grid_size):
                label = QLabel()
                label.setFixedSize(self.cell_size, self.cell_size)
                label.setStyleSheet("border: 1px solid black; background-color: white;")
                label.mousePressEvent = lambda event, r=row, c=col: self.paint_cell(r, c)
                label.mouseMoveEvent = self.mouse_move_event
                self.grid_widget.addWidget(label, row, col)
                row_labels.append(label)
            self.grid_labels.append(row_labels)

        grid_container = QVBoxLayout()
        grid_container.addLayout(self.grid_widget)

        layout_with_favorites = QHBoxLayout()
        layout_with_favorites.addWidget(self.favorites_list)
        layout_with_favorites.addLayout(grid_container)
        layout.addLayout(layout_with_favorites)
        
        send_clear_layout = QHBoxLayout()
        send_button = QPushButton('Send to Device')
        send_button.clicked.connect(self.send_grid)
        send_clear_layout.addWidget(send_button)

        clear_device_button = QPushButton('Clear Device')
        clear_device_button.clicked.connect(self.clear_device)
        send_clear_layout.addWidget(clear_device_button)
        
        layout.addLayout(send_clear_layout)

        # Close button
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
    
    def set_current_color(self, color):
        self.current_color = color
        for button in self.color_buttons:
            if button.property('color_data') == (color.red(), color.green(), color.blue()):
                button.setStyleSheet(f"background-color: rgb{color.red(), color.green(), color.blue()}; border: 2px solid gray;")
            else:
                button.setStyleSheet(f"background-color: rgb{button.property('color_data')}; border: 2px solid transparent;")

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_current_color(color)
    
    def erase_cell(self):
        self.set_current_color(QColor(255, 255, 255))

    def paint_cell(self, row, col):
        if not self.current_stroke:
            self.undo_stack.append([])
        self.current_stroke.append((row, col))
        self.grid[row][col] = self.current_color
        self.update_cell_style(row, col)
    
    def mouse_move_event(self, event):
        if event.buttons() & Qt.LeftButton:
            pos_in_dialog = self.mapFromGlobal(event.globalPos())
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if self.grid_labels[row][col].geometry().contains(pos_in_dialog):
                        self.paint_cell(row, col)
                        return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos_in_dialog = self.mapFromGlobal(event.globalPos())
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if self.grid_labels[row][col].geometry().contains(pos_in_dialog):
                        self.paint_cell(row, col)
                        return
    
    def mouseReleaseEvent(self, event):
        if self.current_stroke:
            self.undo_stack[-1].extend(self.current_stroke)
            self.current_stroke = []
    
    def save_grid(self):
        name, ok = QInputDialog.getText(self, 'Save Grid', 'Enter a name for this favorite:')
        if ok and name:
            self.favorites_list.addItem(name)
            settings = QSettings("MyCompany", self.FAVORITES_KEY)
            settings.setValue(name, self.grid)
            self.save_favorites()

    def load_grid(self):
        current_item = self.favorites_list.currentItem()
        if current_item:
            name = current_item.text()
            settings = QSettings("MyCompany", self.FAVORITES_KEY)
            loaded_grid = settings.value(name)
            if loaded_grid:
                self.grid = loaded_grid
                for row in range(self.grid_size):
                    for col in range(self.grid_size):
                        self.update_cell_style(row, col)
            else:
                QMessageBox.warning(self, 'Load Grid', f'Grid "{name}" not found.')
    
    def clear_grid(self):
        self.undo_stack.append(copy.deepcopy(self.grid))
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.grid[row][col] = QColor(255, 255, 255)
                self.update_cell_style(row, col)
        self.undo_stack[-1].append(None)
    
    def undo(self):
        if self.undo_stack:
            stroke_to_undo = self.undo_stack.pop()
            if stroke_to_undo and stroke_to_undo[-1] is None:
                stroke_to_undo.pop()
                self.grid = copy.deepcopy(stroke_to_undo)
                for row in range(self.grid_size):
                    for col in range(self.grid_size):
                        self.update_cell_style(row, col)
            else:
                for row, col in stroke_to_undo:
                    self.grid[row][col] = QColor(255, 255, 255)
                    self.update_cell_style(row, col)
    
    def send_grid(self):
        commands = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = self.grid[row][col]
                if color != QColor(255, 255, 255):
                    command = f"{col}-{row}-{color.red()}-{color.green()}-{color.blue()}"
                    commands.append(command)
        if commands:
            self.send_command_to_device(commands)
        else:
            QMessageBox.warning(self, 'Send Grid', 'No pixels to send.')

    def send_command_to_device(self, commands):
        command_array = ["--address", self.mac_address]
        for command in commands:
            command_array.extend(["--pixel-color", command])
        self.run_command(command_array)
        
    def send_clear_command_to_device(self, commands):
        command_array = ["--address", self.mac_address]
        self.run_command(command_array)

    def run_command(self, command_array):
        process = QProcess(self)
        process.start("cmd.exe", ["/c", "py", "app.py"] + command_array)
        process.waitForFinished()

    def clear_device(self):
        rgb_str = "0-0-0"
        self.send_clear_command_to_device(["--fullscreen-color", rgb_str.replace('#', '')])

    def update_cell_style(self, row, col):
        color = self.grid[row][col]
        border_style = "border: 1px solid black;" if color == QColor(255, 255, 255) else ""
        self.grid_labels[row][col].setStyleSheet(f"background-color: {color.name()}; {border_style}")
    
    def load_favorites(self):
        settings = QSettings("MyCompany", self.FAVORITES_KEY)
        favorite_names = settings.value("favoriteNames", [])
        for name in favorite_names:
            self.favorites_list.addItem(name)

    def save_favorites(self):
        settings = QSettings("MyCompany", self.FAVORITES_KEY)
        favorite_names = [self.favorites_list.item(i).text() for i in range(self.favorites_list.count())]
        settings.setValue("favoriteNames", favorite_names)
        
    def show_favorites_context_menu(self, pos):
        item = self.favorites_list.itemAt(pos)
        if item:
            menu = QMenu(self)
            load_action = menu.addAction("Load")
            delete_action = menu.addAction("Delete")
            action = menu.exec_(self.favorites_list.mapToGlobal(pos))
            if action == load_action:
                self.load_grid()
            elif action == delete_action:
                self.delete_favorite(item)

    def delete_favorite(self, item):
        name = item.text()
        settings = QSettings("MyCompany", self.FAVORITES_KEY)
        settings.remove(name)
        self.favorites_list.takeItem(self.favorites_list.row(item))
        self.save_favorites()

class ScoreboardDialog(QDialog):
    def __init__(self, device_page):
        super().__init__()
        self.device_page = device_page
        self.left_score = 0
        self.right_score = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Scoreboard")
        self.setWindowIcon(QIcon('gui/idmc.ico')) # Set title bar icon
        self.setFixedSize(300, 200)
        layout = QGridLayout()

        # Score Labels (Centered)
        self.left_score_label = QLabel(str(self.left_score))
        self.left_score_label.setAlignment(Qt.AlignCenter)  # Center the label horizontally
        self.left_score_label.setFont(QFont("Arial", 36, QFont.Bold))
        layout.addWidget(self.left_score_label, 1, 0)

        self.right_score_label = QLabel(str(self.right_score))
        self.right_score_label.setAlignment(Qt.AlignCenter)  # Center the label horizontally
        self.right_score_label.setFont(QFont("Arial", 36, QFont.Bold))
        layout.addWidget(self.right_score_label, 1, 1)  # Changed column to 1 for centering

        # Increment Buttons (Above)
        left_inc_button = QPushButton("+1")
        left_inc_button.clicked.connect(lambda: self.adjust_score(True, True))  # True for left, True for increment
        layout.addWidget(left_inc_button, 0, 0)  # Row 0 for above

        right_inc_button = QPushButton("+1")
        right_inc_button.clicked.connect(lambda: self.adjust_score(False, True))  # False for right, True for increment
        layout.addWidget(right_inc_button, 0, 1)  # Row 0 for above

        # Decrement Buttons (Below)
        left_dec_button = QPushButton("-1")
        left_dec_button.clicked.connect(lambda: self.adjust_score(True, False))  # True for left, False for decrement
        layout.addWidget(left_dec_button, 2, 0)  # Row 2 for below

        right_dec_button = QPushButton("-1")
        right_dec_button.clicked.connect(lambda: self.adjust_score(False, False))  # False for right, False for decrement
        layout.addWidget(right_dec_button, 2, 1)  # Row 2 for below

        self.setLayout(layout)

    def adjust_score(self, is_left, is_inc):
        if is_left:
            if is_inc or self.left_score > 0:  # Increment only if score is above 0 or we are incrementing
                self.left_score += 1 if is_inc else -1
                self.left_score_label.setText(str(self.left_score))
        else:
            if is_inc or self.right_score > 0:  # Increment only if score is above 0 or we are incrementing
                self.right_score += 1 if is_inc else -1
                self.right_score_label.setText(str(self.right_score))

        self.send_score()

    def send_score(self):
        score_str = f"{self.left_score}-{self.right_score}"
        self.device_page.run_command(["--address", self.device_page.mac_address, "--scoreboard", score_str])
        
# --- Main App Classes ---
class DevicePage(QWidget):
   
    # --- UI  Setup ---
    def __init__(self, main_window, friendly_name, device_name, mac_address):
        super().__init__()
        self.main_window = main_window
        self.friendly_name = friendly_name
        self.device_name = device_name
        self.mac_address = mac_address
        self.first_output_received = False
        self.last_command = None
        self.clock_styles = ['Default', 'Christmas', 'Racing', 'Inverted Full Screen',
                             'Animated Hourglass', 'Frame 1', 'Frame 2', 'Frame 3']
        self.init_ui()
        self.flip_screen_state = False

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(self.delete_device)
        header_layout.addWidget(delete_button, 0)

        label = QLabel(f"       {self.friendly_name}         MAC: {self.mac_address}", self)
        label.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(label, 1)

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.go_back_to_homepage)
        header_layout.addWidget(back_button, 0)
        layout.addLayout(header_layout)

        # Grid layout for buttons
        grid_layout = QGridLayout()
        self.action_buttons = []
        actions = [
            ("Clock Style", self.clock_control),
            ("Sync Time", self.sync_time),
            ("Set Time", self.set_time),
            ("Screen On", lambda: self.screen_control("on")),
            ("Screen Off", lambda: self.screen_control("off")),
            ("Stop Watch", self.chronograph_control),
            ("Countdown Timer", lambda: self.countdown_control(1)),
            ("Set Text", self.set_text),
            ("Color Studio", self.color_control),
            ("Scoreboard", self.open_scoreboard),
            ("Set Image", self.set_image),
            ("Set GIF", self.set_gif),
            ("Set Weather", self.set_weather),
            ("Set Weather GIF", self.set_weather_gif),

            
        ]

        for index, (text, func) in enumerate(actions):
            button = QPushButton(text, self)
            button.clicked.connect(func)
            grid_layout.addWidget(button, index // 5, index % 5)
            self.action_buttons.append(button)

        layout.addLayout(grid_layout)
        
        console_widget = QWidget()
        console_layout = QVBoxLayout(console_widget)
        console_label = QLabel("Console:")
        console_label.setFont(QFont("Arial", 12, QFont.Bold))
        console_layout.addWidget(console_label)
        self.console_output = QPlainTextEdit(self)
        self.console_output.setReadOnly(True)
        console_layout.addWidget(self.console_output)
        layout.addWidget(console_widget)

        self.setLayout(layout)
   
    # --- Helpers ---
    def go_back_to_homepage(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.homepage)

    def run_command(self, args):
            self.console_output.clear()
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyRead.connect(self.handle_ready_read)
            self.process.finished.connect(self.process_finished)
            self.process.start("cmd.exe", ["/c", "py", "app.py"] + args)

    def handle_ready_read(self):
        data = self.process.readAll()
        stdout = bytes(data).decode("utf8").strip()
       
        current_command = self.process.arguments()[2:]
        output_lines = stdout.splitlines()
       
        if output_lines:
            first_line = output_lines[0]
            rest_of_output = '\n'.join(output_lines[1:])
           
            if self.last_command != current_command:
                self.console_output.appendPlainText(f"Command: {' '.join(current_command)}\n")
                self.last_command = current_command
           
            self.console_output.appendPlainText(f"Output: {first_line}\n")
           
            if rest_of_output:
                self.console_output.appendPlainText(rest_of_output + '\n')
        else:
            self.console_output.appendPlainText(f"Command: {' '.join(current_command)}\nOutput:\n")
       
        self.last_command = current_command
   
    def process_finished(self):
        pass
   
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            return tuple(int(hex_color[i]*2, 16) for i in range(3))
        else:
            raise ValueError("Invalid hex color format")
   
    def handle_color_control_accepted(self, color_name):
        rgb_str = color_name.replace('#', '')
        self.run_command(["--address", self.mac_address, "--fullscreen-color", rgb_str])
   
    
    # --- Device Button Actions ---
    def delete_device(self):
        confirmation = QMessageBox.question(self, "Delete Device", f"Are you sure you want to delete {self.friendly_name}?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            for i in range(self.main_window.configuration_page.device_list.count()):
                item = self.main_window.configuration_page.device_list.item(i)
                if item.toolTip() == self.mac_address:
                    self.main_window.configuration_page.device_list.takeItem(i)
                    break
                
            button_to_remove = self.main_window.device_buttons.pop(self.mac_address, None)
            if button_to_remove:
                self.main_window.homepage_layout.removeWidget(button_to_remove)
                button_to_remove.deleteLater()

            del self.main_window.device_pages[self.mac_address]
            self.main_window.save_device_settings()
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.homepage)

    def clock_control(self):
            dialog = ClockStyleDialog(self)
            clock_style, show_date, show_24hr, color, ok_pressed = dialog.get_options()

            if ok_pressed:
                args = ["--address", self.mac_address, "--clock", str(self.clock_styles.index(clock_style)), "--sync-time"]
                if show_date:
                    args.append("--clock-with-date")
                if show_24hr:
                    args.append("--clock-24h")
                if color:
                    rgb_str = f"{color.red()}-{color.green()}-{color.blue()}"
                    args.append(f"--clock-color={rgb_str}")  
                self.run_command(args)

    def sync_time(self):
        self.run_command(["--address", self.mac_address, "--sync-time"])

    def set_time(self):
        time, ok_pressed = QInputDialog.getText(self, "Set Time", "Enter the time (DD-MM-YYYY-HH:MM:SS):")
        if ok_pressed:
            self.run_command(["--address", self.mac_address, "--set-time", time])
    pass
    def set_weather(self):
        city, ok_pressed = QInputDialog.getText(self, "Set Weather", "Enter the city:")

        if ok_pressed and city:  # Check if there is a city
            def get_current_data(city):
                url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={api_key}"
                response = requests.get(url)
                data = response.json()
                if response.status_code == 200:
                    return data
                else:
                    raise ValueError("It could not get the info")

            def draw_digit(draw, x_offset, y_offset, digit):
                pattern = digits[digit]
                for y, row in enumerate(pattern):
                    for x, pixel in enumerate(row):
                        if pixel == "1":
                            draw.point((x + x_offset, y + y_offset), fill="white")

            def draw_colored_pattern(draw, x_offset, y_offset, key):
                if key not in patterns:
                    raise ValueError(f"The pattern '{key}' is not defined.")
                pattern = patterns[key]
                for y, row in enumerate(pattern):
                    for x, pixel in enumerate(row):
                        if pixel in colors:
                            draw.point((x + x_offset, y + y_offset), fill=colors[pixel])

            def get_weather_category(condition_code,is_day):
                weather_switch = {
                    "sun": [1000],
                    "partly cloudy": [1003],
                    "cloudy": [1006, 1009],
                    "fog": [1030, 1135, 1147],
                    "raining": [
                    1063, 1150, 1153, 1180, 1183, 1186, 1189, 1192, 1195, 1240,
                    1243, 1246, 1273, 1276
                    ],
                    "snowing": [
                    1066, 1114, 1117, 1168, 1171, 1204, 1207, 1210, 1213, 1216,
                    1219, 1222, 1225, 1255, 1258, 1279, 1282
                    ],
                    "thundering": [1087, 1273, 1276, 1279, 1282],
                    "windy": [1114, 1117]
                }
                if is_day == 0:
                # If it is night , we change the category
                    weather_switch["moon"] = weather_switch.pop("sun", [1000])
                    weather_switch["partly cloudy night"] = weather_switch.pop("partly cloudy", [1003])

               

                for category, codes in weather_switch.items():
                    if condition_code in codes:
                        return category
                return "unknown"

        # OGet weather data
            data_api = get_current_data(city)

            current_weather_code = data_api["current"]["condition"]["code"]
            is_day = data_api["current"]["is_day"]
            
            weather_category = get_weather_category(current_weather_code,is_day)
            

            temperature_celsius = int(round(data_api["current"]["temp_c"])) 
            
        # Do pixel img
            img = Image.new('RGB', (16, 16), color='black')
            draw = ImageDraw.Draw(img)

        # Extract the celsius digits
            first_digit = str(temperature_celsius).zfill(2)[0]
            second_digit = str(temperature_celsius).zfill(2)[1]

        # Draw temperature and weather
            draw_digit(draw, 3, 8, first_digit)
            draw_digit(draw, 9, 8, second_digit)
            draw_colored_pattern(draw, 4, 0, weather_category)

        # Save the img
            file_path = "weather.png"
            img.save(file_path)

        # Run the command with the new img
            self.run_command([
            "--address", self.mac_address,
            "--image", "true",
            "--set-image", file_path,
            "--process-image", str(16)
        ])

    pass
    def set_weather_gif(self):
        
        city, ok_pressed = QInputDialog.getText(self, "Set Weather", "Enter the city:")

        if ok_pressed and city:
            def get_current_data(city):
                #2 days, just in case the actual hour +6 is the next day
                url = f"https://api.weatherapi.com/v1/forecast.json?q={city}&days=2&key={api_key}"
                response = requests.get(url)
                data = response.json()
                if response.status_code == 200:
                    return data
                else:
                    raise ValueError("It could not get the info")
                
            def draw_digit(draw, x_offset, y_offset, digit):
                pattern = digits[digit]
                for y, row in enumerate(pattern):
                    for x, pixel in enumerate(row):
                        if pixel == "1":
                            draw.point((x + x_offset, y + y_offset), fill=(255,255,255))
            def draw_colored_pattern(draw, x_offset, y_offset, key):
                if key not in patterns:
                    raise ValueError(f"The pattern '{key}' is not defined.")
                pattern = patterns[key]
                for y, row in enumerate(pattern):
                    for x, pixel in enumerate(row):
                        if pixel in colors:
                            draw.point((x + x_offset, y + y_offset), fill=colors[pixel])
            
            def get_weather_category(condition_code,is_day):
                weather_switch = {
                    "sun": [1000],
                    "partly cloudy": [1003],
                    "cloudy": [1006, 1009],
                    "fog": [1030, 1135, 1147],
                    "raining": [
                    1063, 1150, 1153, 1180, 1183, 1186, 1189, 1192, 1195, 1240,
                    1243, 1246, 1273, 1276
                    ],
                    "snowing": [
                    1066, 1114, 1117, 1168, 1171, 1204, 1207, 1210, 1213, 1216,
                    1219, 1222, 1225, 1255, 1258, 1279, 1282
                    ],
                    "thundering": [1087, 1273, 1276, 1279, 1282],
                    "windy": [1114, 1117]
                }
                if is_day == 0:
                # If it is night , we change the category
                    weather_switch["moon"] = weather_switch.pop("sun", [1000])
                    weather_switch["partly cloudy night"] = weather_switch.pop("partly cloudy", [1003])

                for category, codes in weather_switch.items():
                    if condition_code in codes:
                        return category
                return "unknown"

            data_api = get_current_data(city)
            current_hour = int(data_api["location"]["localtime"].split()[1].split(":")[0])
            
            hourly_forecast = data_api["forecast"]["forecastday"][0]["hour"]
            #Array for all the images
            images=[]
            #range must be max 6 because specs
            for i in range(6):
                #Checking if the next hour is in the same day or next
                hour_index = (current_hour + i) % 24
                if current_hour + i < 24:  # Same day
                    hour_data = data_api["forecast"]["forecastday"][0]["hour"][hour_index]
                else:  # Next day
                    hour_data = data_api["forecast"]["forecastday"][1]["hour"][hour_index]

                condition_code = hour_data["condition"]["code"]
                is_day = hour_data["is_day"]
                
                #Celsius temperature
                temperature_celsius = int(round(hour_data["temp_c"]))

                weather_category = get_weather_category(condition_code, is_day)
                
                # Create the pixel image
                img = Image.new('RGB', (16, 16), color=1)
                draw = ImageDraw.Draw(img)

                # Extract the Celsius digits
                first_digit = str(temperature_celsius).zfill(2)[0]
                second_digit = str(temperature_celsius).zfill(2)[1]
                # Determine the digit color (red for the first image, white for others)
                
                draw.rectangle([0, 15, i, 15], fill=(255, 255, 255))  #horizontal line to draw the hour, each point is the index of the hour

                draw_digit(draw, 3, 8, first_digit)
                draw_digit(draw, 9, 8, second_digit)
                draw_colored_pattern(draw, 4, 0, weather_category)
                
                # Save the gif with a unique name
                if img.getbbox():
                    images.append(img)
                else:
                    print(f"IMG {i} is empty, it will not be added")

            # Run the command with the new image
            
            images_array = [numpy.array(img) for img in images]

            gif_path = "weather_forecast.gif"

            images[0].save(gif_path, save_all=True, append_images=images[1:], duration=[1000, 1000, 1000, 1000, 1000, 1000], loop=0)
            self.run_command(["--address", self.mac_address, "--set-gif", gif_path, "--process-gif", str(16)])


    def screen_control(self, state):
        self.run_command(["--address", self.mac_address, "--screen", state])

    def chronograph_control(self):
            options = ['Reset', '(Re)Start', 'Pause', 'Continue after Pause']
            default_index = 1
            option, ok_pressed = QInputDialog.getItem(self, "Stop Watch", "Select an option:", options, default_index, False)                            
            if ok_pressed:
                self.run_command(["--address", self.mac_address, "--chronograph", str(options.index(option))])
               
    def countdown_control(self, state):
        options = ['Disable', 'Start', 'Pause', 'Restart']
        option, ok_pressed = QInputDialog.getItem(self, "Countdown Control",
                                                "Select an option:", options, 0, False)
        if ok_pressed and option == 'Start':
            time, ok_pressed = QInputDialog.getText(self, "Set Time", "Enter the Countdown time:\n\n(eg: 5min. 30sec. = 5-30)")
        else:
            time = None

        if ok_pressed:
            command_args = ["--address", self.mac_address, "--countdown", str(options.index(option))]
            if time is not None:
                command_args.extend(["--countdown-time", time])

            self.run_command(command_args)
        else:
            print("Countdown canceled, no command will be executed.")

    def set_text(self):
        dialog = TextStyleDialog(self)
        settings = dialog.get_settings()
        if settings is not None:
            text, text_size, text_mode, text_speed, text_color_mode_index, text_color, text_bg_mode_index, text_bg_color = settings
           
            text_mode = str(text_mode)
            text_color_mode = str(text_color_mode_index)
            text_bg_mode = str(text_bg_mode_index)

            args = ["--address", self.mac_address, "--set-text", text, "--text-size", str(text_size), "--text-mode", text_mode, "--text-speed", str(text_speed), "--text-color-mode", text_color_mode]  
           
            if text_color:
                rgb_text = f"{text_color.red()}-{text_color.green()}-{text_color.blue()}"
                args.append(f"--text-color={rgb_text}")
            if text_bg_color:
                rgb_bg = f"{text_bg_color.red()}-{text_bg_color.green()}-{text_bg_color.blue()}"
                args.append(f"--text-bg-color={rgb_bg}")
            if text_bg_mode != "None":  
                args.append(f"--text-bg-mode={text_bg_mode}")  
           
            self.run_command(args)
        else:
            print("No text settings were provided.")

    def color_control(self):
        dialog = ColorControlDialog(self, self.mac_address)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_color:
            r, g, b = dialog.selected_color.red(), dialog.selected_color.green(), dialog.selected_color.blue()
            rgb_str = f"{r}-{g}-{b}"

            self.run_command(["--address", self.mac_address, "--fullscreen-color", rgb_str])

    def open_scoreboard(self):
        dialog = ScoreboardDialog(self)
        dialog.exec_()

    def set_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "PNG Files (*.png);;All Files (*)", options=options)

        if file_path:
            # Image Size Selection Dialog
            size_dialog = QDialog(self)
            size_dialog.setWindowTitle("Pick Size")
            layout = QVBoxLayout()
            size_combo = QComboBox()
            size_combo.addItems(["16x16", "32x32"])
            layout.addWidget(size_combo)
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(size_dialog.accept)
            button_box.rejected.connect(size_dialog.reject)
            layout.addWidget(button_box)
            size_dialog.setLayout(layout)

            if size_dialog.exec_() == QDialog.Accepted:
                image_size = size_combo.currentText().split("x")[0]
                self.run_command(["--address", self.mac_address, "--image", "true", "--set-image", file_path, "--process-image", image_size])

    def set_gif(self):
        confirmation = QMessageBox.question(self, "GIF Notice", "All GIFs are processed by default to ensure maximum compatibility. \n\nThis doesn't always work for all GIFs. \n\nGIFs closer to 32x32 or 16x16 have better chances of working.",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(self, "Select GIF", "", "GIF Files (*.gif);;All Files (*)", options=options)

            if file_path:
                size_dialog = QDialog(self)
                size_dialog.setWindowTitle("Choose GIF Size")
                layout = QVBoxLayout()
                size_combo = QComboBox()
                size_combo.addItems(["16x16", "32x32"])
                layout.addWidget(size_combo)
                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(size_dialog.accept)
                button_box.rejected.connect(size_dialog.reject)
                layout.addWidget(button_box)
                size_dialog.setLayout(layout)

                if size_dialog.exec_() == QDialog.Accepted:
                    image_size = size_combo.currentText().split("x")[0]
                    self.run_command(["--address", self.mac_address, "--set-gif", file_path, "--process-gif", image_size])

class ConfigurationPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.device_name = ""

        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()

        console_label = QLabel("Console:")  
        console_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.left_layout.addWidget(console_label)

        self.console_output = QPlainTextEdit(self)
        self.console_output.setReadOnly(True)
        self.left_layout.addWidget(self.console_output)

        instruction_label = QLabel('Select a device from the list to add:')
        instruction_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.left_layout.addWidget(instruction_label)

        self.device_list = QListWidget()
        self.device_list.itemClicked.connect(self.device_selected)
        self.left_layout.addWidget(self.device_list)

        self.layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
       
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.go_back_to_homepage)
        back_button.setFixedSize(150, 50)
        self.right_layout.addWidget(back_button)
       
        add_selected_device_button = QPushButton('Add Selected Device')
        add_selected_device_button.clicked.connect(self.add_selected_device)
        add_selected_device_button.setFixedSize(150, 50)
        self.right_layout.addWidget(add_selected_device_button)

        self.layout.addLayout(self.right_layout)
        self.setLayout(self.layout)

    def device_selected(self, item):
        self.selected_device = item.text()

    def add_selected_device(self):
        if hasattr(self, 'selected_device'):
            if self.selected_device in self.main_window.device_buttons:
                QMessageBox.warning(self, 'Device Already Added', f'Device "{self.selected_device}" is already added to the homepage.')
                return

            dialog = CustomInputDialog(self)
            friendly_name, ok = dialog.get_input()
            if ok and friendly_name:
                mac_address = self.device_list.currentItem().toolTip()
            else:
                mac_address = self.device_list.currentItem().toolTip()
                friendly_name = self.selected_device

            self.main_window.add_device_to_homepage(friendly_name, mac_address)
            QMessageBox.information(self, 'Device Added', f'Device "{friendly_name}" has been added.')
            self.main_window.save_device_settings()
        else:
            QMessageBox.warning(self, 'No Device Selected', 'Please select a device from the list.')

    def go_back_to_homepage(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.homepage)

    def update_device_name(self, new_name):
        self.device_name = new_name
       
    def save_device_name(self):
        self.main_window.save_device_settings()
   
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iDotMatrix Controller')
        self.setWindowIcon(QIcon('gui/idmc.ico'))

        screen_geometry = QApplication.desktop().availableGeometry()
        self.screen_center = screen_geometry.center()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        header_font = QFont("Arial", 18, QFont.Bold)
        header_label = QLabel('iDotMatrix Controller')
        header_label.setFont(header_font)
        self.layout.addWidget(header_label)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.homepage = QWidget()
        self.homepage_layout = QVBoxLayout()
        self.homepage_layout.setAlignment(Qt.AlignCenter)

        add_device_button = QPushButton('Add Device')
        add_device_button.setFixedSize(150, 50)
        add_device_button.clicked.connect(self.show_configuration_page)
        self.homepage_layout.addWidget(add_device_button)

        self.homepage.setLayout(self.homepage_layout)
        self.stacked_widget.addWidget(self.homepage)

        self.configuration_page = ConfigurationPage(self)
        self.stacked_widget.addWidget(self.configuration_page)

        self.setLayout(self.layout)
        self.resize(800, 600)
        self.center_window()

        self.device_pages = {}

        self.device_buttons = {}  
        self.load_device_settings()
       
        self.connect_device_buttons()

    def center_window(self):
        window_size = self.frameGeometry().size()
        x = self.screen_center.x() - window_size.width() // 2
        y = self.screen_center.y() - window_size.height() // 2
        self.move(x, y)

    def show_configuration_page(self):
        self.stacked_widget.setCurrentWidget(self.configuration_page)
        self.scan_for_devices()

    def scan_for_devices(self):
        self.configuration_page.console_output.clear()
        self.output_str = ""
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.handle_ready_read)
        self.process.finished.connect(self.process_finished)
        self.process.start("cmd.exe", ["/c", "py app.py --scan"])

    def handle_ready_read(self):
        data = self.process.readAll()
        stdout = bytes(data).decode("utf8")
        self.output_str += stdout
        self.configuration_page.console_output.appendPlainText(stdout)

        device_name_pattern = re.compile(r"found device ([\dA-F:]+) with name (\S+)")
        matches = device_name_pattern.findall(stdout)
        if matches:
            self.configuration_page.device_list.clear()
            for mac_address, device_name in matches:
                item = QListWidgetItem(device_name)
                self.configuration_page.device_list.addItem(item)
                item.setToolTip(mac_address)

    def process_finished(self):
        pass

    def add_device_to_homepage(self, friendly_name, mac_address):
        if mac_address not in self.device_buttons:
            device_button = QPushButton(friendly_name)
            device_button.setToolTip(mac_address)
            device_button.setFixedSize(150, 50)
            self.homepage_layout.addWidget(device_button)
            self.device_buttons[mac_address] = device_button
        else:
            QMessageBox.warning(self, 'Device Already Added', f'Device with MAC address "{mac_address}" is already added to the homepage.')
        device_button.clicked.connect(self.show_device_page)

    def save_device_settings(self):
        settings = QSettings("MyCompany", "iDotMatrixController")
        devices = [(mac_address, button.text()) for mac_address, button in self.device_buttons.items()]
        settings.setValue("devices", devices)
        settings.setValue("device_name", self.configuration_page.device_name)

    def load_device_settings(self):
        settings = QSettings("MyCompany", "iDotMatrixController")
        devices = settings.value("devices", [])
        for device in devices:
            if len(device) == 2:
                mac_address, friendly_name = device
                self.add_device_to_homepage(friendly_name, mac_address)
                self.configuration_page.device_name = settings.value("device_name", "")

    def connect_device_buttons(self):
        for mac_address, button in self.device_buttons.items():
            button.clicked.connect(self.show_device_page)

    def show_device_page(self):
        sender = self.sender()
        if sender:
            mac_address = sender.toolTip()
           
            if mac_address in self.device_pages:
                device_page = self.device_pages[mac_address]
            else:
                device_name = None
                for i in range(self.configuration_page.device_list.count()):
                    item = self.configuration_page.device_list.item(i)
                    if item.toolTip() == mac_address:
                        device_name = item.text()
                        break
               
                friendly_name = sender.text()
                device_page = DevicePage(self, friendly_name, device_name, mac_address)
                self.device_pages[mac_address] = device_page
                self.stacked_widget.addWidget(device_page)

            self.stacked_widget.setCurrentWidget(device_page)
   
    def show_device_page(self):
        sender = self.sender()
        if sender:
            mac_address = sender.toolTip()
            if mac_address in self.device_pages:
                device_page = self.device_pages[mac_address]
            else:
                device_name = None
                for i in range(self.configuration_page.device_list.count()):
                    item = self.configuration_page.device_list.item(i)
                    if item.toolTip() == mac_address:
                        device_name = item.text()
                        break

                friendly_name = sender.text()
                device_page = DevicePage(self, friendly_name, device_name, mac_address)
                self.device_pages[mac_address] = device_page
                self.stacked_widget.addWidget(device_page)

            self.stacked_widget.setCurrentWidget(device_page)

    def open_pixel_paint_dialog(self, mac_address):
        dialog = PixelPaintDialog(mac_address)
        dialog.exec_()
        
# --- Main Execution ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())