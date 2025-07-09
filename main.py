
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.clock import Clock
from plyer import filechooser
import sqlite3
import os
import mimetypes
import traceback
import platform

# Determine storage path (Android or desktop)
if platform.system() == "Linux" and "ANDROID_ARGUMENT" in os.environ:
    from android.storage import app_storage_path
    STORAGE_PATH = app_storage_path()
else:
    STORAGE_PATH = os.getcwd()

class ImageUploadMDApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_display = Image(size_hint_y=1)
        self.selected_file = None
        self.status_label = MDLabel(text="", size_hint_y=None, height=30)
        self.db_path = os.path.join(STORAGE_PATH, "kivydata.db")

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        # Select Image Button
        select_button = MDRaisedButton(
            text="Select Image",
            size_hint_y=None,
            height=50,
            pos_hint={"center_x": 0.5}
        )
        select_button.bind(on_press=self.select_image)
        layout.add_widget(select_button)

        # Upload Image Button
        self.upload_button = MDRaisedButton(
            text="Upload Image",
            size_hint_y=None,
            height=50,
            disabled=True,
            pos_hint={"center_x": 0.5}
        )
        self.upload_button.bind(on_press=self.upload_image)
        layout.add_widget(self.upload_button)

        # Status Label
        layout.add_widget(self.status_label)

        # Image Display
        layout.add_widget(self.image_display)

        self.init_database()
        return layout

    def init_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.ensure_table_exists(self.conn, self.cursor)
            print(f"Database initialized at {self.db_path}")
        except Exception as e:
            print(f"Database error: {e}")
            traceback.print_exc()
            self.status_label.text = "Database error"

    def ensure_table_exists(self, conn, cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS images 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, gambar BLOB)''')
        conn.commit()

    def select_image(self, instance):
        filechooser.open_file(
            filters=[("Image files", "*.png", "*.jpg", "*.jpeg")],
            on_selection=self.on_file_selected
        )

    def on_file_selected(self, selection):
        if selection:
            self.selected_file = selection[0]
            self.upload_button.disabled = False
            self.status_label.text = f"Selected: {os.path.basename(self.selected_file)}"

    def upload_image(self, instance):
        if self.selected_file:
            self.status_label.text = "Uploading..."
            Clock.schedule_once(lambda dt: self.process_upload(), 0)

    def process_upload(self):
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()

            # Insert image into DB
            with open(self.selected_file, "rb") as image_file:
                binary_data = sqlite3.Binary(image_file.read())
            cursor.execute("INSERT INTO images (gambar) VALUES (?)", (binary_data,))
            conn.commit()

            # Get last image inserted
            cursor.execute("SELECT id FROM images ORDER BY id DESC LIMIT 1")
            last_id = cursor.fetchone()[0]

            cursor.execute("SELECT gambar FROM images WHERE id = ?", (last_id,))
            gambar = cursor.fetchone()[0]

            mime_type, _ = mimetypes.guess_type(self.selected_file)
            image_type = mime_type.split('/')[-1] if mime_type else 'jpg'
            temp_path = os.path.join(STORAGE_PATH, f"temp_image_{last_id}.{image_type}")

            with open(temp_path, "wb") as temp_file:
                temp_file.write(gambar)

            self.image_display.source = temp_path
            self.image_display.reload()
            self.status_label.text = "Upload successful!"

        except Exception as e:
            print(f"Upload failed: {e}")
            traceback.print_exc()
            self.status_label.text = "Upload failed"
        finally:
            cursor.close()
            conn.close()

    def on_stop(self):
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    ImageUploadMDApp().run()
