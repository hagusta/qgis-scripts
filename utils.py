from pathlib import Path
import os


def loadSample(filename:Path):
    dataDirectoryError= Exception("data directory does "  \
        + "not contains 'labels' directory")
    if not isinstance(filename,Path):
        if isinstance(filename,str):
            filename=Path(filename).absolute()
        else :
            raise TypeError
            
    if not filename.exists():
        raise FileNotFoundError
    if 'labels' not in os.listdir(filename.parent.parent):
        raise dataDirectoryError
    