import os
from weborg.container import container_exists, create_container, delete_container

def tangle(folder: str, files: list=None) -> None:
    """Every time we tangle, we create a new container and attach 
    a volume to it from the provided folder, tangle and delete
    it in case the next tangle uses a different folder.
    If `files` has a reference to one or more files, only
    tangle the files, in the `folder`, that are in the `files` 
    list."""

    try:
        volume = {f"{folder}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        if not files:
            print(f"Tangling {folder}...")
        else:
            print(f"Tangling {files}...")

        # for each org file in the folder, tangle it
        for file in os.listdir(folder):
            if file.endswith(".org") and (not files or file in files):
                print("Tangling:", file)
                response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (find-file \\\"/mnt/org/{file}\\\") (org-babel-tangle))\"")
                print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Tangling canceled:", str(e))
    
def detangle(folder: str, files: list=None) -> None:
    """Syhnchronize the source files there have been tangled back to their
    original Org code blocks. Code blocks needs to have the header 
    `:comments link` or `:comments both` to be detangled. If you use
    `:noweb yes` references, then the noweb references won't be detangled,
    and the original Org file will be missing the noweb references. So,
    don't use detangle until detangling with noweb is fixed in Org-mode.
    If `files` has a reference to one or more files, only
    tangle the files, in the `folder`, that are in the `files` 
    list."""
    try:
        volume = {f"{folder}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        if not files:
            print(f"Detangling {folder}...")
        else:
            print(f"Detangling {files}...")

        # for each source file in the folder, detangle it
        for file in os.listdir(folder):
            if not file.endswith(".org") and (not files or file in files):
                org_file = file.split(".")[0] + ".org"
                print(f"Detangling: {file} into {org_file}")
                response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (org-babel-detangle \\\"/mnt/org/{file}\\\") (switch-to-buffer \\\"{org_file}\\\") (save-buffer))\"")
                print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Detangling canceled:", str(e))