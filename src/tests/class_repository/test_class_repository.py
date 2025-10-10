import pytest
from yav_snippets import ClassRepository, ClassRepositoryArtifact
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
