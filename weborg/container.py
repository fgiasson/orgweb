import docker
from docker.errors import ImageNotFound, NotFound

docker = docker.from_env()

def image_exists(img: str='localbuild:weborg') -> bool:
    """Check if the weborg image exists in the Docker environment"""
    try:
        docker.images.get(img)
        return True
    except ImageNotFound:
        return False

def container_exists(container: str='weborg') -> bool:
    """Check if the weborg container exists in the Docker environment"""
    try:
        docker.containers.get(container)
        return True
    except NotFound:
        return False 

def container_running(container: str='weborg') -> bool:
    """Check if the weborg container is running in the Docker environment"""
    try:
        if docker.containers.get(container).status == 'running':
            return True
        else:
            return False
    except NotFound:
        return False

def build_image(img: str='localbuild:weborg') -> None:
    """Build the weborg image from the Dockerfile"""
    image, logs = docker.images.build(path='.', tag=img, rm=True)
    return image, logs

def create_container(volume: dict, container: str='weborg', img: str='localbuild:weborg') -> None:
    """Create the weborg container from the weborg image"""
    return docker.containers.run(img, detach=True, tty=True, stdin_open=True, name=container, volumes=volume)

def delete_container(container: str='weborg') -> None:
    """Delete the weborg container from the Docker environment"""
    docker.containers.get(container).remove(force=True)

# def create_volume(path: str, volume: str='weborg') -> None:
#     """Create the `weborg` volume linked to the local `path`"""
#     volume = docker.volumes.create(name=volume, driver='local', driver_opts={'type': 'none', 'device': path, 'o': 'bind'})
#     return volume