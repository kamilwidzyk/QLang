"""
This file contains consts that are access from multiple files
Do not import anything from this module to not make a cyclic import
"""

from antlr4.tree.Tree import TerminalNode
from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser


TerminalCtx = TerminalNode
StatementCtx = QLangParser.StatementContext
ObsDeclCtx = QLangParser.ObsDeclContext
NumExprCtx = QLangParser.NumExprContext
IoStmtCtx = QLangParser.IoStmtContext
VarExprCtx = QLangParser.VarExprContext
PlaceMemberCtx = QLangParser.PlaceMemberContext
FunctionDeclCtx = QLangParser.FunctionDeclContext
ParamListCtx = QLangParser.ParamListContext
ParamCtx = QLangParser.ParamContext
BlockCtx = QLangParser.BlockContext
ObsDefCtx = QLangParser.ObsDefContext
StrExprCtx = QLangParser.StrExprContext
FunctionCallStmtCtx = QLangParser.FunctionCallStmtContext
FunctionCallExprCtx = QLangParser.FuncCallExprContext
ArgListCtx = QLangParser.ArgListContext
ForStmtCtx = QLangParser.ForStmtContext
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

