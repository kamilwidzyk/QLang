from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_for_loop(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # forStmt: FOR ID FROM expr TO expr (STEP expr)? block;

    # for <name> from <start> to <end> block
    # for <name> from <start> to <end> step <step> block

    # 1. Terminal 'for'
    # 2. Terminal <name>
    # 3. Terminal 'from'
    # 4. Terminal <start>
    # 5. Terminal 'to'
    # 6. Terminal <end>
    # If step define:
    #   7a. Terminal 'step'
    #   7b. Terminal <step>
    # 8. BlockContext -> for body

    #            (CHILD INDEX)
    # (0) (1) (2) (3) (4) (5) (6)  (7)  (8)
    # [1] [2] [3] [4] [5] [6] [8]   
    # [1] [2] [3] [4] [5] [6] [7a] [7b] [8]
    # 
    
    if not self.has_children(block):
        print("ForStmtContext: missing 'child' key or no children")
        exit()

    children = block["children"]

    var_name = None
    start_val = None
    end_val = None
    step_defined = False
    step_val = None
    for_block = None


    for child_index in range(len(children)):
        child = children[child_index]

        if child_index == 0:
            if not self.is_terminal(child, text='for', parent=block):
                print("ForStmtContext: child index 0, expected 'for'")
                exit()
        elif child_index == 1:
            var_name = self.handle_block(child, parent=block)
        elif child_index == 2:
            if not self.is_terminal(child, text='from', parent=block):
                print("ForStmtContext: child index 2, expected 'from'")
                exit()
        elif child_index == 3:
            start_val = self.handle_block(child, parent=block)
        elif child_index == 4:
            if not self.is_terminal(child, text='to', parent=block):
                print("ForStmtContext: child index 4, expected 'to'")
                exit()
        elif child_index == 5:
            end_val = self.handle_block(child, parent=block)
        elif child_index == 6:
            if self.is_terminal(child, text='step', parent=block):
                step_defined = True
            else:
                for_block = self.handle_block(child, parent=block)
        elif child_index == 7:
            if not step_defined:
                print("ForStmtContext: child index 7, unexpecxted block")
                exit()

            step_val = self.handle_block(child, parent=block)
        elif child_index == 8:
            if not step_defined:
                print("ForStmtContext: child index 8, unexpected block")
                exit()

            for_block = self.handle_block(child, parent=block)
        else:
            print("ForStmtContext: child index > 8, unexpected block")
            exit()

    
    print("For loop")
    print("Variable name: " + var_name)
    print("Start: " + str(start_val))
    print("End: " + str(end_val))
    print("Step: " + str(step_val))
    print("Block: " + str(for_block))

    if start_val < 0:
        print("For loop: start_val < 0")
        exit()

    if end_val < 0:
        print("For loop: end_val < 0")
        exit()
    
    if step_val is None:
        step_val = 1

    if step_val < 0:
        print("For loop: step_val < 0")
        exit()

    if end_val < start_val:
        print("For loop: skip") # This is not an error
        return # do not run loop
    
    current_val = ObsRegister(32)
    current_val.set(start_val)

    # Enter new scope
    self.scopes.push(pos, scope_type="for")
    self.scopes.create(var_name, current_val)

    try:
        # Repeat block until current_val <= end_val
        while current_val.get() <= end_val:
            for child in for_block:
                self.handle_block(child, parent=block)

            current_val.set(current_val.get() + step_val)
            self.scopes.set(var_name, current_val)
    finally:
        # Exit scope
        self.scopes.pop()

    print("For loop: done")