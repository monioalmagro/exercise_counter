import cv2


class Example:
    def __init__(self) -> None:
        cap = cv2.VideoCapture("video_001.mp4")

        frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Get width and height
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # here I'm trying to write the new rotated video
        # Open the output video file before the loop, cv2.VideoWriter_fourcc(*"mp4v") = 0x7634706d
        newvideoR = cv2.VideoWriter(
            "example.mp4",
            cv2.VideoWriter_fourcc(*"mp4v"),
            50,
            (frame_width, frame_height),
        )

        # Original Frames
        # frames = []
        for i in range(frame_number):
            ret, frame = cap.read()
            # frames.append(frame)  # No need to append the original frames

            # here's where I try to rotate the video
            new = cv2.rotate(frame, cv2.ROTATE_180)

            cv2.imshow("output", new)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            newvideoR.write(new)

        newvideoR.release()
        cap.release()
        cv2.destroyAllWindows()
