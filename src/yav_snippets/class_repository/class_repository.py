import os
import glob
from typing import Generator, Tuple, Hashable
from os.path import basename, isfile, join


class TagDuplicationException(Exception):
    pass


class ClassRepository:
    # class Tag to Class object mapping
    __tag_to_class = {}

    def __init__(self, class_artifacts: list | None = None):
        if class_artifacts:
            for ca in class_artifacts:
                self.__class__.add_class(ca)

    @classmethod
    def from_directory(cls, classes_dir: str):
        ClassRepository._load_classes(classes_dir)
        return ClassRepository()

    @classmethod
    def add_class(cls, Class: type):
        if Class.TAG in cls.__tag_to_class:
            present_class = cls.__tag_to_class[Class.TAG]
            present_class_name = f"{present_class.__module__}.{present_class.__name__}"
            raise TagDuplicationException(
                f"Class tag conflict: cannot add class {f'{Class.__module__}.{Class.__name__}'}. {present_class_name} already added with the same TAG ({Class.TAG})."
            )
        cls.__tag_to_class[Class.TAG] = Class

    @staticmethod
    def _load_classes(classes_dir: str):
        class_root = classes_dir.replace(os.sep, ".")
        if class_root[-1] != ".":
            class_root = class_root + "."

        cur_dir = join(classes_dir + os.sep, "*.py")
        classes_files = glob.glob(cur_dir)

        py_modules = []
        for f in classes_files:
            if isfile(f):
                f_basename = basename(f)[:-3]
                py_modules.append(f_basename)

        for py_module in py_modules:
            __import__(class_root + py_module, locals(), globals(), fromlist=["*"])

    def __getitem__(self, tag: str):
        return self.__tag_to_class[tag]

    def __len__(self):
        return len(self.__tag_to_class)
    
    def __iter__(self) -> Generator[Tuple[Hashable, type], None, None]:
        for tag, class_obj in self.__tag_to_class.items():
            yield tag, class_obj
