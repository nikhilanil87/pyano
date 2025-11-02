# 🎹 **Pyano — A Virtual Piano with Recording, Playback & Shortcuts**

**Pyano** is a Python-based virtual piano built using **Pygame** and **Pydub**.
It lets you play notes from your keyboard, record sessions, assign custom shortcuts, and replay your compositions effortlessly — all within an intuitive, interactive interface.

---

## 🌟 **Features**

* 🎵 **Interactive Piano Interface** – Play realistic piano notes directly from your keyboard.
* 🔴 **Recording & Exporting** – Record your performances and export them as `.wav` files.
* ⚡ **Shortcut Mappings** – Assign any key to instantly replay saved recordings.
* 🎧 **Layered Playback** – Overlay multiple recordings to create rich, blended tracks.
* 🎹 **Graphical Interface** – White and black keys rendered with real-time color feedback.
* 🔼 **Octave Shifting** – Move between octaves using the arrow keys.
* 🧵 **Threaded Saving** – Exports recordings in a background thread, keeping the GUI smooth.

---

## 📂 **Project Structure**

```
Pyano/
│
├── main.py                # Main application file
│
├── assets/
│   ├── buttons/
│   │   ├── record_1.png
│   │   ├── record_2.png
│   │   ├── dd_1.png
│   │   └── dd_2.png
│   ├── A0.wav … C8.wav    # All piano note audio files
│
└── recordings/            # Automatically created for saved performances
```

---

## ⚙️ **Installation**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Pyano.git
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

### Start the Piano

```bash
python main.py
```

### Keyboard Controls

| Action                           | Key                       |
| -------------------------------- | ------------------------- |
| **Play Notes**                   | `W, E, R, T, Y...` etc.   |
| **Start / Stop Recording**       | `Left Ctrl`               |
| **Toggle Sustain (Hold Notes)**  | `Space`                   |
| **Shift Octave Up**              | `→`                       |
| **Shift Octave Down**            | `←`                       |
| **Open / Close Dropdown**        | Click top dropdown button |
| **Play Recording from Dropdown** | Click on recording name   |
| **Exit**                         | `Esc`                     |

---

## 🎙️ **Recording and Shortcuts**

1. Press **Left Ctrl** to start recording.
   → Notes you play are captured with precise timing and duration.
2. Press **Left Ctrl** again to stop.
3. You’ll be prompted to **enter a filename** for your recording.
4. Then choose whether to **assign a shortcut key** (`Y/N`).

   * If yes, press any key to set it.
5. Once saved, your recording appears in the dropdown and in the `recordings/` folder.

> 🎼 You can instantly replay any saved recording using its assigned shortcut key.

---

## 🧩 **How It Works**

* Uses **Pygame mixer channels** to play up to 52 notes simultaneously.
* Each key press triggers a sound from `assets/` mapped to the current octave.
* Recordings store timing, duration, and sound path as event dictionaries.
* **Pydub** overlays recorded notes to produce a full `.wav` file asynchronously (via threads).

---

## 📦 **Dependencies**

| Library     | Purpose                                      |
| ----------- | -------------------------------------------- |
| `pygame`    | GUI rendering, key input, and audio playback |
| `pydub`     | Mixing and exporting `.wav` files            |
| `threading` | Handles non-blocking background exports      |

---

## 📜 **License**

This project is licensed under the **MIT License** — feel free to use, remix, and expand it for your own musical experiments.

---

## 👨‍💻 **Author**

**Nikhil** — *B.Tech Computer Science*
