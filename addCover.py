#!venv/bin/python
import os
import sys
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import APIC
from PIL import Image
from io import BytesIO

walk_dir = sys.argv[1]

for root, subdirs, files in os.walk(walk_dir):
    for file in files:
        fileName, fileExt = os.path.splitext(file)
        if fileExt == ".mp3":
            audioFile = MP3(os.path.join(root, file))
            if "APIC:" in audioFile.keys():
                audioFile.tags.pop("APIC:")
            image = Image.open(os.path.join(root, "cover.jpg"))
            stream = BytesIO()
            image.save(stream, format="JPEG")
            try:
                audioFile.add_tags()
            except:
                pass
            audioFile.tags.add(APIC(encoding = 3, mime = u"image/jpeg", type = 3, desc = u"Cover", data = stream.getvalue()))
            audioFile.save()

        elif fileExt == ".m4a":
            audioFile = MP4(os.path.join(root, file))
            if "covr" in audioFile.keys():
                audioFile.tags.pop("covr")
            covr = []
            image = Image.open(os.path.join(root, "cover.jpg"))
            stream = BytesIO()
            image.save(stream, format="JPEG")
            covr.append(MP4Cover(stream.getvalue(), MP4Cover.FORMAT_JPEG))
            audioFile["covr"] = covr
            audioFile.save()

