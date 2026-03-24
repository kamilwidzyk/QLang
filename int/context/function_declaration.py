from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..function import Function

if TYPE_CHECKING:
    from place import Place

def handle_function_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # functionDecl: FUNCTION ID '(' paramList? ')' block;
    
    # 1. Terminal 'function'
    # 2. Terminal <function_name>
    # 3. Terminal '('
    # Optional: 4. paramList -> handle block
    # 5. Terminal ')'
    # 6. BlockContext -> handle block

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: 'children' key missing or no children")
        exit()

    children = block["children"]

    func_name = None
    param_list = None
    func_block = None
    no_params = False

    for child_index in range(len(children)):
        child = children[child_index]

        if child_index == 0: # 1. Terminal 'function'
            if not self.is_terminal(child, text="function", parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 0, expected 'function'")
                exit()
        elif child_index == 1: # 2. Terminal <function_name>
            func_name = self.extract_text(child, parent=block)
            if not self.is_valid_name(func_name):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 1, function name invalid")
                exit()
        elif child_index == 2: # 3. Terminal '('
            if not self.is_terminal(child, text="(", parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 2, expected '('")
                exit()
        elif child_index == 3: # 4. or 5.
            if self.is_type(child, TERMINAL, parent=block):
                if not self.is_terminal(child, text=')', parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 3, expected ')'")
                    exit()
                no_params = True # this function has no parameters
            else:
                param_list = self.handle_block(child, parent=block) 
        elif child_index == 4: # 5. or 6.
            if no_params:
                if not self.is_type(child, BLOCK_CONTEXT, parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 4, expected BlockContext")
                    exit()
                func_block = self.handle_block(child, parent=block)
            else:
                if not self.is_terminal(child, text=')', parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 4, expected ')'")
                    exit()
        elif child_index == 5: # 6. only if function has params
            if no_params:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index 5, unexpected block")
                exit()
            else:
                if not self.is_type(child, BLOCK_CONTEXT, parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "funcDeclContext: child index 5, excepted BlockContext")
                    exit()
                func_block = self.handle_block(child, parent=block)
        else:
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "functionDeclContext: child index > 5, unexpected block")
            exit()

    print("Function Declaration parse done")
    print("Function name: " + str(func_name))
    print("Function parameters: " + str(param_list))
    print("Function code: " + str(func_block))

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    if self.scopes.exists(func_name):
        self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Name Error", "FuncDeclContext: variable or function with this name already exists")
        exit()

    func = Function(func_name, param_list, func_block, self.scopes.current, pos)
    self.scopes.create(func_name, func)