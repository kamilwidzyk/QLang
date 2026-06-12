from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

from ..expression import Expression, TYPE_STRING

if TYPE_CHECKING:
    from place import Place

def handle_string(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles raw string, replaces escapes characters
    """
    # STRING     : '"' (~["\r\n])* '"' 
    #            | '\'' (~['])* '\''
    #            | '`' (~[`])* '`'
    #           ;
    text = [x for x in block.getChildren()][0].getText()
    quote = text[0]
    content = text[1:-1]
    
    # Handle escape sequences
    content = content.replace('\\n', '\n')
    content = content.replace('\\t', '\t')
    content = content.replace('\\r', '\r')
    content = content.replace('\\\\', '\\')
    content = content.replace('\\\'', '\'')
    content = content.replace('\\"', '"')
    content = content.replace('\\`', '`')
    
    return Expression(TYPE_STRING, content)