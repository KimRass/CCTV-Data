from pathlib import Path
import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_root", type=str, required=True)

    args = parser.parse_args()

    args_dict = vars(args)
    new_args_dict = dict()
    for k, v in args_dict.items():
        new_args_dict[k.upper()] = v
    args = argparse.Namespace(**new_args_dict)
    return args


def main():
    args = get_args()

    img_paths = list(Path(args.DATA_ROOT).glob("**/*.jpg"))
    for img_path in img_paths:
        txt_path = img_path.with_suffix(".txt")
        if not txt_path.exists():
            print(img_path)

    txt_paths = list(Path(args.DATA_ROOT).glob("**/*.txt"))
    for txt_path in txt_paths:
        img_path = txt_path.with_suffix(".jpg")
        if not img_path.exists():
            print(str(txt_path))

    print(len(list(img_paths)), len(list(txt_paths)))


if __name__ == "__main__":
    main()
