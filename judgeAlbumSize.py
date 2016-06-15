#!venv/bin/python
import os
import sys
from io import BytesIO
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

walk_dir = sys.argv[1]

wrongSizedImages = set()
wrongBitRate = set()

for root, subdirs, files in os.walk(walk_dir):
    for file in files:
        fileName, fileExt = os.path.splitext(file)
        if fileExt == ".mp3":
            audioFile = MP3(os.path.join(root, file))
            if "APIC:" in audioFile.keys():
                stream = BytesIO(audioFile["APIC:"].data)
                img = Image.open(stream)
                if (img.size != (500, 500)):
                    wrongSizedImages.add((root, img.size))
                stream.close()
            elif "APIC:Cover" in audioFile.keys():
                stream = BytesIO(audioFile["APIC:Cover"].data)
                img = Image.open(stream)
                if (img.size != (500, 500)):
                    wrongSizedImages.add((root, img.size))
                stream.close()
            else:
                wrongSizedImages.add((root, (0, 0)))
        elif fileExt == ".m4a":
            audioFile = MP4(os.path.join(root, file))
            if "covr" in audioFile.keys():
                stream = BytesIO(audioFile["covr"][0])
                img = Image.open(stream)
                if (img.size != (500, 500)):
                    wrongSizedImages.add((root, img.size))
                stream.close()
            else:
                wrongSizedImages.add((root, (0,0)))

print("--------------------\nIncorrect Album Size\n--------------------")
for i in sorted(list(wrongSizedImages)):
    print(i[0], "-", i[1][0], "x", i[1][1])