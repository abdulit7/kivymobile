# import flet as ft
# import sqlite3
# import base64
# import os

# # CONNECT TO YOU DATABASE FILE SQLITE 
# conn = sqlite3.connect("database.db",check_same_thread=False)
# cursor = conn.cursor()


# def main(page:ft.Page):
# 	page.scroll = "auto"
# 	youdata = ft.Column()
# 	txtname = ft.TextField(label="you name here")


# 	def uploadnow(e:ft.FilePickerResultEvent):
# 		# IF THERE FILE 
# 		if not e.files == "":
# 			for x in e.files:
# 				try:
# 					with open(x.path,"rb") as image_file:
# 						convertImgToString = base64.b64encode(image_file.read()).decode()
# 						# THEN INSERT TO TABLE 
# 						cursor.execute("INSERT INTO images (name,gambar) VALUES (?,?) ",(txtname.value,convertImgToString))
# 						conn.commit()
# 						print("You SUccess uploading file guys !!!!!")
# 						page.update()
# 				except Exception as e:
# 					print(e)
# 					print("YOU HAVE PROBLEM HERE !!!!")
# 				page.update()


# 	# AFTER THAT , I WANT LOAD DATA WHEN APP ONECE LOADED
# 	# LIKE LIFECYCLE 
# 	cursor.execute("select * from images")
# 	data = cursor.fetchall()

# 	sample = []
# 	# IF DATA FOUND FROM YOU TABLE SQLITE THEN PUSH TO COLUMN WIDGET
# 	if not len(data) == 0:
# 		for x in data :
# 			sample.append({"id":x[0],"nama":x[1],"gambar":x[2]})
# 			for p in sample:
# 				youdata.controls.append(
# 					ft.Container(
# 					content=ft.Column([
# 						ft.Text(f"{p['nama']}",size=30),
# 						ft.Image(
# 						src_base64=p['gambar'],
# 						width=300,
# 						height=200,
# 						fit="cover"

# 							)

# 						])

# 						)

# 					)



# 	file_picker = ft.FilePicker(
# 		on_result=uploadnow

# 		)
# 	page.overlay.append(file_picker)
# 	page.add(
# 		ft.Column([
# 		ft.Text("SQLITE UPLOAD IMAGE BLOB",size=30),
# 		txtname,
# 		ft.FilledButton("upload now ",
# 		on_click=lambda e:file_picker.pick_files()
# 		),
# 		youdata 


# 			])
# 		)


# ft.app(target=main)

# import flet as ft
# import sqlite3
# import base64
# import os
# import shutil

# # CONNECT TO YOUR DATABASE FILE SQLITE
# conn = sqlite3.connect("database.db", check_same_thread=False)
# cursor = conn.cursor()

# # CREATE TABLE IF NOT EXISTS
# cursor.execute('''CREATE TABLE IF NOT EXISTS images 
#                   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, gambar BLOB)''')
# conn.commit()

# def main(page: ft.Page):
#     page.scroll = "auto"
#     youdata = ft.Column()
#     txtname = ft.TextField(label="Your name here")
#     txtid = ft.TextField(label="Image ID to update (leave blank to insert)", keyboard_type="number")

#     def uploadnow(e: ft.FilePickerResultEvent):
#         if e.files:
#             file = e.files[0]
#             try:
#                 # Use FLET_APP_STORAGE_TEMP for Android compatibility
#                 temp_dir = os.getenv("FLET_APP_STORAGE_TEMP") or os.path.join(os.getcwd(), "temp")
#                 os.makedirs(temp_dir, exist_ok=True)
#                 temp_path = os.path.join(temp_dir, file.name)
                
#                 # Copy file to temp directory if path is inaccessible
#                 if os.path.exists(file.path):
#                     shutil.copy(file.path, temp_path)
#                 else:
#                     page.add(ft.Text(f"Direct path access failed, using upload: {file.path}"))
#                     with open(temp_path, "wb") as f:
#                         f.write(base64.b64decode(file.data.split(",")[1] if "," in file.data else file.data))  # Fallback to base64 data if available

