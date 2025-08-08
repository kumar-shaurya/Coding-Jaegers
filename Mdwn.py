from huggingface_hub import snapshot_download

# MusicGen-small
snapshot_download(
    repo_id="facebook/musicgen-small",
    local_dir="./models/musicgen-small",
    local_dir_use_symlinks=False
)

# T5-base
snapshot_download(
    repo_id="t5-base",
    local_dir="./models/t5-base",
    local_dir_use_symlinks=False
)
