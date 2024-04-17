import json
from pathlib import Path

from utils import create_dir


def convert_to_voc_format(json_path, out_dir, cls_dict):
    with open(json_path, mode="r") as f:
        data = json.load(f)

    metadata = data["metadata"]
    img_w = metadata["width"]
    img_h = metadata["height"]

    for frame_info in data["frames"]:
        image_name = frame_info["image"]
        annotations = frame_info["annotations"]

        txt_path = (Path(out_dir)/image_name).with_suffix(".txt")
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
                line += f" {norm_x:.6f} {norm_y:.6f} {norm_w:.6f} {norm_h:.6f}"
                out_file.write(f"{line}\n")

    print(f"VOC format text files created in directory: {out_dir}")


if __name__ == "__main__":
    json_path = "/home/jbkim/Documents/datasets/CCTV 추적 영상/Training/[라벨]휠체어_1/annotation_2111366.json"
    out_dir = "/home/jbkim/Documents/cctv_data"
    cls_dict = {
        "person": 0,
        "wheelchair": 1,
    }
    convert_to_voc_format(json_path=json_path, out_dir=out_dir, cls_dict=cls_dict)
