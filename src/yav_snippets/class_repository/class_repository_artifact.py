from typing import Hashable
from yav_snippets.class_repository.class_repository import ClassRepository


class ClassRepositoryArtifact:
    TAG: Hashable = None

    def __init_subclass__(cls):
        # exclude base classes when cls.TAG is None
        if cls.TAG is not None:
            ClassRepository.add_class(cls)
