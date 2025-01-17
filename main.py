from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock


class AnimatedSlime(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ลำดับของไฟล์ภาพ slime
        self.frames = [f'Slime_animation/{i}.png' for i in range(21)]
        self.current_frame = 0

        # แสดงภาพ slime
        self.image = Image(
            source=self.frames[self.current_frame],
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.85, 'center_y': 0.36}
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
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.2, 'center_y': 0.43}
        )
        self.add_widget(self.image)

        # ตั้งเวลาเปลี่ยนภาพ Character
        Clock.schedule_interval(self.update_frame, 0.1)

    def update_frame(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image.source = self.frames[self.current_frame]
        self.image.reload()


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # พื้นหลัง
        self.background = Image(
            source='image.png',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(self.background)

        # ปุ่ม Play
        play_button = Button(
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.35, 'y': 0.6},
            background_normal='button_game.png',
            background_down='button_game.png'
        )
        play_button.bind(on_press=self.go_to_play)
        layout.add_widget(play_button)

        # ปุ่ม Exit
        exit_button = Button(
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.353, 'y': 0.28},
            background_normal='button_exit.png',
            background_down='button_exit.png'
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
            source='Indie Game Background (1).jpg',
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

        # ปุ่ม 4 ปุ่มบริเวณขวาล่าง
        button_positions = [
            {'x': 0.32, 'y': 0.27},
            {'x': 0.5, 'y': 0.25},
            {'x': 0.4, 'y': 0.1},
            {'x': 0.5, 'y': 0.1}
        ]
        for i, pos in enumerate(button_positions):
            button = Button(
                text=f'Button {i + 1}',
                size_hint=(0.08, 0.1),
                pos_hint=pos
            )
            button.bind(on_press=lambda instance, idx=i: self.on_button_press(idx))
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
