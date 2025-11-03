import pygame
from pydub import AudioSegment
import time
import os
import threading

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(52)

shortcut_map = {}  # key: pygame key, value: index of session_recordings
session_recordings = []

# --- Piano sound logic ---

keys = [[
    pygame.K_w, pygame.K_3, pygame.K_e, pygame.K_4, pygame.K_r, pygame.K_t,
    pygame.K_6, pygame.K_y, pygame.K_7, pygame.K_u, pygame.K_8, pygame.K_i,
], [
    pygame.K_o, pygame.K_0, pygame.K_p, pygame.K_MINUS, pygame.K_LEFTBRACKET,
    pygame.K_RIGHTBRACKET, pygame.K_BACKSPACE, pygame.K_BACKSLASH,
    pygame.K_NUMLOCK, pygame.K_KP7, pygame.K_KP_DIVIDE, pygame.K_KP8,
], [
    pygame.K_LSHIFT, pygame.K_a, pygame.K_z, pygame.K_s, pygame.K_x,
    pygame.K_c, pygame.K_f, pygame.K_v, pygame.K_g, pygame.K_b, pygame.K_h, pygame.K_n,
], [
    pygame.K_m, pygame.K_k, pygame.K_COMMA, pygame.K_l, pygame.K_PERIOD,
    pygame.K_SLASH, pygame.K_QUOTE, pygame.K_RSHIFT, pygame.K_RETURN,
    pygame.K_KP_1, pygame.K_KP5, pygame.K_KP_2,
]]

channels = {}
sounds = {}
pressed_keys = set()
sound_paths = {}
WHITE_KEYS = []
BLACK_KEYS = []
record_start_time = 0

