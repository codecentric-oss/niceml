"""Module for configuration schemes"""  # QUEST: refactor?
from typing import (
    Any,
    Callable,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    overload,
)

import attr
import cattr
from attr import NOTHING, Factory, asdict
from dagster.config.field_utils import Map as dagster_Map

import dagster


def format_attribute_doc(attribute: attr.Attribute) -> str:
    """Generates and returns attributes of attribute as string"""
    attr_type = (
        attribute.type.__name__
        if attribute.type is not None and hasattr(attribute.type, "__name__")
        else str(attribute.type)
    )
    doc = f"{attribute.name}: {attr_type}\n\t"
    if "description" in attribute.metadata:
        doc += f"{attribute.metadata['description']}. "
    if attribute.default != NOTHING:
        doc += f"Default: {attribute.default}"
    return doc


def format_attrs_doc(cls: Any) -> str:
    """Add attributes section to attrs class docstring."""
    doc = cls.__doc__ or ""
    try:
        attributes = list(attr.fields(cls))
    except (TypeError, attr.exceptions.NotAnAttrsClassError):
        return doc
    if attributes:
        doc += "\n\nAttributes\n----------\n\n"
        doc += "\n".join(map(format_attribute_doc, attributes))
    return doc


def define(  # pylint: disable=too-many-locals
    maybe_cls=None,
    *,
    these=None,
    repr=None,  # pylint: disable=redefined-builtin
    hash=None,  # pylint: disable=redefined-builtin
    init=None,
    slots=True,
    frozen=False,
    weakref_slot=True,
    str=False,  # pylint: disable=redefined-builtin
    auto_attribs=None,
    kw_only=False,
    cache_hash=False,
    auto_exc=True,
    eq=None,
    order=False,
    auto_detect=True,
    getstate_setstate=None,
    on_setattr=None,
    field_transformer=None,
    match_args=True,
):
    """Replacement of attr.define that updates class docstring with attributes."""

    def decode(cls):
        """Actual decorator function."""
        cls = attr.define(
            these=these,
            repr=repr,  # pylint: disable=redefined-builtin
            hash=hash,  # pylint: disable=redefined-builtin
            init=init,
            slots=slots,
            frozen=frozen,
            weakref_slot=weakref_slot,
            str=str,
            auto_attribs=auto_attribs,
            kw_only=kw_only,
            cache_hash=cache_hash,
            auto_exc=auto_exc,
            eq=eq,
            order=order,
            auto_detect=auto_detect,
            getstate_setstate=getstate_setstate,
            on_setattr=on_setattr,
            field_transformer=field_transformer,
            match_args=match_args,
        )(cls)

        cls.__doc__ = format_attrs_doc(cls)
        return cls

    return decode if maybe_cls is None else decode(maybe_cls)


FieldType = TypeVar("FieldType")  # pylint: disable=invalid-name


@overload
def field(  # pylint: disable=too-many-locals
    *,
    validator=None,
    repr=True,  # pylint: disable=redefined-builtin
    hash=None,  # pylint: disable=redefined-builtin
    init=True,
    metadata=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    description: Optional[str] = None,
) -> Any:
    ...


@overload
def field(  # pylint: disable=too-many-locals
    *,
    default: FieldType,
    validator=None,
    repr=True,  # pylint: disable=redefined-builtin
    hash=None,  # pylint: disable=redefined-builtin
    init=True,
    metadata=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    description: Optional[str] = None,
) -> FieldType:
    ...


def field(  # pylint: disable=too-many-locals
    *,
    default=NOTHING,
    validator=None,
    repr=True,  # pylint: disable=redefined-builtin
    hash=None,  # pylint: disable=redefined-builtin
    init=True,
    metadata=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    description: Optional[str] = None,
):
    """Replacement of attr.field that moves ``description`` into metadata."""
    if description:
        metadata = {**(metadata or {}), "description": description}
    return attr.field(  # type: ignore
        default=default,
        validator=validator,
        repr=repr,  # pylint: disable=redefined-builtin
        hash=hash,  # pylint: disable=redefined-builtin
        init=init,
        metadata=metadata,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
    )


_Config = TypeVar("_Config")


def parse_config(config: Any, cls: Type[_Config]) -> _Config:
    """Parse configuration."""
    parsed: _Config = cattr.structure(config, cls)
    return parsed


