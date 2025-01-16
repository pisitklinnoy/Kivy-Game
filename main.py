from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # พื้นหลังอยู่ตรงกลางและขนาดพอดีกับหน้าจอ
        self.background = Image(
            source='image.png',  # ใส่รูปพื้นหลังที่คุณต้องการ
            size_hint=(1, 1),      # ขนาดเป็น 80% ของหน้าจอ
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # ให้อยู่ตรงกลาง
        )
        layout.add_widget(self.background)

        # ปุ่ม Play
        play_button = Button(
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.35, 'y': 0.6},
            background_normal='button_game.png',  # ใช้รูปปุ่ม Play
            background_down='button_game.png'
        )
        play_button.bind(on_press=self.go_to_play)
        layout.add_widget(play_button)

        # ปุ่ม Menu
        pause_button = Button(
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.36, 'y': 0.45},
            background_normal='button_menu.png',  # ใช้รูปปุ่ม Pause
            background_down='button_menu.png'
        )
        pause_button.bind(on_press=lambda x: print("Menu pressed"))
        layout.add_widget(pause_button)

        # ปุ่ม Exit
        options_button = Button(
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.353, 'y': 0.28},
            background_normal='button_exit.png',  # ใช้รูปปุ่ม Exit
            background_down='button_exit.png'
        )
        options_button.bind(on_press=self.exit_app)
        layout.add_widget(options_button)

        self.add_widget(layout)

    def go_to_play(self, instance):
        # เปลี่ยนไปที่หน้าจอ Play
        self.manager.current = 'play'

    def exit_app(self, instance):
        # ออกจากแอป
        App.get_running_app().stop()
        Window.close()


class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # สร้าง FloatLayout สำหรับหน้าจอนี้
        self.layout = FloatLayout()

        # เพิ่มภาพพื้นหลัง
        background = Image(
            source='Background_monter.png',  # ใส่ชื่อไฟล์พื้นหลังของคุณ
            size_hint=(1, 1),  # ครอบคลุมทั้งหน้าจอ
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(background)

        # เพิ่มตัวละครผู้เล่นบริเวณซ้ายล่าง
        self.player = Image(
            source='Charector.png',  # ไฟล์รูปตัวละครผู้เล่น
            size_hint=(0.2, 0.2),  # ขนาด 20% ของหน้าจอ
            pos_hint={'x': 0, 'y': 0}  # ตำแหน่งซ้ายล่าง
        )
        self.layout.add_widget(self.player)

        # เพิ่มmonster
        self.monster = Image(
            source='golem.png',  # ใส่ชื่อไฟล์มอนสเตอร์ของคุณ
            size_hint=(0.5, 0.5),  # ขนาด 20% ของหน้าจอ
            pos_hint={'center_x': 0.5, 'center_y': 0.4}  # ตำแหน่งเริ่มต้น
        )
        self.layout.add_widget(self.monster)

        self.health_bar = ProgressBar(
            max=110,  # ค่าสูงสุดของเลือด
            value=110,  # ค่าเริ่มต้น (เต็มหลอด)
            size_hint=(0.4, 10),  # ขนาดของหลอดเลือด
            pos_hint={'center_x': 0.5, 'center_y': 0.9}  # ตำแหน่งอยู่บนมอนสเตอร์
        )
        self.layout.add_widget(self.health_bar)

        # ปุ่มกลับไปที่เมนู
        back_button = Button(
            size_hint=(0.09, 0.1),
            pos_hint={'center_x': 0.94, 'y': 0.9},
            background_normal='cross_button.png',  # ใช้รูปปุ่ม Pause
            background_down='cross_button.png'
        )
        back_button.bind(on_press=self.go_to_menu)
        self.layout.add_widget(back_button)

        # เพิ่ม layout เป็นวิดเจ็ตลูกใน PlayScreen
        self.add_widget(self.layout)

        # เรียกฟังก์ชันเคลื่อนไหวมอนสเตอร์
        self.animate_monster()


    def go_to_menu(self, instance):
        # เปลี่ยนกลับไปยังหน้าจอเมนู
        self.manager.current = 'menu'

    def animate_monster(self):
        # สร้างการเคลื่อนไหวซ้าย-ขวา
        animation = Animation(pos_hint={'center_x': 0.8}, duration=4) + \
                    Animation(pos_hint={'center_x': 0.2}, duration=4)
        animation.repeat = True  # ทำซ้ำการเคลื่อนไหว
        animation.start(self.monster)

    def on_touch_down(self, touch):
        # ตรวจสอบว่าคลิกโดนมอนสเตอร์หรือไม่
        if self.monster.collide_point(*touch.pos):
            self.reduce_health()
        else:
            self.show_miss()  # แสดงข้อความ "Miss"
        return super().on_touch_down(touch)


    def reduce_health(self):
        # ลดเลือดของมอนสเตอร์เมื่อคลิกโดน
        if self.health_bar.value > 0:
            self.health_bar.value -= 2  # ลดเลือดครั้งละ 10
            print(f"Monster health: {self.health_bar.value}")

    
    def show_miss(self):
        # แสดงรูปภาพ "Miss"
        miss_image = Image(
            source='miss.png',  # ไฟล์ภาพที่จะแสดง
            size_hint=(1, 1),  # ขนาดของภาพ (ปรับตามต้องการ)
            pos_hint={'center_x': 0.54, 'center_y': 0.6}  # ตำแหน่งกลางหน้าจอด้านบน
        )
        self.layout.add_widget(miss_image)

        # ลบภาพ "Miss" หลังจาก 1 วินาที
        Clock.schedule_once(lambda dt: self.layout.remove_widget(miss_image), 0.2)
        
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))  # หน้าจอเมนู
        sm.add_widget(PlayScreen(name='play'))  # หน้าจอเล่นเกม
        return sm


if __name__ == '__main__':
    MyApp().run()
