import face_recognition
import cv2
import numpy as np


def capture_face_encoding():
    """
    Opens webcam with live preview.
    Press 'q' to capture frame.
    Returns 128-d face encoding (numpy array) or None.
    """

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[FaceAuth] ERROR: Webcam not accessible.")
        return None

    print("[FaceAuth] Press 'q' to capture face.")

    encoding = None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("[FaceAuth] ERROR: Failed to read frame.")
            break

        cv2.imshow("Face Capture - Press Q", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_frame)

            if len(encodings) > 0:
                encoding = encodings[0]
                print("[FaceAuth] Face captured successfully.")
            else:
                print("[FaceAuth] No face detected in captured frame.")

            break

        elif key == ord('x'):
            print("[FaceAuth] Capture cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()

    return encoding


def verify_face(stored_encoding, new_encoding, tolerance=0.6):
    """
    Compare stored encoding with newly captured encoding.
    Returns True if match, False otherwise.
    """

    if stored_encoding is None or new_encoding is None:
        return False

    stored = np.array(stored_encoding)

    results = face_recognition.compare_faces(
        [stored],
        new_encoding,
        tolerance=tolerance
    )

    distance = face_recognition.face_distance(
        [stored],
        new_encoding
    )

    print(f"[FaceAuth] Face distance: {distance[0]:.4f} | Match: {results[0]}")

    return results[0]
