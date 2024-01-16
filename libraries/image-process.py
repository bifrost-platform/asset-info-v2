import math
import os

import cairosvg
from PIL import Image

pwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")

IMAGE_NAME = "image"

def get_svg_image_path (dirname: str) -> str:
  return os.path.join(dirname, f"{IMAGE_NAME}.svg")

def get_png_image_path (dirname: str, scale: int) -> str:
  return os.path.join(dirname, f"{IMAGE_NAME}-{scale}.png")

def downscale_png (dirname: str, scale: int):
  sizes = [ 2 ** i for i in range(5, math.floor(math.log2(scale - 1)) + 1) ]
  with Image.open(get_png_image_path(dirname, scale)) as img:
    for size in sizes:
      print(f"    > resize png {scale} to {size}")
      new_img = img.resize((size, size))
      new_img.save(get_png_image_path(dirname,size), "png", optimize=True)

def gen_png256_by_svg (dirname: str):
  with open(get_svg_image_path(dirname), "r") as fp:
    svg_code = fp.read()
    print(f"    > convert svg to png")
    cairosvg.svg2png(bytestring=svg_code, write_to=get_png_image_path(dirname, 256), output_width=256, output_height=256, dpi=300, scale=2)
  downscale_png(dirname, 256)

def search (dirname: str):
  for (path, _, files) in os.walk(dirname):
    print(f"> searching {path}")
    file_exts = [ os.path.splitext(filename)[-1] for filename in files ]
    if ".png" in file_exts:
      max_size = max([
        int(filename.replace(".png", "").replace("image-", ""))
        for filename in files
        if filename.startswith("image-") and filename.endswith(".png") ])
      print(f"  > processing png-{max_size} in {path}")
      downscale_png (path, max_size)
    elif ".svg" in file_exts:
      print(f"  > processing svg in {path}")
      gen_png256_by_svg(path)

search (pwd)
