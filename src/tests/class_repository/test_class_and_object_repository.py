import pytest
from yav_snippets import ClassRepository, ClassRepositoryArtifact, ObjectRepository
from yav_snippets.class_repository.class_repository import TagDuplicationException


@pytest.fixture()
def class_repository():
    cr = ClassRepository()

    yield cr

    # clear ClassRepository.__tag_to_class mapping after each test
    mangled_name = "_ClassRepository__tag_to_class"
    setattr(ClassRepository, mangled_name, {})


def test_on_directory(class_repository):
    cr = ClassRepository.from_directory(
        "src/tests/class_repository/example_class_repository"
    )

    assert len(cr) == 3


def test_inplace(class_repository):
    class ClassA(ClassRepositoryArtifact):
        TAG = "a"

    class ClassB(ClassRepositoryArtifact):
        TAG = "b"

    assert len(class_repository) == 2


def test_conflict(class_repository):
    class Class1(ClassRepositoryArtifact):
        TAG = "1"

    class Class2(ClassRepositoryArtifact):
        TAG = "2"

    with pytest.raises(TagDuplicationException):

        class ClassD(ClassRepositoryArtifact):
            TAG = "2"

    assert len(class_repository) == 2


def test_get_class_by_tag(class_repository):
    class Foo(ClassRepositoryArtifact):
        TAG = "bar"

    foo_class = class_repository["bar"]

    assert foo_class is Foo


def test_yield_tags_and_classes(class_repository):
    class CatA(ClassRepositoryArtifact):
        TAG = "cat-a"
    
    class CatB(ClassRepositoryArtifact):
        TAG = "cat-b"
    
    class CatC(ClassRepositoryArtifact):
        TAG = "cat-c"

    tags, classes = list(zip(*class_repository))

    assert set(tags) == {"cat-a", "cat-b", "cat-c"}
    assert set(classes) == {CatA, CatB, CatC}


def test_get_object_repository(class_repository):
    class CatA(ClassRepositoryArtifact):
        TAG: str = "cat-a"

        def __str__(self) -> str:
            return f"{self.TAG}:instance"
    
    class CatB(CatA):
        TAG: str = "cat-b"
    
    objr = ObjectRepository(class_repository)

    tags, objs = list(zip(*objr))
    objs_strs = [str(obj) for obj in objs]

    assert set(tags) == {"cat-a", "cat-b"}
    assert set(objs_strs) == {"cat-a:instance", "cat-b:instance"}

