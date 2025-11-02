# 🎹 **Pyano — A Virtual Piano with Recording, Playback & Shortcuts**

**Pyano** is a Python-based virtual piano built using **Pygame** and **Pydub**.
It lets you play notes from your keyboard, record sessions, assign custom shortcuts, and replay your compositions seamlessly — all within an intuitive interface.

---

## 🌟 **Features**

* 🎵 **Interactive Piano Interface** – Play realistic piano notes directly from your keyboard.
* 🔴 **Recording & Exporting** – Record your performances and export them as `.wav` files.
* ⚡ **Shortcut Mappings** – Assign any key to instantly replay saved recordings.
* 🎧 **Layered Playback** – Overlay multiple recordings for rich, blended sound.
* 🎹 **Graphical Interface** – Real-time visual feedback on pressed keys.
* 🔼 **Octave Shifting** – Move between octaves using arrow keys.
* 🧵 **Threaded Saving** – Recordings are saved in a background thread for smooth performance.

---

## 📂 **Project Structure**

```
Pyano/
│
├── pyano.py                # Full-featured version (recording, playback, shortcuts)
├── simple_pyano.py         # Lightweight version (basic virtual piano only)
│
├── assets/
│   ├── buttons/
│   │   ├── record_1.png
│   │   ├── record_2.png
│   │   ├── dd_1.png
│   │   └── dd_2.png
│   ├── A0.wav … C8.wav     # All piano note audio files
│
└── recordings/             # Automatically created for saved performances
```

---

## ⚙️ **Installation**

### 1. Clone the Repository

```bash
git clone https://github.com/nikhilanil87/Pyano.git
cd Pyano
```

### 2. Install Dependencies

Make sure you have **Python 3.9+** installed, then run:

```bash
pip install pygame pydub
```

> **Note:**
> `pydub` requires **ffmpeg**.
> Install it via:
>
> * **Windows:** [Download from ffmpeg.org](https://ffmpeg.org/download.html)
> * **macOS:** `brew install ffmpeg`
> * **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`

---

## 🚀 **How to Use**

### 🪄 Run the Full Version (with Recording & Shortcuts)

```bash
python pyano.py
```

### 🎹 Run the Simple Piano (basic playback only)

```bash
python simple_pyano.py
```

---

### 🎛 Keyboard Controls (Full Version)

| Action                           | Key                     |
| -------------------------------- | ----------------------- |
| **Play Notes**                   | `W, E, R, T, Y...` etc. |
| **Start / Stop Recording**       | `Left Ctrl`             |
| **Toggle Sustain (Hold Notes)**  | `Space`                 |
| **Shift Octave Up**              | `→`                     |
| **Shift Octave Down**            | `←`                     |
| **Open / Close Dropdown**        | Click top dropdown      |
| **Play Recording from Dropdown** | Click on recording name |
| **Exit**                         | `Esc`                   |

---

## 🎙️ **Recording and Shortcuts**

1. Press **Left Ctrl** to start recording.
   → Notes you play are captured with timing and duration.
2. Press **Left Ctrl** again to stop.
3. Enter a **filename** for the recording.
4. Choose whether to **assign a shortcut key** (`Y/N`).

   * If yes, press any key to bind it.
5. Your recording appears in the dropdown and inside the `recordings/` folder.

> 🎼 Tip: Instantly replay any saved recording using its assigned shortcut key.

---

## 🧩 **How It Works**

* **Pygame mixer channels** handle up to 52 notes simultaneously.
* Each key triggers a corresponding sound from the `assets/` folder based on the active octave.
* Recordings store key events (timing, duration, and sound paths) as structured dictionaries.
* **Pydub** layers these sounds to generate `.wav` files asynchronously via threads.

---

## 📦 **Dependencies**

| Library     | Purpose                                           |
| ----------- | ------------------------------------------------- |
| `pygame`    | GUI, keyboard input, and real-time sound playback |
| `pydub`     | Audio overlaying and exporting recordings         |
| `threading` | Background saving of `.wav` files                 |

---

## 📜 **License**

Licensed under the **MIT License** — feel free to use, modify, and expand for your own musical experiments.

---

## 👨‍💻 **Author**

**Nikhil** — *B.Tech Computer Science*
