#!venv/bin/python
import os
import sys
from io import BytesIO
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

walk_dir = sys.argv[1]

counter = dict()
counter["APIC:"] = 0
counter["APIC:Cover"] = 0
counter["covr"] = 0
counter["other"] = 0

other = set()
for root, subdirs, files in os.walk(walk_dir):
    for file in files:
        fileName, fileExt = os.path.splitext(file)
        if fileExt == ".mp3":
            audioFile = MP3(os.path.join(root, file))
            if "APIC:" in audioFile.tags:
                counter["APIC:"] += 1
            elif "APIC:Cover" in audioFile.tags:
                counter["APIC:Cover"] += 1
            elif "covr" in audioFile.tags:
                counter["covr"] += 1
            else:
                counter["other"] += 1
                other.add(os.path.ajoin(root, file))

print("APIC:      - ", counter["APIC:"])
print("APIC:Cover - ", counter["APIC:Cover"])
print("covr       - ", counter["covr"])
print("other      - ", counter["other"])

for i in sorted(list(other)):
    print(i)

