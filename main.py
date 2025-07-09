from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class MinimalApp(MDApp):
    def build(self):
        print("Starting minimal app")
        self.theme_cls.primary_palette = "Blue"
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(MDLabel(text="Hello, World!"))
        return layout

if __name__ == '__main__':
    MinimalApp().run()
