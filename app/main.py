import threading
import cv2
from dotenv import load_dotenv
from hand_detector import HandDetector
from led_ui import draw_leds, check_finger_hit
from esp_client import send_data_to_esp

load_dotenv()  # loads ESP_HOST and ESP_PORT from .env file

WINDOW_NAME = "Hand LED Controller"
CAM_WIDTH = 800
CAM_HEIGHT = 600


def main():
    cap = cv2.VideoCapture(0)  # 0 = first webcam, change if wrong camera opens
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

    detector = HandDetector()
    leds_status = 0     # current LED level, persists between frames
    show_skeleton = True

    print("Running — press Q to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[Camera] Failed to read frame — exiting.")
            break

        hands, frame = detector.find_hands(frame, draw=show_skeleton)
        led_positions, frame = draw_leds(frame, leds_status)

        if hands:
            fx, fy, _ = hands[0]["hlm_list"][8]  # landmark 8 = index fingertip
            hit = check_finger_hit(fx, fy, led_positions)

            if hit is not None and hit != leds_status:  # only send if level changed
                leds_status = hit
                print(f"[LED] Level set to {leds_status}")
                threading.Thread(  # send on background thread so video stays smooth
                    target=send_data_to_esp,
                    args=(leds_status,),
                    daemon=True,
                ).start()

        cv2.imshow(WINDOW_NAME, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("y"):
            show_skeleton = True
            print("skeleton ON")
        elif key == ord("n"):
            show_skeleton = False
            print("skeleton OFF")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
