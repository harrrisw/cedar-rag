# Local setup record

Python 3.13.4 and Git 2.46.0.windows.1 were present. The directory was initially empty and was initialized as a Git repository.

Initial `python -m venv .venv` created the environment but failed during pip bootstrapping. The exact relevant error on retry was `PermissionError: [Errno 13] Permission denied` while writing pip's temporary wheel file. A second attempt using a workspace temporary directory encountered the same restriction. The smallest successful correction was to rerun the environment's `ensurepip` command with approved execution permissions, then install `sentence-transformers` and `numpy` into that same local environment. No system Python installation was changed.

The first restricted-network package installation reported `ERROR: Could not find a version that satisfies the requirement sentence-transformers (from versions: none)`. The approved network-enabled installation could download the packages. Real model execution and package versions are recorded separately in the generated evidence; failed setup attempts are not treated as embedding results.

`gh auth status` found the existing GitHub credential invalid. Remote publication requires reauthentication and a specified destination.

The MiniLM download completed from Hugging Face at snapshot `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Ten configuration, tokenizer, pooling, and safetensors files were cached inside the ignored `.cache/huggingface` directory. The assignment run was launched with `HF_HUB_OFFLINE=1` to use those downloaded files without network requests.
