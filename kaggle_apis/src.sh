upload_mode="upload"

if [ "$upload_mode" = "create" ]; then
    echo "Creating a new dataset"
    python /kaggle/kaggle_apis/upload_src.py --exp-name exp035_b3_512 --upload-or-create "create"
elif [ "$upload_mode" = "upload" ]; then
    echo "Uploading the existing dataset"
    python /kaggle/kaggle_apis/upload_src.py --exp-name exp035_b3_512 --upload-or-create "upload"
else
    echo "Invalid upload mode"
fi
