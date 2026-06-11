"""
This file contains consts that are accessed from multiple files
Do not import anything from this module to not make a cyclic import
"""

from antlr4.tree.Tree import TerminalNode
from .QLang.QLangParser import QLangParser

################### TOP LEVEL #####################
TerminalCtx = TerminalNode
ProgramCtx = QLangParser.ProgramContext
StatementCtx = QLangParser.StatementContext
### FUNCTION DECLARATION ###
FunctionDeclCtx = QLangParser.FunctionDeclContext
FunctionDeclStatementCtx = QLangParser.FunctionDeclStatementContext
### FUNCTION PARAMS ###
ParamListCtx = QLangParser.ParamListContext
ParamCtx = QLangParser.ParamContext

### PLACE DECLARATION ###
PlaceDeclCtx = QLangParser.PlaceDeclContext
PlaceMemberCtx = QLangParser.PlaceMemberContext
### CODE BLOCK ###
BlockCtx = QLangParser.BlockContext


#################### VARIABLES ####################
VarDeclCtx = QLangParser.VarDeclContext
AssigmentStmtCtx = QLangParser.AssignStmtContext
AssignExprCtx = QLangParser.AssignmentExprContext
### CONST ###
ConstDeclarationCtx = QLangParser.ConstDeclarationContext
ConstDeclCtx = QLangParser.ConstDeclContext
### SIZE '#' ###
SizeGetterExprCtx = QLangParser.SizeGetterExprContext
SizeGetterCtx = QLangParser.SizeGetterContext
### TYPE '$' ###
TypeExprCtx = QLangParser.TypeExprContext
### REFERENCE '@' ###
ReferenceCtx = QLangParser.ReferenceContext
### QUANTUM ###
GateStmtCtx = QLangParser.GateStmtContext
MeasureExprCtx = QLangParser.MeasureExprContext
### LIST ###
ListExprCtx = QLangParser.ListExprContext
ListCtx = QLangParser.ListContext
EmptyListCtx = QLangParser.EmptyListContext
NonEmptyListCtx = QLangParser.NonEmptyListContext
### RESET ###
ResetExprCtx = QLangParser.ResetExprContext
### PARENT '^' ###
ParentExprCtx = QLangParser.ParentExprContext


#################### FUNCTION CALL ####################
FunctionCallStmtCtx = QLangParser.FunctionCallStmtContext
ArgListCtx = QLangParser.ArgListContext
FunctionCallExprCtx = QLangParser.FuncCallExprContext


#################### CONTROL ####################
### IF ###
IfStmtCtx = QLangParser.IfStmtContext
# TERNARY #
ShortIfExprCtx = QLangParser.ShortIfExprContext
### FOR ###
ForStmtCtx = QLangParser.ForStmtContext
### WHILE ###
WhileStmtCtx = QLangParser.WhileStmtContext
### ITERATE ###
IterateStmtCtx = QLangParser.IterateStmtContext


#################### TIME ####################
### WAIT ###
waitStmtCtx = QLangParser.WaitStmtContext
### TIME UNITS ###
timeUnitCtx = QLangParser.TimeUnitContext
secondUnitCtx = QLangParser.SecondUnitContext
millisUnitCtx = QLangParser.MillisUnitContext
minuteUnitCtx = QLangParser.MinuteUnitContext
hourUnitCtx = QLangParser.HourUnitContext


#################### CONSOLE INPUT/OUTPUT ####################
IoStmtCtx = QLangParser.IoStmtContext
ConstraintCtx = QLangParser.ConstraintContext
FormatCtx = QLangParser.FormatContext


#################### EXPRESSIONS ####################
ParenExprCtx = QLangParser.ParenExprContext
##### LOGIC #####
# T/F #
BoolExprCtx = QLangParser.BoolExprContext
BoolValueCtx = QLangParser.BoolValueContext
BoolValueTrueCtx = QLangParser.BoolValueTrueContext
BoolValueFalseCtx = QLangParser.BoolValueFalseContext
# OR #
OrExprCtx = QLangParser.OrExprContext
# AND #
AndExprCtx = QLangParser.AndExprContext
# NOT #
NotExprContext = QLangParser.NotExprContext

##### VARIABLES / STRINGS #####
VarExprCtx = QLangParser.VarExprContext
StrExprCtx = QLangParser.StrExprContext
NullExprCtx = QLangParser.NullExprContext

##### NUMBERS #####
NumExprCtx = QLangParser.NumExprContext
IntNumExprCtx = QLangParser.IntNumExprContext
NumCastExprCtx = QLangParser.NumCastExprContext
# MINUS #
MinusExprCtx = QLangParser.MinusExprContext
# PLUS #
PlusExprCtx = QLangParser.PlusExprContext
# PRE/POST INC/DEC #
PreIncrementCtx = QLangParser.PreIncrementExprContext
PostIncrementCtx = QLangParser.PostIncrementExprContext
PreDecrementCtx = QLangParser.PreDecrementExprContext
PostDecrementCtx = QLangParser.PostDecrementExprContext

##### MATH #####
# POWER #
PowExprCtx = QLangParser.PowExprContext
# MULTIPLICATION/DIVISION/MODULO #
MulDivModExprCtx = QLangParser.MulDivModExprContext
# ADDITION/SUBSTRACTION #
AddSubExprContext = QLangParser.AddSubExprContext

##### COMPOUND #####
PlusEqExprCtx = QLangParser.PlusEqExprContext
MinusEqExprCtx = QLangParser.MinusEqExprContext
MulEqExprCtx = QLangParser.MulEqExprContext
DivEqExprCtx = QLangParser.DivEqExprContext
ModEqExprCtx = QLangParser.ModEqExprContext
PowEqExprCtx = QLangParser.PowEqExprContext
AndEqExprCtx = QLangParser.AndEqExprContext
OrEqExprCtx = QLangParser.OrEqExprContext

##### COMPARISION #####
# RELATIVE #
RelExprContext = QLangParser.RelExprContext
# EQUAL/NOT EQUAL #
EqExprCtx = QLangParser.EqExprContext


#################### NETWORK ####################
SendStmtCtx = QLangParser.SendStmtContext
ReceiveDeclCtx = QLangParser.ReceiveDeclContext
AvailableExprContext = QLangParser.AvailableExprAltContext

