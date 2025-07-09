
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

class MainLayout(MDBoxLayout):
    pass

class ImageUploadMDApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_display = Image(size_hint_y=1)
        self.selected_file = None
        self.status_label = MDLabel(text="", size_hint_y=None, height=30)
        self.db_path = os.path.join(os.getcwd(), "kivydata.db")

    def build(self):
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
        except sqlite3.Error as e:
            print(f"Failed to connect to database: {e}")
            self.status_label.text = f"Database connection failed: {e}"

    def ensure_table_exists(self, conn, cursor):
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS images 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, gambar BLOB)''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Failed to create table: {e}")
            raise

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
            try:
                self.ensure_table_exists(conn, cursor)
                cursor.execute("BEGIN TRANSACTION")
                with open(self.selected_file, "rb") as image_file:
                    binary_data = sqlite3.Binary(image_file.read())
                
                cursor.execute("INSERT INTO images (gambar) VALUES (?)", (binary_data,))
                conn.commit()

                cursor.execute("SELECT id FROM images ORDER BY id DESC LIMIT 1")
                last_id = cursor.fetchone()[0]

                # Retrieve and display the last image
                display_cursor = conn.cursor()
                display_cursor.execute("SELECT gambar FROM images WHERE id = ?", (last_id,))
                gambar = display_cursor.fetchone()[0]
                mime_type, _ = mimetypes.guess_type(self.selected_file)
                image_type = mime_type.split('/')[-1] if mime_type else 'jpg'
                temp_path = os.path.join(os.getcwd(), f"temp_image_{last_id}.{image_type}")
                with open(temp_path, "wb") as temp_file:
                    temp_file.write(gambar)

                self.image_display.source = temp_path
                self.image_display.reload()
                self.status_label.text = "Upload successful!"

                # Optional cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            except sqlite3.OperationalError as e:
                conn.rollback()
                print(f"Database error: {e}")
                self.status_label.text = f"Upload failed: {e}"
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"Upload failed: {e}")
            self.status_label.text = f"Upload failed: {e}"

    def on_stop(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == '__main__':
    ImageUploadMDApp().run()
