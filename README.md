# photo-every-day
This project automatically creates a timelapse video from daily pictures. Images are processed and aligned using face detection and facial landarking in order to ensure consistent framing.

## Requirements (+my versions)
* dLib (19.24.4)
* OpenCV (4.10.0.84)
* NumPy (1.26.4)

## Installation
1. Download the repository
2. Install the required libraries
3. Create a folder in documents named "photo_every_day"

## Usage
* Once you take your picture for the day name it whatever the day number is. Ex: "1", "34", "96"
* Add the picture to the photo_every_day folder (make sure every picture has the same resolution)
* Press run and the video will be created in the same folder

## Troubleshooting/Known Issues
1. In some images the face may not be detected. In this case retake the image with better lighting. You may also want to use higher resolution images.
2. If there are multiple people in an image the wrong face may be detected. Retake the picture with the desired face being the biggest and most centered.

## Customization
* You can change the frame rate to make the video slower or faster (second section of create_video())


