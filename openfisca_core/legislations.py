# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Handle legislative parameters in JSON format."""


import collections

from . import conv


units = [
    u'currency',
    u'day',
    u'hour',
    u'month',
    u'year',
    ]


def validate_node_json(node, state = None):
    if node is None:
        return None, None
    state = conv.add_ancestor_to_state(state, node)
    validated_node, errors = conv.pipe(
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                code = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_line,
                    conv.not_none,
                    ),
                comment = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_text,
                    ),
                description = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_line,
                    ),
                nodes = conv.pipe(
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        validate_node_json,
                        drop_none_items = True,
                        ),
                    conv.empty_to_none,
                    ),
                parameters = conv.pipe(
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        validate_parameter_json,
                        drop_none_items = True,
                        ),
                    conv.empty_to_none,
                    ),
                scales = conv.pipe(
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        validate_scale_json,
                        drop_none_items = True,
                        ),
                    conv.empty_to_none,
                    ),
                ),
            constructor = collections.OrderedDict,
            drop_none_values = 'missing',
            keep_value_order = True,
            ),
        )(node, state = state)
    if errors is None:
        required_group_keys = ('nodes', 'parameters', 'scales')
        if all(
                validated_node.get(key) is None
                for key in required_group_keys
                ):
            error = state._(u"At least one of the following items must be present: {}").format(state._(u', ').join(
                u'"{}"'.format(key)
                for key in required_group_keys
                ))
            errors = dict(
                (key, error)
                for key in required_group_keys
                )
    conv.remove_ancestor_from_state(state, node)
    return validated_node, errors


def validate_parameter_json(parameter, state = None):
    if parameter is None:
        return None, None
    state = conv.add_ancestor_to_state(state, parameter)
    validated_parameter, errors = conv.pipe(
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                code = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_line,
                    conv.not_none,
                    ),
                comment = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_text,
                    ),
                description = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_line,
                    ),
                format = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.input_to_slug,
                    conv.test_in([
                        'boolean',
                        'float',
                        'integer',
                        'rate',
                        ]),
                    ),
                unit = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.input_to_slug,
                    conv.test_in(units),
                    ),
                values = conv.pipe(
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        validate_value_json,
                        drop_none_items = True,
                        ),
                    conv.empty_to_none,
                    conv.not_none,
                    ),
                ),
            constructor = collections.OrderedDict,
            drop_none_values = 'missing',
            keep_value_order = True,
            ),
        )(parameter, state = state)
    conv.remove_ancestor_from_state(state, parameter)
    return validated_parameter, errors


def validate_scale_json(scale, state = None):
    if scale is None:
        return None, None
    state = conv.add_ancestor_to_state(state, scale)
    validated_scale, errors = conv.pipe(
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                code = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_line,
                    conv.not_none,
                    ),
                comment = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_text,
                    ),
                description = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_line,
                    ),
                option = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.input_to_slug,
                    conv.test_in((
                        'contrib',
                        'noncontrib',
                        )),
                    ),
                slices = conv.pipe(
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        validate_slice_json,
                        drop_none_items = True,
                        ),
                    conv.empty_to_none,
                    conv.not_none,
                    ),
                unit = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.input_to_slug,
                    conv.test_in((
                        'currency',
                        )),
                    ),
                ),
            constructor = collections.OrderedDict,
            drop_none_values = 'missing',
            keep_value_order = True,
            ),
        )(scale, state = state)
    conv.remove_ancestor_from_state(state, scale)
    return validated_scale, errors


def validate_slice_json(slice, state = None):
    if slice is None:
        return None, None
    state = conv.add_ancestor_to_state(state, slice)
    validated_slice, errors = conv.pipe(
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                base = validate_values_holder_json,
                comment = conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_text,
                    ),
                rate = conv.pipe(
                    validate_values_holder_json,
                    conv.not_none,
                    ),
                threshold = conv.pipe(
                    validate_values_holder_json,
                    conv.not_none,
                    ),
                ),
            constructor = collections.OrderedDict,
            drop_none_values = 'missing',
            keep_value_order = True,
            ),
        )(slice, state = state)
    conv.remove_ancestor_from_state(state, slice)
    return validated_slice, errors


def validate_value_json(value, state = None):
    if value is None:
        return None, None
    container = state.ancestors[-1]
    value_converter = dict(
        boolean = conv.condition(
            conv.test_isinstance(int),
            conv.test_in((0, 1)),
            conv.test_isinstance(bool),
            ),
        float = conv.condition(
            conv.test_isinstance(int),
            conv.anything_to_float,
            conv.test_isinstance(float),
            ),
        integer = conv.condition(
            conv.test_isinstance(float),
            conv.pipe(
                conv.test(lambda number: round(number) == number),
                conv.function(int),
                ),
            conv.test_isinstance(int),
            ),
        rate = conv.condition(
            conv.test_isinstance(int),
            conv.anything_to_float,
            conv.test_isinstance(float),
            ),
        )[container.get('format') or 'float']  # Only parameters have a "format".
    state = conv.add_ancestor_to_state(state, value)
    validated_value, errors = conv.pipe(
        conv.test_isinstance(dict),
        conv.struct(
            {
                u'comment': conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.cleanup_text,
                    ),
                u'from': conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.iso8601_input_to_date,
                    conv.date_to_iso8601_str,
                    conv.not_none,
                    ),
                u'to': conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.iso8601_input_to_date,
                    conv.date_to_iso8601_str,
                    conv.not_none,
                    ),
                u'value': conv.pipe(
                    value_converter,
                    conv.not_none,
                    ),
                },
            constructor = collections.OrderedDict,
            drop_none_values = 'missing',
            keep_value_order = True,
            ),
        )(value, state = state)
    conv.remove_ancestor_from_state(state, value)
    return validated_value, errors


validate_values_holder_json = conv.pipe(
    conv.test_isinstance(list),
    conv.uniform_sequence(
        validate_value_json,
        drop_none_items = True,
        ),
    conv.empty_to_none,
    )
