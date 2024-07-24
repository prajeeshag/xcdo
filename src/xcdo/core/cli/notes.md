
# Notes

- `Annotated[dict, jsonReader]` can be used to type hint an argument of the operator function which expects a `dict` but in the cli it expects a <str> `filename` and `jsonReader(filename)` will return `dict`
- To extend this idea one can annotate `input` in the same way and the `output` as `Annotated[someType, someTypeWriter]`
- Generalizing this idea for `input` and `output` we can define `DataTransformers`. `DataTransformers` convert data from one type to another. `File` is just one of the type. Thus a `DataReader` class is just a subclass of the `DataTransformer` class which transform the `file` object to the desired datatype object.
- In fact DataTransformers are just callables with single input
- assert `output` type at runtime 