import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(48) # 48 for 4 octaves

sustain = True

# 1. Load 4 octave sounds
# 2. display UI

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

SCREEN_WIDTH = 7 * WHITE_KEY_WIDTH
SCREEN_HEIGHT = WHITE_KEY_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Pyano")

# --- Sounds ---
notes_and_keys = {
    pygame.mixer.Sound("assets/A0.wav"): pygame.K_TAB,
    pygame.mixer.Sound("assets/B0.wav"): pygame.K_q,
    pygame.mixer.Sound("assets/A#0.wav"): pygame.K_1,

    pygame.mixer.Sound("assets/C4.wav"): pygame.K_w,
    pygame.mixer.Sound("assets/C#4.wav"): pygame.K_3,
    pygame.mixer.Sound("assets/D4.wav"): pygame.K_e,
    pygame.mixer.Sound("assets/D#4.wav"): pygame.K_4,
    pygame.mixer.Sound("assets/E4.wav"): pygame.K_r,
    pygame.mixer.Sound("assets/F4.wav"): pygame.K_t,
    pygame.mixer.Sound("assets/F#4.wav"): pygame.K_6,
    pygame.mixer.Sound("assets/G4.wav"): pygame.K_y,
    pygame.mixer.Sound("assets/G#4.wav"): pygame.K_7,
    pygame.mixer.Sound("assets/A4.wav"): pygame.K_u,
    pygame.mixer.Sound("assets/A#4.wav"): pygame.K_8,
    pygame.mixer.Sound("assets/B4.wav"): pygame.K_i,

    pygame.mixer.Sound("assets/C5.wav"): pygame.K_o,
    pygame.mixer.Sound("assets/C#5.wav"): pygame.K_0,
    pygame.mixer.Sound("assets/D5.wav"): pygame.K_p,
    pygame.mixer.Sound("assets/D#5.wav"): pygame.K_MINUS,
    pygame.mixer.Sound("assets/E5.wav"): pygame.K_LEFTBRACKET,
    pygame.mixer.Sound("assets/F5.wav"): pygame.K_RIGHTBRACKET,
    pygame.mixer.Sound("assets/F#5.wav"): pygame.K_BACKSPACE,
    pygame.mixer.Sound("assets/G5.wav"): pygame.K_BACKSLASH,
    pygame.mixer.Sound("assets/G#5.wav"): pygame.K_NUMLOCK,
    pygame.mixer.Sound("assets/A5.wav"): pygame.K_KP7,
    pygame.mixer.Sound("assets/A#5.wav"): pygame.K_KP_DIVIDE,
    pygame.mixer.Sound("assets/B5.wav"): pygame.K_KP8,

    pygame.mixer.Sound("assets/C6.wav"): pygame.K_LSHIFT,
    pygame.mixer.Sound("assets/C#6.wav"): pygame.K_a,
    pygame.mixer.Sound("assets/D6.wav"): pygame.K_z,
    pygame.mixer.Sound("assets/D#6.wav"): pygame.K_s,
    pygame.mixer.Sound("assets/E6.wav"): pygame.K_x,
    pygame.mixer.Sound("assets/F6.wav"): pygame.K_c,
    pygame.mixer.Sound("assets/F#6.wav"): pygame.K_d,
    pygame.mixer.Sound("assets/G6.wav"): pygame.K_v,
    pygame.mixer.Sound("assets/G#6.wav"): pygame.K_f,
    pygame.mixer.Sound("assets/A6.wav"): pygame.K_b,
    pygame.mixer.Sound("assets/A#6.wav"): pygame.K_g,
    pygame.mixer.Sound("assets/B6.wav"): pygame.K_n,

    pygame.mixer.Sound("assets/C7.wav"): pygame.K_m,
    pygame.mixer.Sound("assets/C#7.wav"): pygame.K_k,
    pygame.mixer.Sound("assets/D7.wav"): pygame.K_COMMA,
    pygame.mixer.Sound("assets/D#7.wav"): pygame.K_l,
    pygame.mixer.Sound("assets/E7.wav"): pygame.K_PERIOD,
    pygame.mixer.Sound("assets/F7.wav"): pygame.K_SLASH,
    pygame.mixer.Sound("assets/F#7.wav"): pygame.K_QUOTE,
    pygame.mixer.Sound("assets/G7.wav"): pygame.K_RSHIFT,
    pygame.mixer.Sound("assets/G#7.wav"): pygame.K_RETURN,
    pygame.mixer.Sound("assets/A7.wav"): pygame.K_KP_1,
    pygame.mixer.Sound("assets/A#7.wav"): pygame.K_KP5,
    pygame.mixer.Sound("assets/B7.wav"): pygame.K_KP_2,

    pygame.mixer.Sound("assets/C8.wav"): pygame.K_KP3,
}

sounds = notes_and_keys.keys()

# notes = notes_and_keys.keys()
# keys = notes_and_keys.values()
# sounds = list(zip(keys, notes))

# print(sounds)

# We have four octaves at a time

pressed_keys = set()


