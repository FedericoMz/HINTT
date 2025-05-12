import threading
import base64
import mss

import tkinter as tk
from pynput import keyboard
from io import BytesIO
from PIL import Image
from translator import LLMTranslator

class Drawer:
    def __init__(self):
        self.message_window = None
        self.root = tk.Tk()
        self.llm = LLMTranslator()
        self.setup_window()
        self.start_hotkey_listener()

    def setup_secondary_window(self):
        if self.message_window:
            self.message_window.destroy()

        self.message_window = tk.Toplevel(self.root)
        self.message_window.geometry("300x100+{}+{}".format(self.screen_start_x, self.screen_end_y + 10))
        self.message_window.title("HINT")

    def setup_window(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.attributes('-alpha', 0.3)
        self.root.configure(bg='white')

        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = self.start_y = 0
        self.rect = None

        self.canvas.bind("<Button-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_end)

    def on_start(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='cyan')

    def on_drag(self, event):
        cur_x = event.x
        cur_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_end(self, event):
        self.end_x = event.x
        self.end_y = event.y
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        self.screen_start_x = self.start_x + root_x
        self.screen_start_y = self.start_y + root_y
        self.screen_end_x = self.end_x + root_x
        self.screen_end_y = self.end_y + root_y

        self.root.lower()
        self.setup_secondary_window()

    def bring_to_foreground(self):
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)

    def take_screenshot(self):
        if hasattr(self, 'screen_start_x') and hasattr(self, 'screen_start_y'):
            with mss.mss() as sct:
                monitor = {
                    "top": self.screen_start_y,
                    "left": self.screen_start_x,
                    "width": self.screen_end_x - self.screen_start_x,
                    "height": self.screen_end_y - self.screen_start_y
                }
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

                translation = self.llm.translate_image(base64_image)
                self.show_saved_message(translation)

    def show_saved_message(self, string):
        for widget in self.message_window.winfo_children():
            widget.destroy()
        label = tk.Label(self.message_window, text=string, font=("Arial", 14), wraplength=280, justify="left")
        label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def start_hotkey_listener(self):
        threading.Thread(target=self.listen_hotkey, daemon=True).start()

    def listen_hotkey(self):
        def on_press(key):
            if key == keyboard.KeyCode.from_char('q'):
                self.take_screenshot()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def exit_app(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
