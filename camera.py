import cv2
from config import CAMERA_SOURCE, CAMERA_NAME


class Camera:
    def __init__(self):
        print(f"\n🎥 Opening Camera: {CAMERA_NAME}")

        # Use DirectShow backend
        self.cap = cv2.VideoCapture(CAMERA_SOURCE, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            raise Exception("❌ Unable to open camera!")

        print("✅ Camera Connected Susccessfully!")

    def get_frame(self):
        success, frame = self.cap.read()

        if not success:
            print("❌ Failed to grab frame.")
            return None

        return frame

    def release(self):
        self.cap.release()


def main():
    camera = Camera()

    while True:
        frame = camera.get_frame()

        if frame is None:
            break

        cv2.imshow("CampusGuard Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()