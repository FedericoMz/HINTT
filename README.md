# HINTT

**_HINTT Is Not a Traditional Translator_**, but a Python  tool that lets you **select a region of your screen**, captures it as an image, and uses **OpenAI's GPT-4 Vision** model to extract and translate text from the screenshot with **a simple keyboard shortcut**.

HINTT is the perfect companion for playing games in a foreign language or visiting foreign websites!

---

## Features

- **Screen region selector** with transparent overlay (Tkinter)
- **Global hotkey** (`q`) for quick screenshot capture
- **Image-to-text translation** powered by OpenAI Vision (GPT-4.1)
- On-screen display of the translated text you can move around
- Lightweight, Python-native, and easy to extend!

---

## How To Use

1. Launch the app.
```bash
python main.py
```
2. Select a region of the screen with your mouse.
2. Press **`q`** to translate the text in that region.
3. The selected image is captured and sent to OpenAI's API.
4. The translated result is shown in a floating window.

Note: HINTT does not support capturing content from other desktops or full-screen apps. Use it in windowed mode.

The GIF below shows an edge case where HINTT excels: translating Japanese text displayed vertically.

![HINTT demo showing Japanese text](demo.gif)
---

## Requirements

- Python 3.8+
- Access to OpenAI APIs.

Install dependencies:
```bash
pip install -r requirements.txt
```

Set your API key as an environment variable:
```bash
export OPENAI_API_KEY=your-api-key-here  # Unix
set OPENAI_API_KEY=your-api-key-here     # Windows
```

On Windows, you may need to run your terminal as Administrator.

## To-Do / Improvements

- [ ] A better GUI
- [ ] Allow customizing the prompt, the output language, and the model
- [ ] Use translation history as context



