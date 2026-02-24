import cv2

# ── appearance ────────────────────────────────────────────────────────────────
LED_COUNT = 13
RADIUS = 20
GLOW_RADIUS = RADIUS + 5
COLOR_ON = (255, 0, 200)    # purple (BGR)
COLOR_OFF = (253, 255, 245) # near-white (BGR)

# ── position ──────────────────────────────────────────────────────────────────
LED_START_X = 100
LED_START_Y = 50
LED_SPACING = (RADIUS * 2) + 10

# How close the fingertip must be to trigger a LED
HIT_FACTOR = 0.8


def draw_leds(frame, leds_status: int):
    # draws all LED circles on the frame, lit or unlit based on leds_status
    led_positions = []
    x = LED_START_X

    for i in range(LED_COUNT):
        pos = (x, LED_START_Y)
        if leds_status >= i:
            cv2.circle(frame, pos, GLOW_RADIUS, COLOR_OFF, -1)
            cv2.circle(frame, pos, RADIUS, COLOR_ON, -1)
        else:
            cv2.circle(frame, pos, RADIUS, COLOR_OFF, -1)

        led_positions.append((x, LED_START_Y, i))
        x += LED_SPACING

    return led_positions, frame


def check_finger_hit(fingertip_x: int, fingertip_y: int, led_positions: list):
    # returns the index of the LED being hovered over, or None
    hit_radius = int(RADIUS * HIT_FACTOR)
    for lx, ly, idx in led_positions:
        if (lx - hit_radius) <= fingertip_x <= (lx + hit_radius) and (ly - hit_radius) <= fingertip_y <= (ly + hit_radius):
            return idx
    return None
