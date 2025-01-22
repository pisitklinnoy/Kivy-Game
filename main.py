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
from kivy.uix.label import Label


class AnimatedSlime(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames = [f'Slime_animation/{i}.png' for i in range(21)]
        self.current_frame = 0

        # บันทึกตำแหน่งและขนาดเริ่มต้น
        self.original_pos_hint = {'center_x': 0.68, 'center_y': 0.65}
        self.original_size_hint = (0.25, 0.25)
        
        self.health_bar = HealthBar(
            max_health=100,
            size_hint=(0.265, 0.006),
            pos_hint={'center_x': 0.675, 'center_y': 0.528}
        )
        self.add_widget(self.health_bar)

        self.image = Image(
            source=self.frames[self.current_frame],
            size_hint=(0.25, 0.25),
            pos_hint={'center_x': 0.68, 'center_y': 0.65}
        )
        self.add_widget(self.image)


        Clock.schedule_interval(self.update_frame, 0.1)

    def update_frame(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image.source = self.frames[self.current_frame]
        self.image.reload()


    def on_hit(self):
        """แอนิเมชันเมื่อ Slime ถูกโจมตี"""
        print("Slime is hit!")  # Debug

        # โหลดภาพชุดสำหรับแอนิเมชันการโดนตี
        hit_frames = [f'slime_hit_animation/{i}.png' for i in range(29)]  # ใช้ไฟล์ 0.png ถึง 11.png
        original_frames = self.frames  # เก็บเฟรมปกติไว้

        def animate_hit(index, dt):
            """ฟังก์ชันสำหรับเปลี่ยนภาพในแต่ละเฟรม"""
            if index < len(hit_frames):  # ยังมีเฟรมเหลือ
                self.image.source = hit_frames[index]  # เปลี่ยนภาพเป็นเฟรมถัดไป
                self.image.reload()
                Clock.schedule_once(lambda dt: animate_hit(index + 1, dt), 0.009)  # เรียกเฟรมถัดไปทุก 0.05 วินาที
            else:
                # กลับสู่แอนิเมชันปกติ
                self.frames = original_frames
                self.image.source = self.frames[self.current_frame]
                self.image.reload()

        # เริ่มแอนิเมชันที่เฟรมแรก
        animate_hit(0, 0)

    def attack_animation(self, on_attack_complete=None):
        """แอนิเมชันการโจมตีของ Slime"""
        print("Slime attacks!")  # Debug

        attack_frames = [f'slime_attack_animation/{i}.png' for i in range(36)]
        original_frames = self.frames

        def animate_attack(index, dt):
            """ฟังก์ชันสำหรับแสดงแอนิเมชันโจมตี"""
            if index < len(attack_frames):  # หากยังมีเฟรมที่ต้องแสดง
                self.image.source = attack_frames[index]
                self.image.reload()

                # ปรับขนาดและตำแหน่งภาพในแต่ละเฟรม
                self.image.size_hint = (0.7, 0.25)  # ขนาดใหม่ระหว่างโจมตี
                self.image.pos_hint = {'center_x': 0.605, 'center_y': 0.646}  # ตำแหน่งใหม่ระหว่างโจมตี

                Clock.schedule_once(lambda dt: animate_attack(index + 1, dt), 0.013)
            else:
                # กลับสู่เฟรมปกติ
                self.frames = original_frames
                self.image.source = self.frames[self.current_frame]
                self.image.reload()

                # คืนค่าขนาดและตำแหน่งเดิม
                self.image.size_hint = self.original_size_hint
                self.image.pos_hint = self.original_pos_hint

                # หากมี callback หลังโจมตีเสร็จ
                if on_attack_complete:
                    on_attack_complete()

        # เริ่มแอนิเมชันที่เฟรมแรก
        animate_attack(0, 0)

    def on_death(self):
        """แอนิเมชันเมื่อ Slime ตาย"""
        print("Slime has died!")  # Debug

        # โหลดภาพชุดสำหรับแอนิเมชันการตาย
        death_frames = [f'slime_death_animation/{i}.png' for i in range(31)]

        def animate_death(index, dt):
            """ฟังก์ชันสำหรับเปลี่ยนภาพในแต่ละเฟรม"""
            if index < len(death_frames):
                # เปลี่ยนภาพเป็นเฟรมถัดไป
                self.image.source = death_frames[index]
                self.image.reload()

                # ปรับขนาดและตำแหน่งภาพในแต่ละเฟรม
                self.image.size_hint = (0.7, 0.25)  # กำหนดขนาดที่ต้องการ
                self.image.pos_hint = {'center_x': 0.715, 'center_y': 0.657}  # กำหนดตำแหน่งที่ต้องการ

                # เรียกแอนิเมชันเฟรมถัดไปทุก 0.05 วินาที
                Clock.schedule_once(lambda dt: animate_death(index + 1, dt), 0.01)
            else:
                # ลบ Widget หลังแอนิเมชันจบ
                if self.parent:
                    self.parent.remove_widget(self)

        # เริ่มแอนิเมชันที่เฟรมแรก
        animate_death(0, 0)

    def reduce_health(self, amount):
        """ลดค่าเลือดของ Slime"""
        self.health_bar.reduce_health(amount)

        # เช็คว่าเลือดเหลือ 0 หรือไม่
        if self.health_bar.health <= 0:  # เปลี่ยนจาก current_health เป็น health
            self.on_death()  # เรียกแอนิเมชันการตาย
        else:
            self.on_hit()  # เล่นแอนิเมชันโดนตีหากยังมีเลือดเหลือ
            
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

        # วัตถุสำหรับแสดงแอนิเมชัน Magic
        self.magic_effect = Image(
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.685, 'center_y': 0.75},
            opacity=0  # ซ่อนตอนเริ่มต้น
        )
        self.add_widget(self.magic_effect)

        # ตั้งเวลาเปลี่ยนภาพ Character
        Clock.schedule_interval(self.update_frame, 0.1)

    def magic_animation(self, on_animation_complete=None):
        """แอนิเมชันการใช้ Magic"""
        print("Character uses Magic!")  # Debug
        magic_frames = [f'power_fire_animation/{i}.png' for i in range(42)]
        self.magic_effect.opacity = 1  # แสดงแอนิเมชัน Magic

        def animate_magic(index, dt):
            """แสดงแอนิเมชันการใช้ Magic"""
            if index < len(magic_frames):
                self.magic_effect.source = magic_frames[index]  # เปลี่ยนเฟรม Magic
                self.magic_effect.reload()
                Clock.schedule_once(lambda dt: animate_magic(index + 1, dt), 0.01)
            else:
                self.magic_effect.opacity = 0  # ซ่อนแอนิเมชันหลังเสร็จ
                if on_animation_complete:
                    on_animation_complete()

        # เริ่มแอนิเมชัน Magic
        animate_magic(0, 0)

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

class Inventory(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # พื้นหลังหน้าต่าง Inventory
        self.background = Image(
            source="inventory_game.png",  # พื้นหลัง Inventory
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.background)

        # ข้อมูลไอเท็มใน Inventory
        self.items = [
            {
                "name": "Health Potion",
                "effect": "heal",
                "value": 50,
                "background_normal": "Button_image/health_potion_normal.png",
                "background_down": "Button_image/health_potion_down.png",
                "background_disabled": "Button_image/health_potion_disabled.png",
                "pos_hint": {'center_x': 0.367, 'center_y': 0.53},
                "size_hint": (0.25, 0.165),
                "disabled_pos_hint": {'center_x': 0.367, 'center_y': 0.53},
                "disabled_size_hint": (0.208, 0.095),
                "quantity": 1,
            },
            {
                "name": "Mana Potion",
                "effect": "mana",
                "value": 30,
                "background_normal": "Button_image/mana_potion_normal.png",
                "background_down": "Button_image/mana_potion_down.png",
                "background_disabled": "Button_image/mana_potion_disabled.png",
                "pos_hint": {'center_x': 0.369, 'center_y': 0.42},
                "size_hint": (0.241, 0.125),
                "disabled_pos_hint": {'center_x': 0.369, 'center_y': 0.42},
                "disabled_size_hint": (0.208, 0.095),
                "quantity": 1,
            },
        ]

        # แสดงไอเท็มใน Inventory
        for item in self.items:
            item_button = Button(
                size_hint=item["size_hint"],
                pos_hint=item["pos_hint"],
                background_normal=item["background_normal"],
                background_down=item["background_down"],
                text=f"x{item['quantity']}",
                font_size='20sp',
                color=(1, 1, 1, 1),
                disabled=item["quantity"] <= 0
            )
            item_button.bind(on_release=lambda btn, i=item, b=item_button: self.use_item(i, b))
            self.add_widget(item_button)

        # ปุ่มปิดหน้าต่าง Inventory
        self.close_button = Button(
            size_hint=(0.09, 0.11),
            pos_hint={'center_x': 0.37, 'center_y': 0.33},
            background_normal='Button_image/input_exit_inventory_button.png',
            background_down='Button_image/output_exit_inventory_button.png',
        )
        self.close_button.bind(on_release=lambda btn: self.close_inventory())
        self.add_widget(self.close_button)

    def use_item(self, item, button):
        """ใช้งานไอเท็ม"""
        if item["quantity"] > 0:
            print(f"Using item: {item['name']}")
            if item["effect"] == "heal":
                self.parent.character.health_bar.increase_health(item["value"])
            elif item["effect"] == "mana":
                self.parent.character.mana_bar.increase_mana(item["value"])

            # ลดจำนวนไอเท็ม
            item["quantity"] -= 1
            print(f"{item['name']} remaining: {item['quantity']}")

            # อัปเดตข้อความบนปุ่ม
            button.text = f"x{item['quantity']}"

            # หากจำนวนเหลือ 0 ให้ปิดการใช้งานปุ่ม
            if item["quantity"] <= 0:
                button.disabled = True
                button.size_hint = item["disabled_size_hint"]
                button.pos_hint = item["disabled_pos_hint"]

    def update_inventory(self):
        """อัปเดตหน้าต่าง Inventory"""
        self.clear_widgets()
        self.__init__()

    def close_inventory(self):
        """ปิดหน้าต่าง Inventory"""
        parent = self.parent
        if parent and hasattr(parent, 'inventory'):
            parent.inventory = None
            parent.remove_widget(self)

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

        enermy_heal_bar = Image(
            source='enermy_heal_bar.png',  # พาธรูปภาพที่ต้องการเพิ่ม
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.665, 'center_y': 0.53}  # กำหนดตำแหน่ง
        )
        self.layout.add_widget(enermy_heal_bar)

        self.slime = AnimatedSlime()
        self.layout.add_widget(self.slime)

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
            {'x': 0.034, 'y': 0.37},  # ตำแหน่งปุ่ม 1
            {'x': 0.026, 'y': 0.30},  # ตำแหน่งปุ่ม 2
            {'x': 0.027, 'y': 0.23},    # ตำแหน่งปุ่ม 3
        ]

        button_sizes = [
            (0.15, 0.10),  # ขนาดสำหรับปุ่ม 1
            (0.15, 0.11),  # ขนาดสำหรับปุ่ม 2
            (0.16, 0.12),    # ขนาดสำหรับปุ่ม 3
        ]

        # # รูปภาพสำหรับปุ่มแต่ละปุ่ม
        button_images_normal = [
            'Button_image/onput_fight_font_button.png',  # รูปปุ่มปกติสำหรับปุ่ม 1
            'Button_image/onput_magic_font_button.png',  # รูปปุ่มปกติสำหรับปุ่ม 2
            'Button_image/onput_bags_font_button.png',          # รูปปุ่มปกติสำหรับปุ่ม 3
        ]

        button_images_down = [
            'Button_image/output_fight_font_button.png',       # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 1
            'Button_image/output_magic_font_button.png', # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 2
            'Button_image/output_bags_font_button.png',            # รูปปุ่มเมื่อถูกกดสำหรับปุ่ม 3
        ]

        # สร้างปุ่มแต่ละปุ่ม
        for i, pos in enumerate(button_positions):
            button = Button(
                size_hint=button_sizes[i],  # ใช้ขนาดที่กำหนดไว้สำหรับแต่ละปุ่ม
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

        # ป้ายข้อความแสดงผลลัพธ์
        self.result_label = Label(
            text="",
            font_size='40sp',
            color=(1, 1, 1, 1),  # สีขาว
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(0.8, 0.2),
        )
        self.layout.add_widget(self.result_label)

    def on_button_press(self, button_index):
        if button_index == 0:  # ปุ่ม Fight
            print("Character attacks Slime with Fight!")
            self.slime.reduce_health(10)  # ลดเลือดของ Slime ลง 10

            # Slime โจมตีตัวละครกลับ
            Clock.schedule_once(lambda dt: self.slime_attacks_character(), 0.5)

        elif button_index == 1:  # ปุ่ม Magic
            if self.character.mana_bar.mana >= 50:  # เช็คว่ามานาเพียงพอ
                print("Character attacks Slime with Magic!")
            
                # ลดมานาทันที
                self.character.mana_bar.reduce_mana(50)

                # Slime แสดงแอนิเมชัน on_hit ทันที
                self.slime.on_hit()
            
                # ลดเลือดของ Slime
                self.slime.reduce_health(20)

                # เรียกแอนิเมชัน Magic
                self.character.magic_animation()

                # Slime โจมตีตัวละครกลับ
                Clock.schedule_once(lambda dt: self.slime_attacks_character(), 0.01)
            else:
                print("Not enough mana to use Magic!")
    
        elif button_index == 2:  # ปุ่ม Bags
            print("Opening Inventory!")
            if not hasattr(self, "inventory") or not self.inventory:
                self.inventory = Inventory()  # สร้างหน้าต่าง Inventory
                self.add_widget(self.inventory)
            else:
                print("Inventory is already open!")
                
        self.check_health_status()

    def slime_attacks_character(self):
        print("Slime attacks Character!")
    
        # เรียกใช้แอนิเมชันการโจมตีของ Slime
        self.slime.attack_animation(
            on_attack_complete=lambda: self.character.health_bar.reduce_health(15)  # ลดเลือดตัวละครลง 15 หลังแอนิเมชันจบ
        )
        self.check_health_status()

    def check_health_status(self):
        """ตรวจสอบสถานะเลือดของตัวละครและ Slime"""
        if self.character.health_bar.health <= 0:
            self.result_label.text = "Defeat"
            self.result_label.color = (1, 0, 0, 1)  # สีแดง
            self.disable_game_controls()

        elif self.slime.health_bar.health <= 0:
            self.result_label.text = "Victory"
            self.result_label.color = (0, 1, 0, 1)  # สีเขียว
            self.disable_game_controls()

    def disable_game_controls(self):
        """ปิดการควบคุมเกมหลังจากจบ"""
        for child in self.layout.children:
            if isinstance(child, Button):
                child.disabled = True

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
