# Class Repository

It allows you to collect several classes to avoid multiple imports.

There can be situations when you have dozens of classes that share common use case. For example, there is a collection of ML/DL models that are served on a separate service. So each model requires to do specific operations (preprocessing/postprocessing). All the operations abstracted out with general method `inference`, therefore all you need is to call the method on each model object.

To use all the classes (models) you have to:

1. Import dozens of classes probably from different modules or
2. Collect the classes as a `dict` using some intermediate module or
3. Use Class Repository which does all of the above.

## Usage

### Class Repository Artifact

The class you want to be collected by the class Class Repository must be inherited from `yav_snippets.ClassRepositoryArtifact` class and set class attribute `TAG` which must be of `Hashable` type.

Example:
```python
from yav_snippets import ClassRepositoryArtifact


class ModelA(ClassRepositoryArtifact):
    TAG = 'model_a'


class ModelB(ClassRepositoryArtifact):
    TAG = 'model_b'
```

So there are two steps:

1. Inherit your class from `yav_snippets.ClassRepositoryArtifact`
2. Initialize `TAG` class attribute to the `Hashable` object, so your class will be identified using the `TAG`

No need to import this classes in your main code base. Instead you can use `yav_snippets.ClassRepository`.

> `TAG` class attribute must have unique values along all the classes otherwise `yav_snippets.class_repository.class_repository.TagDuplicationException` exception will be raised.

### Class Repository

To get the collection of all classes you need you should instantiate `yav_snippets.ClassRepository`.

Suppose all your classes implemented as bunch of modules in directory `example_class_repository`. So the instantiation should be like that:

```python
from yav_snippets import ClassRepository

cr = ClassRepository.from_directory("example_class_repository")

# get class using the TAG
model_a_class = cr['model_a']

# get the total amount of classes collected
len(cr) 
```

Class Repository class [tests](../src/tests/class_repository/test_class_repository.py) can be an example.