def set_octaves():
    WHITE_KEYS.clear()
    BLACK_KEYS.clear()
    channels.clear()
    n_channels = 4

    channels[pygame.K_TAB] = pygame.mixer.Channel(0)
    channels[pygame.K_1] = pygame.mixer.Channel(1)
    channels[pygame.K_q] = pygame.mixer.Channel(2)
    channels[pygame.K_KP3] = pygame.mixer.Channel(3)

    sounds[pygame.K_TAB] = pygame.mixer.Sound("assets/A0.wav")
    sounds[pygame.K_1] = pygame.mixer.Sound("assets/A#0.wav")
    sounds[pygame.K_q] = pygame.mixer.Sound("assets/B0.wav")
    sounds[pygame.K_KP3] = pygame.mixer.Sound("assets/C8.wav")

    sound_paths[pygame.K_TAB] = "assets/A0.wav"
    sound_paths[pygame.K_1] = "assets/A#0.wav"
    sound_paths[pygame.K_q] = "assets/B0.wav"
    sound_paths[pygame.K_KP3] = "assets/C8.wav"

    for i, octave in enumerate(octaves):
        for j, note in enumerate(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']):
            channels[keys[i][j]] = pygame.mixer.Channel(n_channels)
            sounds[keys[i][j]] = pygame.mixer.Sound(f'assets/{note}{octave}.wav')
            sound_paths[keys[i][j]] = f'assets/{note}{octave}.wav'
            if '#' not in note:
                WHITE_KEYS.append(keys[i][j])
            else:
                BLACK_KEYS.append(keys[i][j])
            n_channels += 1

# --- GUI Setup ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (100, 180, 255)
PINK = (255,192,203)

WHITE_KEY_WIDTH = 50
WHITE_KEY_HEIGHT = 300
BLACK_KEY_WIDTH = WHITE_KEY_WIDTH / 1.7
BLACK_KEY_HEIGHT = WHITE_KEY_HEIGHT / 1.5
SETTINGS_HEIGHT = 150

SCREEN_WIDTH = 28 * WHITE_KEY_WIDTH
SCREEN_HEIGHT = WHITE_KEY_HEIGHT + SETTINGS_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

record_img_on = pygame.transform.scale(pygame.image.load("assets/buttons/record_2.png").convert_alpha(), (120, 50))
record_img_off = pygame.transform.scale(pygame.image.load("assets/buttons/record_1.png").convert_alpha(), (120, 50))
dd_1 = pygame.transform.scale(pygame.image.load("assets/buttons/dd_1.png").convert_alpha(), (175, 50))
dd_2 = pygame.transform.scale(pygame.image.load("assets/buttons/dd_2.png").convert_alpha(), (175, 50))
sus_on = pygame.transform.scale(pygame.image.load("assets/buttons/sus_on.png").convert_alpha(), (300, 60))
sus_off = pygame.transform.scale(pygame.image.load("assets/buttons/sus_off.png").convert_alpha(), (300, 60))

dropdown_open = False
selected_recording = None
dropdown_rect = pygame.Rect(200, 20, 180, 40)
sus_rect = pygame.Rect(400, 20, 175, 50)

# --- Recording / Playback ---

def export_audio_thread(events, output_path, filename, shortcut_key):
    global session_recordings, shortcut_map
    
    try:
        total_duration = max(e["start_time"] + e["duration"] for e in events)
        final_audio = AudioSegment.silent(duration=int(total_duration * 1000))

        for e in events:
            sound = AudioSegment.from_wav(e["sound_path"])
            
            note_audio = sound[:int(e["duration"] * 1000)]
            final_audio = final_audio.overlay(note_audio, position=int(e["start_time"] * 1000))

        final_audio.export(output_path, format="wav")

        session_recordings.append({
            "name": filename,
            "events": events,
            "file_path": output_path
        })
        
        recording_index = len(session_recordings) - 1
        print(f"Recording saved as {output_path} ({round(total_duration, 2)}s)")

        if shortcut_key:
            shortcut_map[shortcut_key] = recording_index
            print(f"Shortcut assigned: {pygame.key.name(shortcut_key)} → {filename}")

    except Exception as e:
        print(f"Error saving audio: {e}")

def stop_and_save_recording(events):
    if not events:
        print("No notes recorded.")
        return

    os.makedirs("recordings", exist_ok=True)
    
    filename, shortcut_key = get_filename_and_shortcut(f"Recording_{len(session_recordings)+1}")

    if filename:
        if not filename.lower().endswith(".wav"):
            filename += ".wav"
        
        output_path = os.path.join("recordings", filename)

        print("Saving audio in background...")
        threading.Thread(
            target=export_audio_thread, 
            args=(events, output_path, filename, shortcut_key), 
            daemon=True
        ).start()
    
    else:
        print("Recording discarded.")

def play_note_on(note_key):
    global playback_keys
    if note_key in channels:
        channels[note_key].play(sounds[note_key])
        playback_keys.add(note_key)

def play_note_off(note_key):
    global playback_keys
    if not sustain:
        channels[note_key].stop()
    playback_keys.discard(note_key)

def play_recording(events):
    if not events:
        print("No notes to play.")
        return

    playback_keys.clear() 

    for e in events:
        note_key = e["note"]
        start_time = e["start_time"]
        duration = e["duration"]
        

        threading.Timer(start_time, play_note_on, args=[note_key]).start()
        
        threading.Timer(duration, play_note_off, args=[note_key]).start()
            
# --- GUI Functions ---

def render_dropdown():
    if dropdown_open:
        screen.blit(dd_2, dropdown_rect.topleft)
    else:
        screen.blit(dd_1, dropdown_rect.topleft)

    if dropdown_open:
        font = pygame.font.Font(None, 28)
        for idx, rec in enumerate(session_recordings):
            item_rect = pygame.Rect(
                dropdown_rect.x,
                dropdown_rect.y + (idx + 1) * dropdown_rect.height,
                dropdown_rect.width,
                dropdown_rect.height
            )
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, PINK, item_rect)
            else:
                pygame.draw.rect(screen, BLUE, item_rect)
            pygame.draw.rect(screen, BLACK, item_rect, 2)
            item_text = font.render(rec["name"], True, BLACK)
            screen.blit(item_text, (item_rect.x + 10, item_rect.y + 8))

def render_gui():
    pygame.display.set_caption(f'Pyano - Octaves {octaves}')
    screen.fill((143, 140, 140))

    option_rect = pygame.Rect(55, SETTINGS_HEIGHT - 100, 60, 40)
    if is_recording:
        screen.blit(record_img_on, option_rect)
    else:
        screen.blit(record_img_off, option_rect)

    for i, key in enumerate(WHITE_KEYS):
        white_rect = pygame.Rect(i * WHITE_KEY_WIDTH, SETTINGS_HEIGHT, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT)
        
        color = BLUE if (key in pressed_keys or key in playback_keys) else WHITE
        
        pygame.draw.rect(screen, color, white_rect)
        pygame.draw.rect(screen, (55, 60, 69), white_rect, 1)

    black_key_index = 0
    for i, key in enumerate(WHITE_KEYS):
        if i % 7 != 2 and i % 7 != 6:
            if black_key_index < len(BLACK_KEYS): 
                black_x = i * WHITE_KEY_WIDTH + (WHITE_KEY_WIDTH - BLACK_KEY_WIDTH / 2)
                black_rect = pygame.Rect(black_x,  SETTINGS_HEIGHT, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
                
                black_key = BLACK_KEYS[black_key_index]
                
                color = GRAY if (black_key in pressed_keys or black_key in playback_keys) else BLACK
                
                pygame.draw.rect(screen, color, black_rect)
                pygame.draw.rect(screen, (55, 60, 69), black_rect, 5)
                black_key_index += 1
    render_dropdown()
    if sustain:
        screen.blit(sus_on, sus_rect.topleft)
    else:
        screen.blit(sus_off, sus_rect.topleft)



def get_filename_and_shortcut(default_name="Recording"):
    input_active = True
    user_text = default_name
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))

        label = font.render("Enter filename:", True, WHITE)
        screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, input_box.y - 40))
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = font.render(user_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 8))
        pygame.display.flip()

    shortcut_key = None
    ask_shortcut = True
    while ask_shortcut:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return user_text, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    print("Press a key to set as shortcut...")
                    shortcut_key = wait_for_keypress()
                    ask_shortcut = False
                elif event.key == pygame.K_n:
                    ask_shortcut = False

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))

        label = font.render("Set shortcut? (Y/N)", True, WHITE)
        screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - 20))
        pygame.display.flip()

    return user_text, shortcut_key

