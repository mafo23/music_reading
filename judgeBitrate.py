#!venv/bin/python
import os
import sys
from io import BytesIO
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

walk_dir = sys.argv[1]

wrongBitRate = set()

for root, subdirs, files in os.walk(walk_dir):
    for file in files:
        fileName, fileExt = os.path.splitext(file)
        if fileExt == ".mp3":
            audioFile = MP3(os.path.join(root, file))
            if (int(audioFile.info.bitrate)/1000) < 320:
                wrongBitRate.add((os.path.join(root, file), int(audioFile.info.bitrate)/1000))
        elif fileExt == ".m4a":
            audioFile = MP4(os.path.join(root, file))
            if (int(audioFile.info.bitrate)/1000) < 256:
                wrongBitRate.add((os.path.join(root, file), int(audioFile.info.bitrate)/1000))

print("--------------------\n Incorrect Bitrate  \n--------------------")
for i in sorted(list(wrongBitRate)):
    print(i[0], "-", i[1])