#                 with open(temp_path, "rb") as image_file:
#                     convertImgToString = base64.b64encode(image_file.read()).decode()
                
#                 # Check if updating or inserting
#                 image_id = txtid.value.strip()
#                 if image_id:
#                     cursor.execute("UPDATE images SET name = ?, gambar = ? WHERE id = ?", (txtname.value, convertImgToString, image_id))
#                     conn.commit()
#                     print(f"Updated image with ID {image_id} successfully!")
#                 else:
#                     cursor.execute("INSERT INTO images (name, gambar) VALUES (?, ?)", (txtname.value, convertImgToString))
#                     conn.commit()
#                     print("Inserted new image successfully!")
                
#                 page.update()
#             except Exception as e:
#                 print(f"Error: {e}")
#                 page.add(ft.Text(f"Upload failed: {e}"))
#             page.update()

#     # LOAD DATA WHEN APP LOADS
#     cursor.execute("SELECT * FROM images")
#     data = cursor.fetchall()

#     sample = []
#     if data:
#         for x in data:
#             sample.append({"id": x[0], "nama": x[1], "gambar": x[2]})
#         for p in sample:
#             youdata.controls.append(
#                 ft.Container(
#                     content=ft.Column([
#                         ft.Text(f"ID: {p['id']} - {p['nama']}", size=20),
#                         ft.Image(
#                             src_base64=p['gambar'],
#                             width=300,
#                             height=200,
#                             fit="cover"
#                         )
#                     ])
#                 )
#             )

#     file_picker = ft.FilePicker(on_result=uploadnow)
#     page.overlay.append(file_picker)
#     page.add(
#         ft.Column([
#             ft.Text("SQLITE UPLOAD/UPDATE IMAGE BLOB", size=30),
#             txtid,
#             txtname,
#             ft.FilledButton("Upload/Update Image",
#                         on_click=lambda e: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"])),
#             youdata
#         ])
#     )

# ft.app(target=main)



# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.uix.label import Label
# from kivy.properties import ObjectProperty
# from kivy.clock import Clock
# from plyer import filechooser
# import sqlite3
# import base64
# import os

# class ImageUploadApp(App):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.image_display = Image()
#         self.selected_file = None
#         self.status_label = Label(text="", size_hint_y=None, height=30)

#     def build(self):
#         layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
#         # Select Image Button
#         select_button = Button(text="Select Image", size_hint_y=None, height=50)
#         select_button.bind(on_press=self.select_image)
#         layout.add_widget(select_button)

#         # Upload Image Button
#         upload_button = Button(text="Upload Image", size_hint_y=None, height=50, disabled=True)
#         upload_button.bind(on_press=self.upload_image)
#         self.upload_button = upload_button
#         layout.add_widget(upload_button)

#         # Status Label
#         layout.add_widget(self.status_label)

#         # Image Display
#         layout.add_widget(self.image_display)

#         # Initialize database (create connection only, table creation handled in upload)
#         self.init_database()
#         return layout

#     def init_database(self):
#         try:
#             self.conn = sqlite3.connect("kivydata.db", check_same_thread=False)
#             self.cursor = self.conn.cursor()
#             print("Database connection established.")
#         except sqlite3.Error as e:
#             print(f"Failed to connect to database: {e}")
#             self.status_label.text = f"Database connection failed: {e}"

#     def ensure_table_exists(self, conn, cursor):
#         try:
#             cursor.execute('''CREATE TABLE IF NOT EXISTS images 
#                             (id INTEGER PRIMARY KEY AUTOINCREMENT, gambar BLOB)''')
#             conn.commit()
#             print("Table 'images' ensured or created.")
#         except sqlite3.Error as e:
#             print(f"Failed to create table: {e}")
#             raise

#     def select_image(self, instance):
#         filechooser.open_file(filters=[("Image files", "*.png", "*.jpg", "*.jpeg")], 
#                              on_selection=self.on_file_selected)

