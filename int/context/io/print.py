from typing import Any, TYPE_CHECKING

from int.num import Num
from int.obs import Obs
from int.text import Text
from int.expression import Expression, TYPE_LIST, TYPE_INT, TYPE_FLOAT, TYPE_NUM, TYPE_OBS, TYPE_BOOL, TYPE_TEXT, TYPE_STRING, ValueResolver

if TYPE_CHECKING:
    from place import Place

from .common import convert_value, format_print_value

def force_to_string(value, inside_list=False):
    if isinstance(value, Expression):
        raw = value.extract_raw_value()
        if not isinstance(raw, list) and hasattr(raw, 'get_value'):
            raw = raw.get_value()
        if value.type == TYPE_BOOL or value.type == TYPE_OBS:
            if hasattr(raw, 'get_value'):
                raw = raw.get_value()
            return 'T' if raw else 'F'
        if value.type in (TYPE_INT, TYPE_FLOAT, TYPE_NUM):
            return str(raw)
        if value.type in (TYPE_TEXT, TYPE_STRING):
            if inside_list:
                return '"' + str(raw) + '"'
            return str(raw)
        if value.type == TYPE_LIST and isinstance(raw, list):
            return '[' + ', '.join(force_to_string(item, inside_list=True) for item in raw) + ']'
        
        return force_to_string(value.extract_raw_value(), inside_list=inside_list)
    
    if isinstance(value, list):
        return '[' + ', '.join(force_to_string(item, inside_list=True) for item in value) + ']'
    if isinstance(value, Obs):
        return 'T' if value.get_value() else 'F'
    if isinstance(value, bool):
        return 'T' if value else 'F'
    if isinstance(value, str):
        if inside_list:
            return '"' + value + '"'
        return value
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, Num):
        return str(value.get_value())
    if isinstance(value, Text):
        if inside_list:
            return '"' + value.get_value() + '"'
        return value.get_value()
    return str(value)


def handle_print(self: Place, block: Any, add_newline=False):
    # no expr -> print a newline if enabled
    if not block.expr():
        if add_newline:
            self.console.write("\n")
        return
    
    # Get all expressions
    exprs = []
    for i in range(len(block.expr())):
        exprs.append(self.handle_block(block.expr(i), block))

    print("print expr type: ", type(exprs[0]))

    
    # Print all args separated by space
    print_parts = []
    for expr in exprs:
        converted = force_to_string(expr)
        converted = ValueResolver.extract_raw_value(converted)
        while(hasattr(converted, 'get')):
            converted = converted.get()
        print_parts.append(converted)
    print_text = ' '.join(print_parts)

    # add a newline if the command was println
    if add_newline:
        self.console.write(print_text + "\n")
    else:
        self.console.write(print_text)