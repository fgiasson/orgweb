import os
from weborg.container import container_exists, create_container, delete_container

def tangle(folder: str) -> None:
    """Every time we tangle, we create a new container and attach 
    a volume to it from the provided folder, tangle and delete
    it in case the next tangle uses a different folder"""

    try:
        volume = {f"{folder}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        print(f"Tangling {folder}...")

        # for each org file in the folder, tangle it
        for file in os.listdir(folder):
            if file.endswith(".org"):
                print("Tangling:", file)
                response = container.exec_run(f"emacs --batch --eval \"(progn (setq python-indent-guess-indent-offset t) (setq python-indent-guess-indent-offset-verbose nil) (find-file \\\"/mnt/org/{file}\\\") (org-babel-tangle))\"")
                print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Tangling canceled:", str(e))
    
def detangle(folder: str) -> None:
    """Syhnchronize the source files there have been tangled back to their
    original Org code blocks. Code blocks needs to have the header 
    `:comments link` or `:comments both` to be detangled. If you use
    `:noweb yes` references, then the noweb references won't be detangled,
    and the original Org file will be missing the noweb references. So,
    don't use detangle until detangling with noweb is fixed in Org-mode."""
    try:
        volume = {f"{folder}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        print(f"Detangling {folder}...")

        # for each source file in the folder, detangle it
        for file in os.listdir(folder):
            if not file.endswith(".org"):
                org_file = file.split(".")[0] + ".org"
                print(f"Detangling: {file} into {org_file}")
                response = container.exec_run(f"emacs --batch --eval \"(progn (require 'org) (setq make-backup-files nil) (setq python-indent-guess-indent-offset t) (setq python-indent-guess-indent-offset-verbose nil) (org-babel-detangle \\\"/mnt/org/{file}\\\") (switch-to-buffer \\\"{org_file}\\\") (save-buffer))\"")
                print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Detangling canceled:", str(e))