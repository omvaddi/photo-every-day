# automatic-daily-photo-editor
This project automatically creates a timelapse video from daily pictures. Images are processed and aligned using face detection and facial landarking in order to ensure consistent framing.

## Requirements (+my versions)
dLib (19.24.4)
OpenCV (4.10.0.84)
NumPy (1.26.4)

## Installation
1. Download the repository
2. Install the required libraries
3. Create a folder in documents named "photo_every_day"

## Usage
Once you take your picture for the day name it whatever the day number is. Ex: "1", "34", "96"
Add the picture to the photo_every_day folder
Press run and the video will be created in the same folder

## Troubleshooting/Known Problems
*In some cases faces may not be recognized. The best way to resolve this is to take the picture in better lighting.
*If there are multiple people in your picture the first face that is identified will be centered. 