# channels = {k: pygame.mixer.Channel(i) for i, k in enumerate(sounds.keys())}
#the og sounds was a list of pygame.mixer.sound(file)

# key_objects

keys = [[
    pygame.K_w,
    pygame.K_3,
    pygame.K_e,
    pygame.K_4,
    pygame.K_r,
    pygame.K_t,
    pygame.K_6,
    pygame.K_y,
    pygame.K_7,
    pygame.K_u,
    pygame.K_8,
    pygame.K_i,
],
[
    pygame.K_o,
    pygame.K_0,
    pygame.K_p,
    pygame.K_MINUS,
    pygame.K_LEFTBRACKET,
    pygame.K_RIGHTBRACKET,
    pygame.K_BACKSPACE,
    pygame.K_BACKSLASH,
    pygame.K_KP7,
    pygame.K_NUMLOCK,
    pygame.K_KP8,
    pygame.K_KP_DIVIDE,
],
[
    pygame.K_LSHIFT,
    pygame.K_a,
    pygame.K_z,
    pygame.K_s,
    pygame.K_x,
    pygame.K_d,
    pygame.K_c,
    pygame.K_v,
    pygame.K_b,
    pygame.K_n,

    pygame.K_f,
    pygame.K_g,
],
[

    pygame.K_m,
    pygame.K_COMMA,
    pygame.K_PERIOD,
    pygame.K_SLASH,
    pygame.K_RSHIFT,
    pygame.K_KP_1,
    pygame.K_KP_2,

    pygame.K_k,
    pygame.K_l,
    pygame.K_QUOTE,
    pygame.K_RETURN,
    pygame.K_KP5,
]]



channels = {}
sounds = {}

def set_octaves(octaves):
    channels.clear()
    n_channels = 0
    for i, octave in enumerate(octaves):
        for j, note in enumerate(['C','C#','D','D#','E','F','F#','G','G#', 'A', 'A#', 'B']):
            channels[keys[i][j]] = pygame.mixer.Channel(n_channels)
            sounds[keys[i][j]] = pygame.mixer.Sound(f'assets/{note}{octave}.wav')
            n_channels += 1

octaves = [3, 4, 5, 6]

set_octaves(octaves)

OCTAVE_WHITE_KEYS = [
    pygame.K_TAB,
    pygame.K_q,
    pygame.K_w,
    pygame.K_r,
    pygame.K_t,
    pygame.K_y,
    pygame.K_u
]

OCTAVE_BLACK_KEYS = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5
]


