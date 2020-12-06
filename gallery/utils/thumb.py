import os, sys
import glob
from PIL import Image, ExifTags

size = 512, 512

for infile in glob.glob("../images/*.jpg"):
    print(infile)
    try:
        image = Image.open(infile)
        if hasattr(image, '_getexif'): # only present in JPEGs
            for orientation in ExifTags.TAGS.keys(): 
                if ExifTags.TAGS[orientation]=='Orientation':
                    break 
            e = image._getexif()       # returns None if no EXIF data
            if e is not None:
                exif=dict(e.items())
                if orientation in exif:
                    orientation = exif[orientation] 
                    if orientation == 3:   image = image.transpose(Image.ROTATE_180)
                    elif orientation == 6: image = image.transpose(Image.ROTATE_270)
                    elif orientation == 8: image = image.transpose(Image.ROTATE_90)

        image.thumbnail(size, Image.ANTIALIAS)
        outfile = os.path.splitext(infile)[0] + ".png"
        image.save(outfile, "PNG")
    except IOError:
        print("cannot create thumbnail for", infile)