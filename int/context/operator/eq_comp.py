from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression, TYPE_BOOL
from ...operations.compare import do_compare_equal, do_compare_not_equal

if TYPE_CHECKING:
    from place import Place



def handle_eq_comp(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('==' | '!=') expr
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    right = self.handle_block(children[2], block)

    if children[1].getText() == "==":
        return do_compare_equal(left, right)
    else:
        return do_compare_not_equal(left, right)