"""Tests for the _docs_helpers module."""

import pytest

pytest.importorskip("pandas")

from unittest.mock import Mock, patch

import voluptuous as vol
from homeassistant.helpers import config_validation as cv, selector

from custom_components.adaptive_lighting._docs_helpers import (
    _format_voluptuous_instance,
    _type_to_str,
    generate_apply_markdown_table,
    generate_config_markdown_table,
    generate_set_manual_control_markdown_table,
)


def test_type_to_str_bool():
    assert _type_to_str(bool) == "`bool`"


def test_type_to_str_int():
    assert _type_to_str(int) == "`int`"


def test_type_to_str_float():
    assert _type_to_str(float) == "`float`"


def test_type_to_str_str():
    assert _type_to_str(str) == "`str`"


def test_type_to_str_entity_ids():
    assert _type_to_str(cv.entity_ids) == "list of `entity_id`s"


def test_type_to_str_boolean():
    assert _type_to_str(cv.boolean) == "bool"


def test_type_to_str_vol_in():
    type_ = vol.In([1, 2, 3])
    assert _type_to_str(type_) == "one of `[1, 2, 3]`"


def test_type_to_str_vol_any():
    type_ = vol.Any(int, str)
    result = _type_to_str(type_)
    assert "`int`" in result
    assert "`str`" in result
    assert " or " in result


def test_type_to_str_color_rgb_selector():
    type_ = selector.ColorRGBSelector()
    assert _type_to_str(type_) == "RGB color"


def test_type_to_str_select_selector():
    type_ = selector.SelectSelector(selector.SelectSelectorConfig(options=["a", "b"]))
    assert _type_to_str(type_) == "one of `['a', 'b']`"


def test_type_to_str_unknown():
    try:
        _type_to_str(object())
    except ValueError:
        pass


def test_format_voluptuous_instance_min_max():
    instance = vol.All(vol.Coerce(int), vol.Clamp(min=0, max=100))
    result = _format_voluptuous_instance(instance)
    assert result == "`int` 0-100"


def test_format_voluptuous_instance_min_only():
    instance = vol.All(vol.Coerce(int), vol.Clamp(min=0))
    result = _format_voluptuous_instance(instance)
    assert result == "`int > 0`"


def test_format_voluptuous_instance_max_only():
    instance = vol.All(vol.Coerce(int), vol.Clamp(max=100))
    result = _format_voluptuous_instance(instance)
    assert result == "`int < 100`"


def test_format_voluptuous_instance_no_range():
    instance = vol.All(vol.Coerce(int))
    result = _format_voluptuous_instance(instance)
    assert result == "`int`"


def test_generate_config_markdown_table():
    result = generate_config_markdown_table()
    assert result.startswith("|")
    assert "Variable name" in result
    assert "Description" in result
    assert "Default" in result
    assert "Type" in result


def test_generate_apply_markdown_table():
    result = generate_apply_markdown_table()
    assert result.startswith("|")
    assert "Variable name" in result
    assert "Description" in result


def test_generate_set_manual_control_markdown_table():
    result = generate_set_manual_control_markdown_table()
    assert result.startswith("|")
    assert "Variable name" in result
    assert "Description" in result
