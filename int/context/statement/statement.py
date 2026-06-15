from __future__ import annotations
from typing import Any, TYPE_CHECKING



from ...script_errors import ScriptErrors
from ...consts import *
from ..function.function_call import FunctionReturn
from ...QLang.QLangParser import QLangParser

if TYPE_CHECKING:
    from place import Place


class BreakLoop(Exception):
    pass


class ContinueLoop(Exception):
    pass


def handle_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles any statement
    Raises returns, breaks and continues

    """
    print("Statement: ", block.getText())

    if isinstance(block, varDeclarationCtx):
        print("VarDecl")
        self.handle_block(block.varDecl(), parent=parent)
        return None
    if isinstance(block, ConstDeclarationCtx):
        print("ConstDecl")
        self.handle_block(block.constDecl(), parent=parent)
        return None
    if isinstance(block, receiveDeclCtx):
        print("ReceiveDecl")
        self.handle_block(block.receiveDecl(), parent=parent)
        return None
    if isinstance(block, sendStatementCtx):
        print("SendStmt")
        self.handle_block(block.sendStmt(), parent=parent)
        return None
    if isinstance(block, gateStatementCtx):
        print("GateStmt")
        self.handle_block(block.gateStmt(), parent=parent)
        return None
    if isinstance(block, assignmentStatementCtx):
        print("AssignStmt")
        self.handle_block(block.assignStmt(), parent=parent)
        return None
    
    if isinstance(block, functionCallStatementCtx):
        print("FuncCallStmt")
        self.handle_block(block.functionCallStmt(), parent=parent)
        return None
    
    if isinstance(block, ifStatementCtx):
        print("IfStmt")
        self.handle_block(block.ifStmt(), parent=parent)
        return None

    if isinstance(block, forStatementCtx):
        print("ForStmt")
        self.handle_block(block.forStmt(), parent=parent)
        return None
    
    if isinstance(block, whileStatementCtx):
        print("WhileStmt")
        self.handle_block(block.whileStmt(), parent=parent)
        return None

    if isinstance(block, iterateStatementCtx):
        print("IterateStmt")
        self.handle_block(block.iterateStmt(), parent=parent)
        return None
    
    if isinstance(block, waitStatementCtx):
        print("WaitStmt")
        self.handle_block(block.waitStmt(), parent=parent)
        return None
    
    if isinstance(block, ioStatementCtx):
        print("IoStmt")
        self.handle_block(block.ioStmt(), parent=parent)
        return None
    
    if isinstance(block, breakStatementCtx):
        from .continue_break import handle_break
        handle_break(self, block, parent, pos)
    
    if isinstance(block, continueStatementCtx):
        from .continue_break import handle_continue
        handle_continue(self, block, parent, pos)
    
    if isinstance(block, returnStatementCtx):
        print("ReturnStmt")
        return_val = None
        if block.expr() is not None:
            return_val = self.handle_block(block.expr(), parent=parent)
        raise FunctionReturn(return_val)
    
    if isinstance(block, blockStatementCtx):
        print("BlockStmt")
        self.handle_block(block.block(), parent=parent)
        return None
    
    if isinstance(block, functionDeclStatementCtx):
        print("FunctionDeclStmt")
        self.handle_block(block.functionDecl(), parent=parent)
        return None
    
    if isinstance(block, exprStatementCtx):
        print("ExprStmt")
        self.handle_block(block.expr(), parent=parent)
        return None
    
    if isinstance(block, semicolorStatementCtx):
        print("SemicolonStmt")
        return None
    
    
    """
    def is_return(block) -> bool:
        if not isinstance(block, TerminalCtx):
            return False
        if block.getText() != "return":
            return False
        return True
    


    first = block.getChild(0)


    print(block.getText())

    # return
    if is_return(first):
        return_val = None
        if block.getChildCount() > 2:
            return_val = self.handle_block(block.getChild(1))
        raise FunctionReturn(return_val)

    # break
    if isinstance(first, TerminalCtx) and first.getText() == "break":
        print("BREAK LOOP")
        raise BreakLoop()

    # continue
    if isinstance(first, TerminalCtx) and first.getText() == "continue":
        print("CONTINUE LOOP")
        raise ContinueLoop()

    if isinstance(first, TerminalCtx) and first.getText() == "{":
        for item in self.handle_block(first, parent=block):
            self.handle_block(item, parent=block)
        return None

    self.handle_block(first, parent=block)

    return None

    """