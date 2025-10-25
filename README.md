# 🎹 Pyano

**Pyano** is a virtual piano built with **Pygame**, featuring real `.wav` key sounds, octave shifting, sustain toggle, and visual key feedback.  
Play directly from your keyboard — no MIDI device needed!

---

## 🧩 Features
- Realistic piano sounds (C3–C6 range)
- 4 simultaneous octaves
- Visual on-screen keyboard
- Key press highlighting
- Sustain mode (toggle with **SPACE**)
- Octave shifting (**← / →** keys)
- Modular setup for adding more keys or effects

---

## 🕹️ Controls
| Action | Key |
|--------|-----|
| Play note | Assigned key (A–L, W–I, etc.) |
| Sustain toggle | `SPACE` |
| Shift octave up | `RIGHT ARROW` |
| Shift octave down | `LEFT ARROW` |
| Exit | `ESC` or window close |

---

## 🛠️ Requirements
- Python 3.9+
- [Pygame](https://www.pygame.org/)
- (Optional) [pydub](https://github.com/jiaaro/pydub) for recording extensions

Install with:
```bash
pip install pygame pydub
