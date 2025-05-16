# HINTT

**_HINTT Is Not a Traditional Translator_**, but a Python tool that lets you **select a region of your screen**, captures it as an image, and uses **OpenAI's GPT-4 Vision** model to extract and translate text from the screenshot with **a simple keyboard shortcut**.

HINTT is the perfect companion for playing games in a foreign language or visiting foreign websites!

---

## Features

- **Screen region selector** with transparent overlay (Tkinter)
- **Global hotkey** (`q`) for quick screenshot capture
- **Image-to-text translation** powered by OpenAI Vision (GPT-4.1)
- On-screen display of the translated text you can move around
- Retain previously translated text for context
- Compatible with **OpenAI** and open-source **Ollama** models
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

## Requirements and configuration

- Python 3.10+
- Access to OpenAI APIs for the best experience

Install dependencies:
```bash
pip install -r requirements.txt
```

In `config.env` you can set the OpenAI key and customize the prompt (and thus the output language), the OpenAI model used, and how many previous messages are retained for translation context.

If you set `RUN_MODE="Ollama"` or `RUN_MODE="ollama"`, a local Ollama model will be used instead, set via the `OLLAMA_MODEL` variable. HINTT has been tested with `llava` and `granite3.2-vision`. Results are far worse than with OpenAI, and you might have to tweak the prompt. Hopefully better models will be available in the future.

## To-Do / Improvements

- [ ] A proper GUI
- [X] Allow customizing the prompt, the output language, and the model
- [X] Use translation history as context
- [X] Implement Ollama models as an option



