import os
import re
from weborg.container import container_exists, create_container, delete_container

def tangle(project_folder: str, folder: str, files: list=None) -> None:
    """Every time we tangle, we create a new container and attach 
    a volume to it from the provided folder, tangle and delete
    it in case the next tangle uses a different folder.
    If `files` has a reference to one or more files, only
    tangle the files, in the `folder`, that are in the `files` 
    list."""
    print(f"project_folder: {project_folder}")
    print(f"folder: {folder}")
    print(f"files: {files}")
    try:
        volume = {f"{os.path.abspath(project_folder)}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        if not files:
            print(f"Tangling {folder}...")
        else:
            print(f"Tangling {files}...")

        # for each org file in the folder, tangle it
        for file in os.listdir(folder):
            if file.endswith(".org") and (not files or file in files):
                print("Tangling:", file)
                response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (find-file \\\"/mnt/org/{folder.strip('/')}/{file}\\\") (org-babel-tangle))\"")
                print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Tangling canceled:", str(e))


# To detangle a Org-file, we have to go to all tangled source files and 'org-detangle' each of them to recompose the original Org-file.
def detangle(project_folder: str, folder: str, files: list=None) -> None:
    """Syhnchronize the source files there have been tangled back to their
    original Org code blocks. Code blocks needs to have the header 
    `:comments link` or `:comments both` to be detangled. If you use
    `:noweb yes` references, then the noweb references won't be detangled,
    and the original Org file will be missing the noweb references. So,
    don't use detangle until detangling with noweb is fixed in Org-mode.
    If `files` has a reference to one or more files, only
    tangle the files, in the `folder`, that are in the `files` 
    list."""
    print(f"project_folder: {project_folder}")
    print(f"folder: {folder}")
    print(f"files: {files}")
    try:
        volume = {f"{os.path.abspath(project_folder)}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        if not files:
            print(f"Detangling {folder}...")
        else:
            print(f"Detangling {files}...")

        # for each source file in the folder, detangle it
        for file in os.listdir(folder):
            if not file.endswith(".org") and (not files or file in files):
                # org_file = file.split(".")[0] + ".org"
                # TODO "file:org/Docker.org::" get the ORG file from the tangled file

                # Extract each Org file reference from the tangled source file.
                # This handle the scenario where multiple Org files export code
                # in the same source file.
                #
                # If that source file change, we have to detangle it in all referenced Org file
                # TODO: remove that, this scenario doesn't work with org-mode at the moment
                with open(f"{folder}/{file}", "r") as tangled_file:
                    org_files = list(set(re.findall(r"file:(.*)::", tangled_file.read())))
                    print(org_files)

                for org_file in org_files:
                    # remove path from org_file
                    org_file = org_file.split("/")[-1]
                    print(f"Detangling: {file} into {org_file}")
                    response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (org-babel-detangle \\\"/mnt/org/{folder.strip('/')}/{file}\\\") (switch-to-buffer \\\"{org_file}\\\") (save-buffer))\"")
                    print(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (org-babel-detangle \\\"/mnt/org/{folder.strip('/')}/{file}\\\") (switch-to-buffer \\\"{org_file}\\\") (save-buffer))\"")
                    print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Detangling canceled:", str(e))

def execute(project_folder: str, folder: str, files: list=None) -> None:
    """Execute all the code blocks in the Org files in the folder. 
    When you use this operation, it will execute all the code blocks 
    of the file(s)."""
    try:
        volume = {f"{os.path.abspath(project_folder)}": {'bind': '/mnt/org', 'mode': 'rw'}}
        container = create_container(volume)

        if not files:
            print(f"Execute {folder}...")
        else:
            print(f"Execute {files}...")

        # for each org file in the folder, tangle it
        for file in os.listdir(folder):
            if file.endswith(".org") and (not files or file in files):
                print("Execute:", file)
                response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (find-file \\\"/mnt/org/{folder.strip('/')}/{file}\\\") (setq org-confirm-babel-evaluate nil) (org-babel-execute-buffer))\"")
                print(response.output.decode('utf-8'))

        delete_container()
    except Exception as e:
        print("Execute canceled:", str(e))    

# TODO: create a weave function to create the documentation pages, "the book"