from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from place import Place

from .common import convert_value



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

    
    # Print all args separated by space
    print_parts = []
    for expr in exprs:
        print_parts.append(str(convert_value(expr)))
    print_text = ' '.join(print_parts)

    # add a newline if the command was println
    if add_newline:
        self.console.write(print_text + "\n")
    else:
        self.console.write(print_text)