class ConfigSchemaConversionException(BaseException):
    """Base class for exceptions when building config schema."""


def _build_scalar_config_schema(  # pylint: disable=unused-argument
    config_class: Any, builders: Iterable[Callable[..., Any]]
) -> Optional[Union[float, int, bool, str]]:
    """Build dagster config schema from scalar configuration type."""
    if config_class in (float, int, bool, str):
        return config_class
    return None


def _build_iterable_config_schema(
    config_class: Any, builders: Iterable[Callable[..., Any]]
) -> Optional[dagster.Array]:
    """Build dagster config schema from iterable configuration type."""
    outer_class = get_origin(config_class)
    if outer_class in (list, tuple):
        inner_class = get_args(config_class)
        inner_schema = build_config_schema(inner_class, builders)
        return dagster.Array(inner_schema)
    return None


def _build_dict_config_schema(
    config_class: Any, builders: Iterable[Callable[..., Any]]
) -> Optional[dagster_Map]:
    """Build dagster config schema from mapping type."""
    outer_class = get_origin(config_class)
    if outer_class is dict:
        key_class, value_class = get_args(config_class)
        value_schema = build_config_schema(value_class, builders)
        return dagster_Map(key_type=key_class, inner_type=value_schema)
    return None


def _build_optional_config_schema(
    config_class: Any, builders: Iterable[Callable[..., Any]]
) -> Optional[dagster.Noneable]:
    """Build dagster config schema from optional type."""
    outer_class = get_origin(config_class)
    if outer_class is Union:
        inner_classes = get_args(config_class)
        if len(inner_classes) != 2:
            raise ConfigSchemaConversionException(
                f"Union type not supported: {config_class}"
            )
        inner_class, none_class = inner_classes
        if none_class is not type(None):
            raise ConfigSchemaConversionException(
                f"Second union type argument must be NoneType but is {none_class}"
            )
        inner_schema = build_config_schema(inner_class, builders)
        return dagster.Noneable(inner_schema)  # type: ignore
    return None


def _build_attribute_config_schema(
    attribute: attr.Attribute, builders: Iterable[Callable[..., Any]]
) -> dagster.Field:
    """Build dagster config schema from attrs ``Attribute``."""
    kwargs = {}
    if attribute.default is not None and attribute.default != NOTHING:
        if isinstance(attribute.default, Factory):  # type: ignore
            try:
                attr.fields(attribute.default.factory)
                default_value: Any = asdict(attribute.default.factory())
            except (TypeError, attr.exceptions.NotAnAttrsClassError):
                default_value = attribute.default.factory()  # type: ignore
        else:
            default_value = attribute.default
        kwargs["default_value"] = default_value
    if "description" in attribute.metadata:
        kwargs["description"] = attribute.metadata["description"]
    inner_schema = build_config_schema(attribute.type, builders)
    return dagster.Field(inner_schema, **kwargs)


def _build_attrs_class_config_schema(
    config_class: Any, builders: Iterable[Callable[..., Any]]
) -> Optional[dagster.Permissive]:
    """Build dagster config schema from attrs class."""
    try:
        attributes = attr.fields(config_class)
    except (TypeError, attr.exceptions.NotAnAttrsClassError):
        return None
    fields = {
        attribute.name: _build_attribute_config_schema(attribute, builders)
        for attribute in attributes
    }
    return dagster.Permissive(fields=fields)


_CONFIG_SCHEMA_BUILDERS = (
    _build_scalar_config_schema,
    _build_iterable_config_schema,
    _build_dict_config_schema,
    _build_optional_config_schema,
    _build_attrs_class_config_schema,
)


def build_config_schema(
    config_class: Any, builders: Iterable[Callable[..., Any]] = _CONFIG_SCHEMA_BUILDERS
):
    """Build dagster config schema from an configuration class.

    Here, a configuration class is

    - a scalar type (bool, float, int, str) or
    - a list or tuple of configuration classes or
    - a mapping from scalar type to a configuration class or
    - an attrs class whose attribute types are configuration classes.

    For anything else, return ``dagster.Any``.
    """
    builders_list = list(builders)
    for converter in builders_list:
        result = converter(config_class, builders_list)
        if result is not None:
            return result  # type: ignore
    return dagster.Any
