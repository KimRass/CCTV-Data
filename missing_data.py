from pathlib import Path


DATA_ROOT = "/home/jbkim/Documents/datasets/cctv_data"

img_paths = list(Path(DATA_ROOT).glob("**/*.jpg"))
for img_path in img_paths:
    txt_path = img_path.with_suffix(".txt")
    if not txt_path.exists():
        print(img_path)

txt_paths = list(Path(DATA_ROOT).glob("**/*.txt"))
for txt_path in txt_paths:
    img_path = txt_path.with_suffix(".jpg")
    if not img_path.exists():
        print(str(txt_path))

print(len(list(img_paths)), len(list(txt_paths)))
