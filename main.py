from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from fungsiya import vaqt

Builder.load_file('ui_qismi.kv')

if platform not in ('android', 'ios'):
    Window.size = (360, 650)
    Window.left = 900
    Window.top = 14


class Oyna(Screen):
    def ornatildi(self):
        # Ish va dam olish vaqtini minutdan sekundga o'girib saqlaymiz
        self.manager.get_screen('Oyna1').ishlash_vaqti = int(self.ids.ol_ish.text) * 60
        self.manager.get_screen('Oyna1').dam_vaqti = int(self.ids.ol_dam.text) * 60
        self.manager.current = 'Oyna1'

class Oyna1(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ishlash_vaqti = 0
        self.dam_vaqti = 0
        self.qolgan_vaqt = 0
        self.holat = "ish"  # Boshlang'ich holat: "ish" yoki "dam"
        self.event = None
        self.running = False

    def toggle_timer(self):
        if self.running:
            # To'xtatish
            if self.event:
                self.event.cancel()
            self.ids.btn.text = "Start"
            self.running = False
        else:
            # Davom ettirish
            if self.qolgan_vaqt == 0:
                self.qolgan_vaqt = self.ishlash_vaqti
            
            self.event = Clock.schedule_interval(self.update_ui, 1)
            self.ids.btn.text = "Stop"
            self.running = True

    def update_ui(self, dt):
        # Ikkala labelga ham real vaqtni yozamiz
        hozirgi_vaqt = vaqt()
        self.ids.matn.text = hozirgi_vaqt  # Yashil soat
        self.ids.matn1.text = hozirgi_vaqt # Qizil soat
        
        # Holatga qarab ko'rsatishni boshqarish
        if self.holat == "ish":
            self.ids.matn.opacity = 1    # Yashil ko'rinadi
            self.ids.matn1.opacity = 0.1 # Qizil xiralashadi
        else:
            self.ids.matn.opacity = 0.1  # Yashil xiralashadi
            self.ids.matn1.opacity = 1   # Qizil ko'rinadi

        # Taymer mantig'i
        self.qolgan_vaqt -= 1
        if self.qolgan_vaqt <= 0:
            if self.holat == "ish":
                self.holat = "dam"
                self.qolgan_vaqt = self.dam_vaqti
            else:
                self.holat = "ish"
                self.qolgan_vaqt = self.ishlash_vaqti

class Soat(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Oyna(name='Oyna'))
        sm.add_widget(Oyna1(name='Oyna1'))
        return sm

if __name__ == "__main__":
    Soat().run()