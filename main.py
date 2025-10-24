import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(52)

# --- Piano sound logic ---

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
    pygame.K_NUMLOCK,
    pygame.K_KP7,
    pygame.K_KP_DIVIDE,
    pygame.K_KP8,
],
[
    pygame.K_LSHIFT,
    pygame.K_a,
    pygame.K_z,
    pygame.K_s,
    pygame.K_x,
    pygame.K_c,
    pygame.K_f,
    pygame.K_v,
    pygame.K_g,
    pygame.K_b,
    pygame.K_h,
    pygame.K_n,
],
[
    pygame.K_m,
    pygame.K_k,
    pygame.K_COMMA,
    pygame.K_l,
    pygame.K_PERIOD,
    pygame.K_SLASH,
    pygame.K_QUOTE,
    pygame.K_RSHIFT,
    pygame.K_RETURN,
    pygame.K_KP_1,
    pygame.K_KP5,
    pygame.K_KP_2,
]]

channels = {}
sounds = {}
pressed_keys = set()

def set_octaves():
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
    

    for i, octave in enumerate(octaves):
        for j, note in enumerate(['C','C#','D','D#','E','F','F#','G','G#', 'A', 'A#', 'B']):
            channels[keys[i][j]] = pygame.mixer.Channel(n_channels)
            sounds[keys[i][j]] = pygame.mixer.Sound(f'assets/{note}{octave}.wav')
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

SCREEN_WIDTH = 28 * WHITE_KEY_WIDTH
SCREEN_HEIGHT = WHITE_KEY_HEIGHT + 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


WHITE_KEYS = []
BLACK_KEYS = []

def render_gui():
    pygame.display.set_caption(f'Pyano - Octaves {octaves}')
    screen.fill(BLACK)
    for i, key in enumerate(WHITE_KEYS):
        white_rect = pygame.Rect(i * WHITE_KEY_WIDTH, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT)
        color = BLUE if key in pressed_keys else WHITE
        pygame.draw.rect(screen, color, white_rect)
        pygame.draw.rect(screen, (55, 60, 69), white_rect, 1)

    black_key_index = 0
    for i, key in enumerate(WHITE_KEYS):
        if i%7 != 2 and i%7 != 6:
            black_x = i * WHITE_KEY_WIDTH + (WHITE_KEY_WIDTH - BLACK_KEY_WIDTH / 2)
            black_rect = pygame.Rect(black_x, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
            color = GRAY if BLACK_KEYS[black_key_index] in pressed_keys else BLACK
            pygame.draw.rect(screen, color, black_rect)
            pygame.draw.rect(screen, (55, 60, 69), black_rect, 5)
            black_key_index += 1
            

# --- Settings ---
sustain = True
is_recording = False
octaves = [3, 4, 5, 6]
set_octaves()


# --- Game loop ---
running = True
while running:

    render_gui()

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
            elif event.key == pygame.K_RIGHT:
                if octaves[-1] < 7:
                    octaves = [octave + 1 for octave in octaves]
                    set_octaves()
            elif event.key == pygame.K_LEFT:
                if octaves[0] > 1:
                    octaves = [octave - 1 for octave in octaves]
                    set_octaves()
            
        elif event.type == pygame.KEYUP:
            if event.key in sounds:
                if not sustain:
                    channels[event.key].stop()
                pressed_keys.discard(event.key)

    pygame.display.flip()

pygame.quit()