#     def on_file_selected(self, selection):
#         if selection:
#             self.selected_file = selection[0]
#             self.upload_button.disabled = False
#             self.status_label.text = f"Selected: {os.path.basename(self.selected_file)}"

#     def upload_image(self, instance):
#         if self.selected_file:
#             self.status_label.text = "Uploading..."
#             Clock.schedule_once(lambda dt: self.process_upload(), 0)

#     def process_upload(self):
#         try:
#             # Use a new connection for this operation
#             conn = sqlite3.connect("kivydata.db", check_same_thread=False)
#             cursor = conn.cursor()
#             try:
#                 # Ensure table exists in this connection
#                 self.ensure_table_exists(conn, cursor)
#                 cursor.execute("BEGIN TRANSACTION")
#                 with open(self.selected_file, "rb") as image_file:
#                     convertImgToString = base64.b64encode(image_file.read()).decode()
                
#                 cursor.execute("INSERT INTO images (gambar) VALUES (?)", (convertImgToString,))
#                 conn.commit()
#                 print("Image uploaded to database successfully!")
#                 self.status_label.text = "Upload successful!"
                
#                 # Load and display the last inserted image with a new connection
#                 display_conn = sqlite3.connect("kivydata.db", check_same_thread=False)
#                 display_cursor = display_conn.cursor()
#                 try:
#                     display_cursor.execute("SELECT gambar FROM images ORDER BY id DESC LIMIT 1")
#                     gambar = display_cursor.fetchone()[0]
#                     self.image_display.source = f'data:image/jpeg;base64,{gambar}'  # Adjust format if needed
#                     self.image_display.reload()
#                 finally:
#                     display_cursor.close()
#                     display_conn.close()
#             except sqlite3.OperationalError as e:
#                 conn.rollback()
#                 print(f"Database error: {e}")
#                 self.status_label.text = f"Upload failed: {e}"
#             finally:
#                 cursor.close()
#                 conn.close()
#         except Exception as e:
#             print(f"Upload failed: {e}")
#             self.status_label.text = f"Upload failed: {e}"

#     def on_stop(self):
#         if hasattr(self, 'cursor') and self.cursor:
#             self.cursor.close()
#         if hasattr(self, 'conn') and self.conn:
#             self.conn.close()

# if __name__ == '__main__':
#     ImageUploadApp().run()



# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.uix.label import Label
# from kivy.properties import ObjectProperty
# from kivy.clock import Clock
# from plyer import filechooser
# import sqlite3
# import os
# import imghdr

# class ImageUploadApp(App):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.image_display = Image()
#         self.selected_file = None
#         self.status_label = Label(text="", size_hint_y=None, height=30)
#         self.db_path = os.path.join(os.getcwd(), "kivydata.db")  # Explicit database location

#     def build(self):
#         layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
#         # Select Image Button
#         select_button = Button(text="Select Image", size_hint_y=None, height=50)
#         select_button.bind(on_press=self.select_image)
#         layout.add_widget(select_button)

#         # Upload Image Button
#         upload_button = Button(text="Upload Image", size_hint_y=None, height=50, disabled=True)
#         upload_button.bind(on_press=self.upload_image)
#         self.upload_button = upload_button
#         layout.add_widget(upload_button)

#         # Status Label
#         layout.add_widget(self.status_label)

#         # Image Display
#         layout.add_widget(self.image_display)

#         # Initialize database
#         self.init_database()
#         return layout

#     def init_database(self):
#         try:
#             self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
#             self.cursor = self.conn.cursor()
#             self.ensure_table_exists(self.conn, self.cursor)
#             print(f"Database initialized at {self.db_path}")
#         except sqlite3.Error as e:
#             print(f"Failed to connect to database: {e}")
#             self.status_label.text = f"Database connection failed: {e}"

