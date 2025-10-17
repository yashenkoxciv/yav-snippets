# Object Repository

It allows you to collect the instances of a class repository.

## Usage

To create object repository:

```python
from yav_snippets import ClassRepository, ObjectRepository

cr = ClassRepository.from_directory("example_class_repository")
objr = ObjectRepository(cr)

for tag, obj in objr:
    print(tag, str(obj))
```

It uses alreadt constructed class repository. To specify object initialization implement `yav_snippets.object_repository.ObjectRepository._instance_initialize`. It also allows you to get object using a tag: `object_repo["tag"]`, iterate over pairs of tag and object, get length of the repository (collection).
