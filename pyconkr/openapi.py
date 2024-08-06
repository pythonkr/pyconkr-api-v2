import typing

EndpointType = tuple[str, str, str, typing.Callable]


def preprocessing_filter_spec(endpoints: typing.Iterable[EndpointType]) -> list[EndpointType]:
    return [endpoint for endpoint in endpoints if endpoint[0].startswith("/{version}/")]