#     def ensure_table_exists(self, conn, cursor):
#         try:
#             cursor.execute('''CREATE TABLE IF NOT EXISTS images 
#                             (id INTEGER PRIMARY KEY AUTOINCREMENT, gambar BLOB)''')
#             conn.commit()
#             print("Table 'images' ensured or created.")
#         except sqlite3.Error as e:
#             print(f"Failed to create table: {e}")
#             raise

#     def select_image(self, instance):
#         filechooser.open_file(filters=[("Image files", "*.png", "*.jpg", "*.jpeg")], 
#                              on_selection=self.on_file_selected)

#     def on_file_selected(self, selection):
#         if selection:
#             self.selected_file = selection[0]
#             self.upload_button.disabled = False
#             self.status_label.text = f"Selected: {os.path.basename(self.selected_file)}"

#     def upload_image(self, instance):
#         if self.selected_file:
#             self.status_label.text = "Uploading..."
#             Clock.schedule_once(lambda dt: self.process_upload(), 0)

#     def process_upload(self):
#         try:
#             # Use a new connection for this operation
#             conn = sqlite3.connect(self.db_path, check_same_thread=False)
#             cursor = conn.cursor()
#             try:
#                 self.ensure_table_exists(conn, cursor)
#                 cursor.execute("BEGIN TRANSACTION")
#                 with open(self.selected_file, "rb") as image_file:
#                     binary_data = sqlite3.Binary(image_file.read())
#                     print(f"Binary data length: {len(binary_data)}")  # Debug
                
#                 cursor.execute("INSERT INTO images (gambar) VALUES (?)", (binary_data,))
#                 conn.commit()
#                 print("Commit successful, checking row count...")
#                 cursor.execute("SELECT COUNT(*) FROM images")
#                 row_count = cursor.fetchone()[0]
#                 print(f"Row count after insert: {row_count}")
#                 cursor.execute("SELECT id, gambar FROM images ORDER BY id DESC LIMIT 1")
#                 last_row = cursor.fetchone()
#                 last_id, last_gambar = last_row
#                 print(f"Last inserted ID: {last_id}, gambar length: {len(last_gambar)}")
                
#                 print("Image uploaded to database successfully!")
#                 self.status_label.text = "Upload successful!"
                
#                 # Display image from database
#                 display_conn = sqlite3.connect(self.db_path, check_same_thread=False)
#                 display_cursor = display_conn.cursor()
#                 try:
#                     display_cursor.execute("SELECT gambar FROM images WHERE id = ?", (last_id,))
#                     gambar = display_cursor.fetchone()[0]
#                     print(f"Retrieved gambar length for display: {len(gambar)}")
#                     image_type = imghdr.what(self.selected_file) or 'jpg'
#                     temp_path = os.path.join(os.getcwd(), f"temp_image_{last_id}.{image_type}")
#                     with open(temp_path, "wb") as temp_file:
#                         temp_file.write(gambar)
#                     self.image_display.source = temp_path
#                     self.image_display.reload()
#                 finally:
#                     display_cursor.close()
#                     display_conn.close()
#                     if os.path.exists(temp_path):
#                         os.remove(temp_path)  # Clean up temp file
#             except sqlite3.OperationalError as e:
#                 conn.rollback()
#                 print(f"Database error: {e}")
#                 self.status_label.text = f"Upload failed: {e}"
#             finally:
#                 cursor.close()
#                 conn.close()
#         except Exception as e:
#             print(f"Upload failed: {e}")
#             self.status_label.text = f"Upload failed: {e}"

#     def on_stop(self):
#         if hasattr(self, 'cursor') and self.cursor:
#             self.cursor.close()
#         if hasattr(self, 'conn') and self.conn:
#             self.conn.close()

# if __name__ == '__main__':
#     ImageUploadApp().run()



from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.image import FitImage
from kivy.clock import Clock
from plyer import filechooser
import sqlite3
import os
import imghdr

class MainLayout(MDBoxLayout):
    pass

class ImageUploadMDApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_display = FitImage(size_hint_y=1)
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
                image_type = imghdr.what(self.selected_file) or 'jpg'
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
