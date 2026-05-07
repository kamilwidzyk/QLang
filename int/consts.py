"""
This file contains consts that are access from multiple files
Do not import anything from this module to not make a cyclic import
"""

from antlr4.tree.Tree import TerminalNode
from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser


TerminalCtx = TerminalNode
StatementCtx = QLangParser.StatementContext

#################### VARIABLES ####################
VarDeclCtx = QLangParser.VarDeclContext
SizeGetterExprCtx = QLangParser.SizeGetterExprContext
SizeGetterCtx = QLangParser.SizeGetterContext

#################### LIST ####################
ListExprCtx = QLangParser.ListExprContext
ListCtx = QLangParser.ListContext
EmptyListCtx = QLangParser.EmptyListContext
NonEmptyListCtx = QLangParser.NonEmptyListContext

#################### NUMBERS ####################
NumExprCtx = QLangParser.NumExprContext
IntNumExprCtx = QLangParser.IntNumExprContext
NumCastExprCtx = QLangParser.NumCastExprContext



IoStmtCtx = QLangParser.IoStmtContext
VarExprCtx = QLangParser.VarExprContext
PlaceMemberCtx = QLangParser.PlaceMemberContext
FunctionDeclCtx = QLangParser.FunctionDeclContext
ParamListCtx = QLangParser.ParamListContext
ParamCtx = QLangParser.ParamContext
BlockCtx = QLangParser.BlockContext
StrExprCtx = QLangParser.StrExprContext
FunctionCallStmtCtx = QLangParser.FunctionCallStmtContext
FunctionCallExprCtx = QLangParser.FuncCallExprContext
ArgListCtx = QLangParser.ArgListContext
ForStmtCtx = QLangParser.ForStmtContext
WhileStmtCtx = QLangParser.WhileStmtContext
PowExprCtx = QLangParser.PowExprContext
FormatCtx = QLangParser.FormatContext
IfStmtCtx = QLangParser.IfStmtContext
RelExprContext = QLangParser.RelExprContext
AddSubExprContext = QLangParser.AddSubExprContext
MulDivModExprCtx = QLangParser.MulDivModExprContext
EqExprCtx = QLangParser.EqExprContext
AndExprCtx = QLangParser.AndExprContext
OrExprCtx = QLangParser.OrExprContext
BoolExprCtx = QLangParser.BoolExprContext
ParenExprCtx = QLangParser.ParenExprContext
ConstraintCtx = QLangParser.ConstraintContext
AssigmentStmtCtx = QLangParser.AssignStmtContext


#################### Operators ####################

# Not 
NotExprContext = QLangParser.NotExprContext

# Minus
MinusExprCtx = QLangParser.MinusExprContext

# Plus
PlusExprCtx = QLangParser.PlusExprContext

# Pre-post increment and decrement
PreIncrementCtx = QLangParser.PreIncrementExprContext
PostIncrementCtx = QLangParser.PostIncrementExprContext
PreDecrementCtx = QLangParser.PreDecrementExprContext
PostDecrementCtx = QLangParser.PostDecrementExprContext

# Assignment expr
AssignExprCtx = QLangParser.AssignmentExprContext

# Plus equal
PlusEqExprCtx = QLangParser.PlusEqExprContext

# Minus equal
MinusEqExprCtx = QLangParser.MinusEqExprContext

# Mul equal
MulEqExprCtx = QLangParser.MulEqExprContext

# Div equal
DivEqExprCtx = QLangParser.DivEqExprContext

# Mod equal
ModEqExprCtx = QLangParser.ModEqExprContext

# Pow equal
PowEqExprCtx = QLangParser.PowEqExprContext

# And equal
AndEqExprCtx = QLangParser.AndEqExprContext

# Or equal
OrEqExprCtx = QLangParser.OrEqExprContext


