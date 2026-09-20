## Setup

### Remove `.idea` from Git tracking

If `.idea` was previously committed but should now be ignored:

```bash
git rm -r --cached .idea
```

### Install `uv` and set up the environment

Run the bootstrap script from the project root:

```bash
python bootstrap.py
```

This will install `uv` if necessary and synchronize the project's Python environment using `uv.lock`.

### Add a dependency

To install a new library and add it to the project dependencies:

```bash
uv add <package-name>
```

For example:

```bash
uv add requests
```

### Run the application

Run a Python program using the project's managed environment:

```bash
uv run main.py
```

### Remove a dependency

To remove a library from the project:

```bash
uv remove <package-name>
```

For example:

```bash
uv remove requests
```



huggingface-cli download moonshotai/Kimi-K3 --local-dir /home/grf/Music/Kimi-K3

huggingface-cli download moonshotai/Kimi-K3 --dry-run