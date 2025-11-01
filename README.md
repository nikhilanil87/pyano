# ■ Pyano — A Virtual Piano with Recording, Playback, and Shortcuts
Pyano is a Python-based virtual piano built using **Pygame** and **Pydub**.
It allows you to play notes with your keyboard, record multiple sessions, assign shortcuts, and replay
your compositions seamlessly.
---
## ■ Features
- ■ **Playable Piano Interface** – Use your keyboard to play realistic piano notes.
- ■■ **Recording & Exporting** – Record performances and export them as `.wav` files.
- ■■ **Shortcut Mappings** – Assign any key to instantly replay saved recordings.
- ■ **Layered Playback** – Combine multiple recordings by overlaying audio.
- ■■ **Graphical Interface** – Visual white/black keys rendered with real-time color feedback.
- ■ **Octave Shifting** – Move octaves up or down with arrow keys.
- ■ **Threaded Saving** – Exports recordings in a background thread without freezing the GUI.
---
## ■■ Project Structure
```
Pyano/
■
■■■ main.py # Main application file (this script)
■■■ assets/
■ ■■■ buttons/
■ ■ ■■■ record_1.png
■ ■ ■■■ record_2.png
■ ■ ■■■ dd_1.png
■ ■ ■■■ dd_2.png
■ ■■■ A0.wav … C8.wav # All piano note audio files
■
■■■ recordings/ # Automatically created folder for saved performances
```
---
## ■■ Installation
### 1. Clone or download the repository
```bash
git clone https://github.com/yourusername/Pyano.git
cd Pyano
```
### 2. Install dependencies
Make sure you have **Python 3.9+** installed.
Then run:
```bash
pip install pygame pydub
```
> **Note:**
> `pydub` requires **ffmpeg**.
> Install it via:
> - Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html)
> - macOS: `brew install ffmpeg`
> - Linux (Debian/Ubuntu): `sudo apt install ffmpeg`
---
## ■ How to Use
### Start the Piano
```bash
python main.py
```
### Keyboard Controls
| Action | Key |
|--------|-----|
| **Play Notes** | Use keys `W, E, R, T, Y...` etc. |
| **Record / Stop Recording** | `Left Ctrl` |
| **Toggle Sustain (Hold Notes)** | `Space` |
| **Shift Octave Up** | `→` |
| **Shift Octave Down** | `←` |
| **Open / Close Dropdown** | Click top dropdown button |
| **Play Recording from Dropdown** | Click on recording name |
| **Exit** | `Esc` |
---
## ■ Recording and Shortcuts
1. Press **Left Ctrl** to start recording.
- Notes played will be saved with timing and duration.
2. Press **Left Ctrl** again to stop.
3. You’ll be asked to **enter a filename** for the recording.
4. Then choose whether to assign a **shortcut key** (`Y/N`).
- If yes, press any key to set it.
5. Once saved, the recording will appear in the dropdown and in the `recordings/` folder.
> ■ You can replay any saved recording instantly by pressing its assigned shortcut key.
---
## ■ How It Works
- Uses **Pygame mixer channels** to handle up to 52 simultaneous notes.
- Each key press triggers a sound from `assets/` mapped to the selected octave.
- Recordings store note timing, duration, and sound paths as event dictionaries.
- **Pydub** overlays these events to construct a full `.wav` file asynchronously via threads.
---
## ■ Dependencies
| Library | Purpose |
|----------|----------|
| `pygame` | GUI, key input, audio playback |
| `pydub` | Mixing and exporting `.wav` files |
| `threading` | Non-blocking audio export |
---
## ■ License
This project is licensed under the **MIT License** — feel free to use and modify it for your own musical
experiments.
---
## ■■■ Author
**Nikhil** — B.Tech Computer Science
Building projects that blend **code and creativity** ■
