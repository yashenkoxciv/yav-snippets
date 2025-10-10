from yav_snippets import ClassRepositoryArtifact


def test_no_tag():
    class Example(ClassRepositoryArtifact):
        pass

    assert Example.TAG is None


def test_str_tag():
    test_tag = "tag"

    class Example(ClassRepositoryArtifact):
        TAG = test_tag

    assert Example.TAG == test_tag