# --- Game loop ---
running = True
while running:
    screen.fill(PINK)
    width = 0
    for i, key in enumerate(OCTAVE_WHITE_KEYS):
        white_rect = pygame.Rect(i * WHITE_KEY_WIDTH, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT)
        color = BLUE if key in pressed_keys else WHITE
        pygame.draw.rect(screen, color, white_rect)
        pygame.draw.rect(screen, (55, 60, 69), white_rect, 1)

    for i, key in enumerate(OCTAVE_WHITE_KEYS):
            if i != 2 and i != 6:
                black_x = i * WHITE_KEY_WIDTH + (WHITE_KEY_WIDTH - BLACK_KEY_WIDTH / 2)
                black_rect = pygame.Rect(black_x, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
                color = GRAY if key in pressed_keys else BLACK
                pygame.draw.rect(screen, color, black_rect)
                pygame.draw.rect(screen, (55, 60, 69), black_rect, 5)

    # print(pressed_keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in sounds:
                channels[event.key].stop()
                channels[event.key].play(sounds[event.key], loops=0)
                pressed_keys.add(event.key)
            elif event.key == pygame.K_SPACE:
                sustain = not sustain
            
        elif event.type == pygame.KEYUP:
            if event.key in sounds:
                if not sustain:
                    channels[event.key].stop()
                pressed_keys.discard(event.key)


    pygame.display.flip()

pygame.quit()


#######################################################

# FOUR OCTAVES AVAILABLE AT A TIME
# OCTAVES USED BY DEFAULT - 3,4,5,6


# sound_objects = sounds = [

#     # Octave 0
#     pygame.mixer.Sound("assets/A0.wav"),
#     pygame.mixer.Sound("assets/A#0.wav"),
#     pygame.mixer.Sound("assets/B0.wav"),


#     # Octave 1
#     pygame.mixer.Sound("assets/C1.wav"),
#     pygame.mixer.Sound("assets/C#1.wav"),
#     pygame.mixer.Sound("assets/D1.wav"),
#     pygame.mixer.Sound("assets/D#1.wav"),
#     pygame.mixer.Sound("assets/E1.wav"),
#     pygame.mixer.Sound("assets/F1.wav"),
#     pygame.mixer.Sound("assets/F#1.wav"),
#     pygame.mixer.Sound("assets/G1.wav"),
#     pygame.mixer.Sound("assets/G#1.wav"),
#     pygame.mixer.Sound("assets/A1.wav"),
#     pygame.mixer.Sound("assets/A#1.wav"),
#     pygame.mixer.Sound("assets/B1.wav"),


#     # Octave 2
#     pygame.mixer.Sound("assets/C2.wav"),
#     pygame.mixer.Sound("assets/C#2.wav"),
#     pygame.mixer.Sound("assets/D2.wav"),
#     pygame.mixer.Sound("assets/D#2.wav"),
#     pygame.mixer.Sound("assets/E2.wav"),
#     pygame.mixer.Sound("assets/F2.wav"),
#     pygame.mixer.Sound("assets/F#2.wav"),
#     pygame.mixer.Sound("assets/G2.wav"),
#     pygame.mixer.Sound("assets/G#2.wav"),
#     pygame.mixer.Sound("assets/A2.wav"),
#     pygame.mixer.Sound("assets/A#2.wav"),
#     pygame.mixer.Sound("assets/B2.wav"),


#     # Octave 3
#     pygame.mixer.Sound("assets/C3.wav"),
#     pygame.mixer.Sound("assets/C#3.wav"),
#     pygame.mixer.Sound("assets/D3.wav"),
#     pygame.mixer.Sound("assets/D#3.wav"),
#     pygame.mixer.Sound("assets/E3.wav"),
#     pygame.mixer.Sound("assets/F3.wav"),
#     pygame.mixer.Sound("assets/F#3.wav"),
#     pygame.mixer.Sound("assets/G3.wav"),
#     pygame.mixer.Sound("assets/G#3.wav"),
#     pygame.mixer.Sound("assets/A3.wav"),
#     pygame.mixer.Sound("assets/A#3.wav"),
#     pygame.mixer.Sound("assets/B3.wav"),


#     # Octave 4
#     pygame.mixer.Sound("assets/C4.wav"),
#     pygame.mixer.Sound("assets/C#4.wav"),
#     pygame.mixer.Sound("assets/D4.wav"),
#     pygame.mixer.Sound("assets/D#4.wav"),
#     pygame.mixer.Sound("assets/E4.wav"),
#     pygame.mixer.Sound("assets/F4.wav"),
#     pygame.mixer.Sound("assets/F#4.wav"),
#     pygame.mixer.Sound("assets/G4.wav"),
#     pygame.mixer.Sound("assets/G#4.wav"),
#     pygame.mixer.Sound("assets/A4.wav"),
#     pygame.mixer.Sound("assets/A#4.wav"),
#     pygame.mixer.Sound("assets/B4.wav"),


#     # Octave 5
#     pygame.mixer.Sound("assets/C5.wav"),
#     pygame.mixer.Sound("assets/C#5.wav"),
#     pygame.mixer.Sound("assets/D5.wav"),
#     pygame.mixer.Sound("assets/D#5.wav"),
#     pygame.mixer.Sound("assets/E5.wav"),
#     pygame.mixer.Sound("assets/F5.wav"),
#     pygame.mixer.Sound("assets/F#5.wav"),
#     pygame.mixer.Sound("assets/G5.wav"),
#     pygame.mixer.Sound("assets/G#5.wav"),
#     pygame.mixer.Sound("assets/A5.wav"),
#     pygame.mixer.Sound("assets/A#5.wav"),
#     pygame.mixer.Sound("assets/B5.wav"),


#     # Octave 6
#     pygame.mixer.Sound("assets/C6.wav"),
#     pygame.mixer.Sound("assets/C#6.wav"),
#     pygame.mixer.Sound("assets/D6.wav"),
#     pygame.mixer.Sound("assets/D#6.wav"),
#     pygame.mixer.Sound("assets/E6.wav"),
#     pygame.mixer.Sound("assets/F6.wav"),
#     pygame.mixer.Sound("assets/F#6.wav"),
#     pygame.mixer.Sound("assets/G6.wav"),
#     pygame.mixer.Sound("assets/G#6.wav"),
#     pygame.mixer.Sound("assets/A6.wav"),
#     pygame.mixer.Sound("assets/A#6.wav"),
#     pygame.mixer.Sound("assets/B6.wav"),


#     # Octave 7
#     pygame.mixer.Sound("assets/C7.wav"),
#     pygame.mixer.Sound("assets/C#7.wav"),
#     pygame.mixer.Sound("assets/D7.wav"),
#     pygame.mixer.Sound("assets/D#7.wav"),
#     pygame.mixer.Sound("assets/E7.wav"),
#     pygame.mixer.Sound("assets/F7.wav"),
#     pygame.mixer.Sound("assets/F#7.wav"),
#     pygame.mixer.Sound("assets/G7.wav"),
#     pygame.mixer.Sound("assets/G#7.wav"),
#     pygame.mixer.Sound("assets/A7.wav"),
#     pygame.mixer.Sound("assets/A#7.wav"),
#     pygame.mixer.Sound("assets/B7.wav"),

#     # Octave 8
#     pygame.mixer.Sound("assets/C8.wav"),
# ]

# #    pygame.K_TAB,
#     pygame.K_q,

#     pygame.K_1,


#the last one

    # pygame.K_KP3, c8 or somehting






