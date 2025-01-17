from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class AnimatedSlime(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ลำดับของไฟล์ภาพ slime
        self.frames = [f'Slime_animation/{i}.png' for i in range(21)]
        self.current_frame = 0

        # แสดงภาพ slime
        self.image = Image(
            source=self.frames[self.current_frame],
            size_hint=(0.25, 0.25),
            pos_hint={'center_x': 0.68, 'center_y': 0.65}
        )
        self.add_widget(self.image)

        # ตั้งเวลาเปลี่ยนภาพ slime
        Clock.schedule_interval(self.update_frame, 0.1)

    def update_frame(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image.source = self.frames[self.current_frame]
        self.image.reload()


class AnimatedCharacter(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ลำดับของไฟล์ภาพ Character
        self.frames = [f'Charector_animation/{i}.png' for i in range(48)]
        self.current_frame = 0

        # แสดงภาพ Character
        self.image = Image(
            source=self.frames[self.current_frame],
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.34, 'center_y': 0.7}
        )
        self.add_widget(self.image)

        # เพิ่ม HealthBar (หลอดเลือดสีแดง)
        self.health_bar = HealthBar(
            max_health=100,
            size_hint=(0.27, 0.006),
            pos_hint={'center_x': 0.350, 'center_y': 0.549}
        )
        self.add_widget(self.health_bar)

        # เพิ่ม ManaBar (หลอดมานาสีฟ้า)
        self.mana_bar = ManaBar(
            max_mana=100,
            size_hint=(0.27, 0.006),
            pos_hint={'center_x': 0.350, 'center_y': 0.509}
        )
        self.add_widget(self.mana_bar)

        # ตั้งเวลาเปลี่ยนภาพ Character
        Clock.schedule_interval(self.update_frame, 0.1)

    def update_frame(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image.source = self.frames[self.current_frame]
        self.image.reload()

class ManaBar(Widget):
    mana = NumericProperty(100)  # ค่าเริ่มต้นของมานา

    def __init__(self, max_mana=100, **kwargs):
        super().__init__(**kwargs)
        self.max_mana = max_mana  # ค่าเต็มของมานา
        self.mana = max_mana  # เริ่มต้นที่ค่ามานาเต็ม

        # กำหนดขนาดหลอดมานา
        self.size_hint = kwargs.get('size_hint', (0.3, 0.05))
        self.pos_hint = kwargs.get('pos_hint', {'center_x': 0.5, 'center_y': 0.45})

        # วาดหลอดมานาใน canvas
        with self.canvas:
            # สีพื้นหลัง (สีเทา)
            Color(0.3, 0.3, 0.3, 1)  # RGBA
            self.background = Rectangle(size=self.size, pos=self.pos)

            # สีมานา (สีฟ้า)
            Color(0, 0, 1, 1)  # สีฟ้า RGBA
            self.mana_bar = Rectangle(size=self.size, pos=self.pos)

        # อัปเดตตำแหน่งและขนาดเมื่อมีการเปลี่ยนแปลง
        self.bind(pos=self.update_bar, size=self.update_bar, mana=self.update_bar)

    def update_bar(self, *args):
        """อัปเดตหลอดมานาเมื่อค่าหรือขนาดเปลี่ยน"""
        self.background.size = self.size
        self.background.pos = self.pos

        # ความกว้างของหลอดมานาสัมพันธ์กับค่า mana
        mana_width = (self.mana / self.max_mana) * self.size[0]
        self.mana_bar.size = (mana_width, self.size[1])
        self.mana_bar.pos = self.pos

    def reduce_mana(self, amount):
        """ลดค่ามานา"""
        self.mana = max(0, self.mana - amount)  # ลดค่ามานาแต่ไม่ต่ำกว่า 0

    def increase_mana(self, amount):
        """เพิ่มค่ามานา"""
        self.mana = min(self.max_mana, self.mana + amount)  # เพิ่มค่ามานาแต่ไม่เกิน max

class HealthBar(Widget):
    health = NumericProperty(100)  # ค่าเลือดเริ่มต้น

    def __init__(self, max_health=100, **kwargs):
        super().__init__(**kwargs)
        self.max_health = max_health  # ค่าเลือดสูงสุด
        self.health = max_health  # เริ่มต้นที่ค่าหลอดเต็ม

        # กำหนดขนาดหลอดเลือด
        self.size_hint = kwargs.get('size_hint', (0.3, 0.05))
        self.pos_hint = kwargs.get('pos_hint', {'center_x': 0.5, 'center_y': 0.5})

        # วาดหลอดเลือดใน canvas
        with self.canvas:
            # สีพื้นหลัง (สีเทา)
            Color(0.3, 0.3, 0.3, 1)  # RGBA
            self.background = Rectangle(size=self.size, pos=self.pos)

            # สีเลือด (สีแดง)
            Color(1, 0, 0, 1)  # สีแดง RGBA
            self.health_bar = Rectangle(size=self.size, pos=self.pos)

        # อัปเดตตำแหน่งและขนาดเมื่อมีการเปลี่ยนแปลง
        self.bind(pos=self.update_bar, size=self.update_bar, health=self.update_bar)

    def update_bar(self, *args):
        """อัปเดตหลอดเลือดเมื่อค่าหรือขนาดเปลี่ยน"""
        self.background.size = self.size
        self.background.pos = self.pos

        # ความกว้างของหลอดเลือดสัมพันธ์กับค่า health
        health_width = (self.health / self.max_health) * self.size[0]
        self.health_bar.size = (health_width, self.size[1])
        self.health_bar.pos = self.pos

    def reduce_health(self, amount):
        """ลดค่าเลือด"""
        self.health = max(0, self.health - amount)  # ลดค่าเลือดแต่ไม่ต่ำกว่า 0

    def increase_health(self, amount):
        """เพิ่มค่าเลือด"""
        self.health = min(self.max_health, self.health + amount)  # เพิ่มค่าเลือดแต่ไม่เกิน max

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # พื้นหลัง
        self.background = Image(
            source='Main_background.png',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(self.background)

        # ปุ่ม Play
        play_button = Button(
            size_hint=(0.1, 0.12),
            pos_hint={'x': 0.597, 'y': 0.44},
            background_normal='Play_button.png',
            background_down='Play_button.png'
        )
        play_button.bind(on_press=self.go_to_play)
        layout.add_widget(play_button)

        # ปุ่ม Exit
        exit_button = Button(
            size_hint=(0.09, 0.1),
            pos_hint={'x': 0.624, 'y': 0.82},
            background_normal='cross_button.png',
            background_down='cross_button.png'
        )
        exit_button.bind(on_press=self.exit_app)
        layout.add_widget(exit_button)

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

        # สร้าง FloatLayout สำหรับจัดการองค์ประกอบ
        self.layout = FloatLayout()

        # พื้นหลัง
        background = Image(
            source='All_backgroiund.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(background)

        # เพิ่ม slime
        self.slime = AnimatedSlime()
        self.layout.add_widget(self.slime)

        # รูปภาพบริเวณขวาล่าง
        static_image = Image(
            source='Battle_Ui.png',  # ใส่ชื่อไฟล์รูปภาพ
            size_hint=(0.4, 0.5),
            pos_hint={'x': 0.33, 'y': 0.0}
        )
        self.layout.add_widget(static_image)

        heal_bar = Image(
            source='heal_bar.png',  # พาธรูปภาพที่ต้องการเพิ่ม
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.338, 'center_y': 0.555}  # กำหนดตำแหน่ง
        )
        self.layout.add_widget(heal_bar)

        mana_bar = Image(
            source='mana_bar.png',  # พาธรูปภาพที่ต้องการเพิ่ม
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.338, 'center_y': 0.515}  # กำหนดตำแหน่ง
        )
        self.layout.add_widget(mana_bar)

        # ปุ่ม 4 ปุ่มบริเวณขวาล่างพร้อมรูปภาพแยก
        button_positions = [
            {'x': 0.33, 'y': 0.25},  # ตำแหน่งปุ่ม 1
            {'x': 0.5, 'y': 0.25},   # ตำแหน่งปุ่ม 2
            {'x': 0.4, 'y': 0.1},    # ตำแหน่งปุ่ม 3
            {'x': 0.5, 'y': 0.1}     # ตำแหน่งปุ่ม 4
        ]

        # รูปภาพสำหรับปุ่มแต่ละปุ่ม
        button_images_normal = [
            'Button_image/button_fight.png',  # รูปปุ่มปกติสำหรับปุ่ม 1
            'button_image_2_normal.png',  # รูปปุ่มปกติสำหรับปุ่ม 2
            'button_image_3_normal.png',  # รูปปุ่มปกติสำหรับปุ่ม 3
            'button_image_4_normal.png'  # รูปปุ่มปกติสำหรับปุ่ม 4
        ]

        button_images_down = [
            'Button_image/button_fight.png',  # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 1
            'button_image_2_down.png',  # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 2
            'button_image_3_down.png',  # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 3
            'button_image_4_down.png'  # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 4
        ]

        # สร้างปุ่มแต่ละปุ่ม
        for i, pos in enumerate(button_positions):
            button = Button(
                size_hint=(0.17, 0.17),  # กำหนดขนาดปุ่ม
                pos_hint=pos,
                background_normal=button_images_normal[i],  # ใช้รูปสำหรับสถานะปกติ
                background_down=button_images_down[i]       # ใช้รูปสำหรับสถานะถูกกด
            )
            button.bind(on_press=lambda instance, idx=i: self.on_button_press(idx))  # ผูกฟังก์ชันเมื่อกดปุ่ม
            self.layout.add_widget(button)


        # เพิ่มตัวละครใหม่
        self.character = AnimatedCharacter()
        self.layout.add_widget(self.character)

        # ปุ่มกลับไปที่เมนู
        back_button = Button(
            size_hint=(0.09, 0.1),
            pos_hint={'center_x': 0.94, 'y': 0.9},
            background_normal='cross_button.png',
            background_down='cross_button.png'
        )
        back_button.bind(on_press=self.go_to_menu)
        self.layout.add_widget(back_button)

        # เพิ่ม layout เป็นวิดเจ็ตลูกใน PlayScreen
        self.add_widget(self.layout)

    def on_button_press(self, button_index):
        print(f"Button {button_index + 1} pressed")

    def go_to_menu(self, instance):
        # เปลี่ยนกลับไปยังหน้าจอเมนู
        self.manager.current = 'menu'



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))  # หน้าจอเมนู
        sm.add_widget(PlayScreen(name='play'))  # หน้าจอเล่นเกม
        return sm


if __name__ == '__main__':
    MyApp().run()
