import json
from pathlib import Path
import shutil
import argparse

from utils import create_dir


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_root", type=str, required=True)
    parser.add_argument("--out_dir", type=str, required=True)

    args = parser.parse_args()

    args_dict = vars(args)
    new_args_dict = dict()
    for k, v in args_dict.items():
        new_args_dict[k.upper()] = v
    args = argparse.Namespace(**new_args_dict)
    return args


def move_imgs(data_root, out_dir):
    for img_path in Path(data_root).glob("**/*.jpg"):
            split = img_path.parents[4].name
            dst_path = Path(out_dir)/split/img_path.relative_to(
                img_path.parents[3]
            )
            create_dir(dst_path)
            shutil.copy(img_path, dst_path)


def create_txt_file(json_path, out_dir, cls_dict):
    json_path = Path(json_path)
    out_dir = Path(out_dir)
    split = json_path.parents[3].name

    with open(json_path, mode="r") as f:
        data = json.load(f)

    metadata = data["metadata"]
    img_w = metadata["width"]
    img_h = metadata["height"]
    vid_id = data["id"]

    for frame_info in data["frames"]:
        image_name = frame_info["image"]
        annotations = frame_info["annotations"]

        txt_path = (out_dir/split/json_path.relative_to(
            json_path.parents[2]
        ).parent/str(vid_id)/image_name).with_suffix(".txt")
        img_path = txt_path.with_suffix(".jpg")
        if img_path.exists():
            create_dir(txt_path)
            with open(str(txt_path), mode="w") as out_file:
                for annotation in annotations:
                    cls_name = annotation["category"]["code"]
                    cls_idx = cls_dict[cls_name]
                    bbox = annotation["label"]

                    l = bbox["x"]
                    t = bbox["y"]
                    w = bbox["width"]
                    h = bbox["height"]
                    r = l + w
                    b = t + h
                    x = (l + r) / 2
                    y = (t + b) / 2
                    norm_x = x / img_w
                    norm_y = y / img_h
                    norm_w = w / img_w
                    norm_h = h / img_h

                    line = f"{cls_idx}"
                    line += f" {norm_x:.6f} {norm_y:.6f}"
                    line += f" {norm_w:.6f} {norm_h:.6f}"
                    out_file.write(f"{line}\n")


def main():
    args = get_args()

    move_imgs(data_root=args.DATA_ROOT, out_dir=args.OUT_DIR)
    cls_dic = {
        "person": 0,
        "wheelchair": 1,
        "stroller": 2,
        "drunk": 0,
        "blind": 0,
        "merchant": 0,
        "child": 0,
    }
    for json_path in Path(args.DATA_ROOT).glob("**/*.json"):
        create_txt_file(
            json_path=json_path, out_dir=args.OUT_DIR, cls_dict=cls_dic,
        )


if __name__ == "__main__":
    main()
