"""
This file contains consts that are access from multiple files
Do not import anything from this module to not make a cyclic import
"""


# Tree block types
STATEMENT_CONTEXT = "StatementContext" # any statement
OBS_DECL_CONTEXT = "ObsDeclContext" # declaration of Observation variable
NUM_EXPR_CONTEXT = "NumExprContext" # number expr = just a number
TERMINAL = "Terminal" # terminal string
IO_STMT_CONTEXT = "IoStmtContext" # print/println/input/debug
VAR_EXPR_CONTEXT = "VarExprContext" # <name>[<index>] or <name>
FORMAT_CONTEXT = "FormatContext" # print format option
PLACE_MEMBER_CONTEXT = "PlaceMemberContext" # top level items of place block
FUNCTION_DECL_CONTEXT = "FunctionDeclContext" # function declaration
BLOCK_CONTEXT = "BlockContext" # block of code in { }
PARAM_LIST_CONTEXT = "ParamListContext" # list of function parameters
PARAM_CONTEXT = "ParamContext" # one function parameter (part of the list)
OBS_DEF_CONTEXT = "ObsDefContext" # Observation definition list item
STR_EXPR_CONTEXT = "StrExprContext" # String literal
FUNCTION_CALL_STMT_CONTEXT = "FunctionCallStmtContext"
FUNCTION_CALL_EXPR_CONTEXT = "FuncCallExprContext"
ARG_LIST_CONTEXT = "ArgListContext" # Argument list of function call
FOR_STMT_CONTEXT = "ForStmtContext" # For loop
POW_EXPR_CONTEXT = "PowExprContext" # x^b 
IF_STMT_CONTEXT = "IfStmtContext" # If
REL_EXPR_CONTEXT = "RelExprContext" # comparision operators
ADD_SUB_EXPR_CONTEXT = "AddSubExprContext" # add(+) substract(-)
NOT_EXPR_CONTEXT = "NotExprContext" # not(!) 0-->1 >=1-->0
MUL_DIV_MOD_EXPR_CONTEXT = "MulDivModExprContext" # multiply(*) divide(/) mod(%)
EQ_EXPR_CONTEXT = "EqExprContext" # equal(==) notEqual(!=)
AND_EXPR_CONTEXT = "AndExprContext" # and(&&) both > 0 --> 1
OR_EXPR_CONTEXT = "OrExprContext" # or(&&) any > 0 --> 1
BOOL_EXPR_CONTEXT = "BoolExprContext" # true(T)-->1 false(F)-->0
PAREN_EXPR_CONTEXT = "ParenExprContext" # ()
CONSTRAINT_CONTEXT = "ConstraintContext" # input min max