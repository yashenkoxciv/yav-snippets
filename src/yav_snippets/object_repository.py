from typing import Generator, Tuple, Hashable
from yav_snippets import ClassRepository


class ObjectRepository:
    def __init__(self, class_repo: ClassRepository) -> None:
        self.__tag_to_obj = {}
        for tag, cls in class_repo:
            self.__tag_to_obj[tag] = self._instance_initialize(cls)
    
    def _instance_initialize(self, cls: type) -> object:
        return cls()
    
    def __getitem__(self, tag: str):
        return self.__tag_to_obj[tag]

    def __len__(self):
        return len(self.__tag_to_obj)
    
    def __iter__(self) -> Generator[Tuple[Hashable, object], None, None]:
        for tag, obj in self.__tag_to_obj.items():
            yield tag, obj
