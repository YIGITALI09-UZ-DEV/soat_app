from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from datetime import datetime, timedelta
from fungsiya import vaqt

# Deraza sozlamalari
if platform not in ('android', 'ios'):
    Window.size = (360, 650)
    Window.left = 900
    Window.top = 14

Builder.load_file('ui_qismi.kv')

class Oyna(Screen):
    def ornatildi(self):
        oyna1 = self.manager.get_screen('Oyna1')
        oyna1.ishlash_davomiyligi = int(self.ids.ol_ish.text) * 60
        oyna1.dam_davomiyligi = int(self.ids.ol_dam.text) * 60
        oyna1.qolgan_vaqt = oyna1.ishlash_davomiyligi
        oyna1.holat = "ish"
        # Boshlang'ich tugash vaqtini hisoblab olamiz
        oyna1.qotgan_vaqt_str = (datetime.now() + timedelta(seconds=oyna1.qolgan_vaqt)).strftime("%H:%M:%S")
        self.manager.current = 'Oyna1'

class Oyna1(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ishlash_davomiyligi = 0
        self.dam_davomiyligi = 0
        self.qolgan_vaqt = 0
        self.holat = "ish"
        self.qotgan_vaqt_str = ""
        self.running = False
        self.event = None

    def toggle_timer(self):
        if self.running:
            if self.event: self.event.cancel()
            self.ids.btn.text = "Start"
        else:
            self.event = Clock.schedule_interval(self.update_ui, 1)
            self.ids.btn.text = "Stop"
        self.running = not self.running

    def update_ui(self, dt):
        # Taymerni kamaytirish
        self.qolgan_vaqt -= 1
        
        # Holat almashganda yangi tugash vaqtini hisoblash
        if self.qolgan_vaqt <= 0:
            if self.holat == "ish":
                self.holat = "dam"
                self.qolgan_vaqt = self.dam_davomiyligi
            else:
                self.holat = "ish"
                self.qolgan_vaqt = self.ishlash_davomiyligi
            self.qotgan_vaqt_str = (datetime.now() + timedelta(seconds=self.qolgan_vaqt)).strftime("%H:%M:%S")

        # UI yangilash
        if self.holat == "ish":
            self.ids.matn.text = vaqt() # Yashil harakatlanadi[cite: 2]
            self.ids.matn.opacity = 1
            self.ids.matn1.text = self.qotgan_vaqt_str # Qizil qotadi[cite: 2]
            self.ids.matn1.opacity = 0.3
        else:
            self.ids.matn.text = self.qotgan_vaqt_str # Yashil qotadi[cite: 2]
            self.ids.matn.opacity = 0.3
            self.ids.matn1.text = vaqt() # Qizil harakatlanadi[cite: 2]
            self.ids.matn1.opacity = 1

class Soat(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Oyna(name='Oyna'))
        sm.add_widget(Oyna1(name='Oyna1'))
        return sm

if __name__ == "__main__":
    Soat().run()