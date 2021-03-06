# -*- coding: utf-8 -*-
import sys
import six


if six.PY2:
    stdout = sys.stdout
    reload(sys)
    sys.setdefaultencoding('utf-8')
    sys.stdout = stdout


def tree(obj, name='root', **kwargs):
    """
    print out an object as a tree

    :param obj: the object to be printed
    :param name: the name of the object, default='root'
    :param symbol_child_birth: the tree symbol where a sub-item is showing its first line, default=' ├─ '
    :param symbol_child_alive: the tree symbol where a sub-item is showing its rest lines, default=' │  '
    :param symbol_last_child_birth: the tree symbol where the last sub-item is showing its first line, default=' └─ '
    :param symbol_last_child_alive: the tree symbol where the last sub-item is showing its rest lines, default='    '
    :param expand_types: if not empty, only expand_types objects will be expanded, default={}
    :param no_expand_types: all iterable objects will be expanded except no_expand_types objects, only works when expand_types is empty, default={}
    :param expand: if False, print out the object in one line, default=True
    :param return_instead: if True, no printing, but return a string instead, default=False
    :param show_type: if True, object type info will be added at the end of expanding object name, default=False
    :return:
        unicode (in PY2) or str (in PY3) or None (return_instead=False)
    """
    _kwargs = {'symbol_child_birth': ' ├─ ',
               'symbol_child_alive': ' │  ',
               'symbol_last_child_birth': ' └─ ',
               'symbol_last_child_alive': '    ',
               'expand_types': {},
               'no_expand_types': {},
               'expand': True,
               'return_instead': False,
               'show_type': False,
               'padding_base': '',
               'padding_extra': '',
               'padding_increment': '',
               'padding_end': '\n'}
    _kwargs.update(kwargs)
    at_top_level_of_non_expand_line = False
    if _kwargs['expand']:
        _kwargs['expand'] = hasattr(obj, '__iter__') and not isinstance(obj, six.string_types)
        if _kwargs['expand_types']:
            _kwargs['expand'] = _kwargs['expand'] and isinstance(obj, tuple(_kwargs['expand_types']))
        elif _kwargs['no_expand_types']:
            _kwargs['expand'] = _kwargs['expand'] and not isinstance(obj, tuple(_kwargs['no_expand_types']))
        if not _kwargs['expand']:
            at_top_level_of_non_expand_line = True
    result = u''
    if _kwargs['expand']:
        obj_type = ' ' + repr(type(obj)) if _kwargs['show_type'] else ''
        head = u'{}{}{}{}\n'.format(_kwargs['padding_base'], _kwargs['padding_extra'], name, obj_type)
        if _kwargs['return_instead']:
            result += head
        else:
            six.print_(head, end='')
        _kwargs['padding_base'] = _kwargs['padding_base'] + _kwargs['padding_increment']
        for i, item in enumerate(obj):
            if isinstance(obj, dict):
                item, item_name = obj[item], item
            else:
                item_name = "{{{}}}".format(i) if isinstance(obj, set) \
                    else "[{}]".format(i) if isinstance(obj, list) \
                    else "({})".format(i) if isinstance(obj, tuple) \
                    else "<{}>".format(i)
            if i < len(obj) - 1:
                _kwargs['padding_extra'] = _kwargs['symbol_child_birth']
                _kwargs['padding_increment'] = _kwargs['symbol_child_alive']
            else:
                _kwargs['padding_extra'] = _kwargs['symbol_last_child_birth']
                _kwargs['padding_increment'] = _kwargs['symbol_last_child_alive']
            if _kwargs['return_instead']:
                result += tree(item, item_name, **_kwargs)
            else:
                tree(item, item_name, **_kwargs)
    else:
        head = u'{}{}{}{}'.format(_kwargs['padding_base'], _kwargs['padding_extra'], name, ': ' if name else '')
        if _kwargs['return_instead']:
            result += head
        else:
            six.print_(head, end='')
        if hasattr(obj, '__iter__') and not isinstance(obj, six.string_types):
            body_start = u'{' if isinstance(obj, (dict, set)) \
                else u'[' if isinstance(obj, list) \
                else u'(' if isinstance(obj, tuple) \
                else u'<'
            if _kwargs['return_instead']:
                result += body_start
            else:
                six.print_(body_start, end='')
            _kwargs['padding_base'] = ""
            _kwargs['padding_extra'] = ""
            _kwargs['padding_increment'] = ""
            _kwargs['padding_end'] = ""
            for i, item in enumerate(obj):
                if isinstance(obj, dict):
                    item, item_name = obj[item], item
                else:
                    item_name = ""
                if _kwargs['return_instead']:
                    result += tree(item, item_name, **_kwargs)
                else:
                    tree(item, item_name, **_kwargs)
                if i < len(obj) - 1:
                    sep = ', '
                else:
                    sep = ''
                if _kwargs['return_instead']:
                    result += sep
                else:
                    six.print_(sep, end='')
            body_end = u'}' if isinstance(obj, (dict, set)) \
                else u']' if isinstance(obj, list) \
                else u')' if isinstance(obj, tuple) \
                else u'>'
            body_end += "\n" if at_top_level_of_non_expand_line else ""
            if _kwargs['return_instead']:
                result += body_end
            else:
                six.print_(body_end, end='')
        else:
            body = (obj if isinstance(obj, six.string_types) else repr(obj)) + _kwargs['padding_end']
            if _kwargs['return_instead']:
                result += body
            else:
                six.print_(body, end='')
    if _kwargs['return_instead']:
        return result
