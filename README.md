# **Pyano — A Virtual Piano with Recording, Playback & Shortcuts**

Pyano is a Python-based virtual piano built using python. You can play piano notes from your keyboard.
Play notes from your keyboard, record sessions, assign custom shortcuts, and replay your compositions.
<img width="1396" height="478" alt="image" src="https://github.com/user-attachments/assets/cf648bde-e5f8-463c-aece-d1b781a3aafe" />

---

## **Features**

* **Recording & Exporting** – Record your performances and export them as `.wav` files.
* **Shortcut Mappings** – Assign any key to replay saved recordings in a session.
* **Layered Playback** – It's possible to overlay multiple recordings.
* **Graphical Interface** – Real-time visual feedback on pressed keys.
* **Octave Shifting** – Move between octaves using arrow keys.

---

## **Installation**

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
> 
> You can skip this if you just want the playable piano without recording and playback features. (simple_pyano.py)
> 
> Install it ffmpeg via:
>
> * **Windows:** [Download from ffmpeg.org](https://ffmpeg.org/download.html)
> * **macOS:** `brew install ffmpeg`
> * **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`

---

## **How to Use**

Run the Full Version (with Recording & Shortcuts)

```bash
python pyano.py
```

Run the Simple Piano (basic playback only)

```bash
python simple_pyano.py
```

---
## **Recording and Shortcuts**

1. Press **Left Ctrl** to start recording.
2. Press **Left Ctrl** again to stop.
3. Enter a filename for the recording.
4. Choose whether to assign a shortcut key (`Y/N`). If yes, press any key to bind it.
5. Your recording appears in the dropdown and inside the `recordings/` folder.

Replay any saved recording using its assigned shortcut key in a session.

---
## **Keyboard Controls**

| Action                           | Key                     |
| -------------------------------- | ----------------------- |
| **Play Notes**                   | `W, E, R, T, Y...` etc. |
| **Start / Stop Recording**       | `Left Ctrl`             |
| **Toggle Sustain (Hold Notes)**  | `Space`                 |
| **Shift Octave Up**              | `→`                     |
| **Shift Octave Down**            | `←`                     |
| **Open / Close Dropdown**        | Click top dropdown      |
| **Left Ctrl**                    | Record                  |
| **Exit**                         | `Esc`                   |

---

## **How It Works**

* **Pygame mixer channels** handle up to 52 notes simultaneously.
* Each key triggers a corresponding sound from the `assets/` folder based on the active octave.
* Recordings store key events (timing, duration, and sound paths) as structured dictionaries.
* **Pydub** layers these sounds to generate `.wav` files asynchronously via threads.

---

## **Project Structure**

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

## **Dependencies**

| Library     | Purpose                                           |
| ----------- | ------------------------------------------------- |
| `pygame`    | GUI, keyboard input, and sound playback           |
| `pydub`     | Audio overlaying and exporting recordings         |
| `threading` | Background saving of `.wav` files                 |

---