def wait_for_keypress():
    waiting = True
    font = pygame.font.Font(None, 32)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(f"Shortcut key set: {pygame.key.name(event.key)}")
                waiting = False
                return event.key
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        label = font.render("Press any key for shortcut...", True, WHITE)
        screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - 20))
        pygame.display.flip()

# --- Settings ---
sustain = True
is_recording = False
octaves = [3, 4, 5, 6]
set_octaves()
chord_shortcuts = {}
current_recording = []
record_start_time = None
active_notes = {}
num_recordings = 1
running = True
playback_keys = set()

# --- Event Handling ---

def get_inputs():
    global running, dropdown_open, selected_recording, sustain, is_recording, octaves, record_start_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in sounds:
                channels[event.key].stop()
                channels[event.key].play(sounds[event.key], loops=0)
                pressed_keys.add(event.key)
            
            if is_recording and event.key in sounds:
                start = time.time() - record_start_time
                active_notes[event.key] = start

            elif event.key == pygame.K_RIGHT:
                if octaves[-1] < 7:
                    octaves = [octave + 1 for octave in octaves]
                    set_octaves()
            elif event.key == pygame.K_LEFT:
                if octaves[0] > 1:
                    octaves = [octave - 1 for octave in octaves]
                    set_octaves()

            elif event.key == pygame.K_LCTRL:
                is_recording = not is_recording
                if is_recording:
                    print("Recording started...")
                    current_recording.clear()
                    record_start_time = time.time()
                    active_notes.clear()
                else:
                    print("Recording stopped.")
                    events_to_save = current_recording.copy()
                    stop_and_save_recording(events_to_save)

            elif event.key == pygame.K_ESCAPE:
                running = False

            if event.key in shortcut_map:
                rec_index = shortcut_map[event.key]
                rec = session_recordings[rec_index]
                print(f"Shortcut triggered: Playing {rec['name']}")
                play_recording(rec["events"])

                if is_recording:
                    shortcut_start_time = time.time() - record_start_time
                    for note_event in rec["events"]:
                        new_event = note_event.copy() 
                        new_event["start_time"] += shortcut_start_time
                        current_recording.append(new_event)

        elif event.type == pygame.KEYUP:
            if event.key in sounds:
                if not sustain:
                    channels[event.key].stop()
                pressed_keys.discard(event.key)

            if is_recording and event.key in active_notes:
                start_time = active_notes[event.key]
                
                duration = time.time() - record_start_time
                
                current_recording.append({
                    "event": event,
                    "sound_path": sound_paths[event.key],
                    "note": event.key,
                    "start_time": start_time,
                    "duration": duration
                })
                del active_notes[event.key]

            elif event.key == pygame.K_SPACE:
                sustain = not sustain

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if dropdown_rect.collidepoint(mx, my):
                dropdown_open = not dropdown_open
            
            elif dropdown_open and not dropdown_rect.collidepoint(mx, my):
                 dropdown_open = False

            if dropdown_open:
                for idx, rec in enumerate(session_recordings):
                    item_rect = pygame.Rect(
                        dropdown_rect.x,
                        dropdown_rect.y + (idx + 1) * dropdown_rect.height,
                        dropdown_rect.width,
                        dropdown_rect.height
                    )
                    if item_rect.collidepoint(mx, my):
                        selected_recording = idx
                        dropdown_open = False
                        print(f"Playing {rec['name']}...")
                        play_recording(rec["events"])
                        break
            
# --- Main Loop ---

def main_loop():
    global running
    clock = pygame.time.Clock()
    while running:
        get_inputs()
        render_gui()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main_loop()
