upload_mode="upload"

if [ "$upload_mode" = "create" ]; then
    echo "Creating a new dataset"
    python /kaggle/kaggle_apis/upload_models.py --exp-name-list "exp011s_smooth2_001" "exp022s_maxvit_384" "exp022s_swin_384_2" \
                                                --upload-or-create "create"
elif [ "$upload_mode" = "upload" ]; then
    echo "Uploading the existing dataset"
    python /kaggle/kaggle_apis/upload_models.py --exp-name-list "exp011s_smooth2_001" "exp022s_maxvit_384" "exp022s_swin_384_2" \
                                                 --upload-or-create "upload"
else
    echo "Invalid upload mode"
fi
