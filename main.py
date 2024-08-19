import cv2
import numpy as np
import dlib
import os
import math


# creates video
def create_video():

    # gets directories for picture and video
    home_dir = os.path.expanduser("~")
    documents_dir = os.path.join(home_dir, "Documents")
    photos_dir = os.path.join(documents_dir, "photo_every_day")
    video_path = os.path.join(photos_dir, "video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # sets frame rate
    frame_rate = 8

    # list all files in directory
    files = os.listdir(photos_dir)

    jpg_files = []

    # add .jpg files to array
    for file in files:
        if file.endswith('.jpg'):
            jpg_files.append(file)

    photo_paths = []

    # add photo paths
    for file in jpg_files:
        photo_paths.append(os.path.join(photos_dir, file))

    # sort photo paths
    photo_paths.sort()

    # check for photos
    if not photo_paths:
        print("No photos available")
        return

    # Adjust photo resolution for easier processing
    photo = cv2.imread(photo_paths[0])
    win_width = photo.shape[1]
    win_height = photo.shape[0]
    if win_width or win_height > 1500:
        gcd = math.gcd(win_width, win_height)
        win_width /= gcd
        win_height /= gcd
        while win_width < 1000 and win_height < 1000:
            win_width *= 2
            win_height *= 2
        win_width = int(win_width)
        win_height = int(win_height)

    # initialize video writer
    out = cv2.VideoWriter(video_path, fourcc, frame_rate, (win_width, win_height))

    # add each photo to video
    for photo_path in photo_paths:
        photo = cv2.imread(photo_path)
        photo = cv2.resize(photo, (win_width, win_height))
        photo = process_image(photo, win_width, win_height)
        out.write(photo)
        print("working...")

    out.release()


# resizes image according to desired eye distance
def resize_image(image, landmarks, win_width, win_height):

    left_eye_center_x = (landmarks.part(37).x + landmarks.part(40).x) / 2
    right_eye_center_x = (landmarks.part(43).x + landmarks.part(46).x) / 2

    image_eye_dist = right_eye_center_x - left_eye_center_x
    desired_eye_dist = win_width/10

    resize_factor = desired_eye_dist/image_eye_dist

    resized_image = cv2.resize(image, (int(win_width * resize_factor), int(win_height * resize_factor)))

    return resized_image


# finds angles between eyes and adjusts accordingly in order to level them
def rotate_image(image, landmarks):

    angle_degrees = 0

    left_eye_x = (landmarks.part(37).x + landmarks.part(40).x) / 2
    right_eye_x = (landmarks.part(43).x + landmarks.part(46).x) / 2
    left_eye_y = (landmarks.part(37).y + landmarks.part(40).y) / 2
    right_eye_y = (landmarks.part(43).y + landmarks.part(46).y) / 2

    image_center_x = image.shape[1] / 2
    image_center_y = image.shape[0] / 2

    dist_y = abs(left_eye_y - right_eye_y)
    dist_x = abs(right_eye_x - left_eye_x)
    angle_radians = np.arctan(dist_y / dist_x)
    angle_degrees = np.degrees(angle_radians)

    if right_eye_y < left_eye_y:
        angle_degrees = -angle_degrees

    M = cv2.getRotationMatrix2D((image_center_x, image_center_y), angle_degrees, 1)
    rotated_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return rotated_image


# translates image so that eyes are in desired position
def translate_image(image, landmarks, win_width, win_height):

    left_eye_center_x = (landmarks.part(37).x + landmarks.part(40).x) / 2
    right_eye_center_x = (landmarks.part(43).x + landmarks.part(46).x) / 2

    eyes_center_x = int((right_eye_center_x + left_eye_center_x) / 2)
    eyes_center_y = landmarks.part(28).y

    screen_center_x = win_width / 2
    screen_center_y = win_height / 2

    offset_x = int(screen_center_x - eyes_center_x)
    offset_y = int(screen_center_y - eyes_center_y)

    M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
    translated_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return translated_image


def process_image(image, win_width, win_height):

    # set up detector and predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # resize image
    gray_og = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_og, 0)
    if len(faces) == 0:
        print("no faces found (original)")
        return
    landmarks = predictor(gray_og, faces[0])
    resized_image = resize_image(image, landmarks, win_width, win_height)

    # rotate image
    gray_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_resized, 0)
    if len(faces) == 0:
        print("no faces found (resized)")
        return
    landmarks = predictor(gray_resized, faces[0])
    rotated_image = rotate_image(resized_image, landmarks)

    # translate image
    gray_rotated = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_rotated, 0)
    if len(faces) == 0:
        print("no faces found (rotated)")
        return
    landmarks = predictor(gray_rotated, faces[0])
    translated_image = translate_image(rotated_image, landmarks, win_width, win_height)

    # crop image to desired dimensions
    final_image = translated_image[0:win_height, 0:win_width]

    # add black space if image smaller than desired dimensions
    img_width = final_image.shape[1]
    img_height = final_image.shape[0]
    if img_width < win_width or img_height < win_height:
        right_pixels = max(0, win_width - img_width)
        bottom_pixels = max(0, win_height - img_height)
        final_image = cv2.copyMakeBorder(final_image, 0, bottom_pixels, 0, right_pixels, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return final_image


create_video()
