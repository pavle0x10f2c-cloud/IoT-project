import cv2
import mediapipe as mp


class HandDetector:
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 1,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.6,
    ):
        self._mp_draw = mp.solutions.drawing_utils      #draws skeleton on frame
        self._mp_hands = mp.solutions.hands             #hand tracking model
        self._hands = self._mp_hands.Hands(             #activate with settings
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        ) 

    def find_hands(self, frame, draw: bool = True):
        # detect hands and return landmark positions
        h, w, _ = frame.shape 
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #mediapipe needs rgb not bgr
        results = self._hands.process(rgb)
        hands = []
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks: 
                # convert coordinations to pixel positions
                landmarks = [
                    (int(lm.x * w), int(lm.y * h), int(lm.z * w))
                    for lm in hand_lms.landmark 
                ]
                hands.append({"hlm_list": landmarks})
                if draw: # toggle skeleton with y/n in main
                    self._mp_draw.draw_landmarks(
                        frame, hand_lms, self._mp_hands.HAND_CONNECTIONS
                        )

        return hands, frame
