import argparse
import json
import os
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-dir", type=str, default="./working")
    parser.add_argument("--upload-dir", type=str, default="./upload_models")
    parser.add_argument("--kaggle-username", type=str, default="stgkrtua")
    parser.add_argument("--competition", type=str, default="rsna2024")
    # parser.add_argument("--exp-name", type=str, default="debug")
    parser.add_argument("--exp-name-list", type=str, nargs="*", default=["debug"])
    parser.add_argument("--folds", type=int, nargs="*", default=[0, 1, 2, 3, 4])
    parser.add_argument("--upload-or-create", type=str, default="upload")
    args = parser.parse_args()
    target_files = [
        "best_official_weights.pth",
        "best_official_oof.csv",
        "final_weights.pth",
        "config_tree.log",
        "model_config.yaml",
        "train.log",
    ]
    uploading_dir = "/kaggle/kaggle_apis/upload_models"
    # src_dirがなければエラー
    for exp_name in args.exp_name_list:
        exp_dir = os.path.join(args.src_dir, exp_name)
        if not os.path.exists(exp_dir):
            raise FileNotFoundError(f"{exp_dir} is not found.")
    # dst_dirを作成
    for exp_name in args.exp_name_list:
        dst_dir = os.path.join(uploading_dir, exp_name)
        os.makedirs(dst_dir, exist_ok=True)
        for fold in args.folds:
            exp_fold_dir = os.path.join(exp_dir, str(fold))
            fold_dst_dir = os.path.join(dst_dir, str(fold))
            os.makedirs(fold_dst_dir, exist_ok=True)
            for target_file in target_files:
                src_path = os.path.join(exp_fold_dir, target_file)
                dst_path = os.path.join(fold_dst_dir, target_file)
                # src_pathからdst_pathにファイルをコピー
                os.system(f"cp {src_path} {dst_path}")

    # dst_pathの中身をzipにしてupload_dirに保存
    os.makedirs(args.upload_dir, exist_ok=True)
    zip_path = f"{args.upload_dir}/models.zip"
    os.system(f"zip -r {zip_path} {uploading_dir}")

    # dataset用のmetadataファイルを作成
    dataset_meta = {
        "title": f"{args.competition}-models",
        "id": f"{args.kaggle_username}/{args.competition}-models",
        "licenses": [{"name": "CC0-1.0"}],
    }
    # metadataファイルをupload_dirに保存
    with open(os.path.join(args.upload_dir, "dataset-metadata.json"), "w") as f:
        json.dump(dataset_meta, f)

    # kaggle APIを使ってファイルをアップロード
    if args.upload_or_create == "upload":
        subprocess.run(
            f"kaggle datasets version -p {args.upload_dir} -m 'upload' -d ", shell=True
        )
    elif args.upload_or_create == "create":
        subprocess.run(
            f"kaggle datasets create -p {args.upload_dir} --dir-mode zip", shell=True
        )
    else:
        raise ValueError("upload_or_create must be 'upload' or 'create'")
    # 一時ファイルを削除
    # os.system(f"rm -r {dst_dir}")
    os.system(f"rm -r {args.upload_dir}")
