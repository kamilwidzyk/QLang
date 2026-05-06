# Generated from ../QLang/QLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QLangParser import QLangParser
else:
    from QLangParser import QLangParser

# This class defines a complete listener for a parse tree produced by QLangParser.
class QLangListener(ParseTreeListener):

    # Enter a parse tree produced by QLangParser#program.
    def enterProgram(self, ctx:QLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by QLangParser#program.
    def exitProgram(self, ctx:QLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by QLangParser#topLevelItem.
    def enterTopLevelItem(self, ctx:QLangParser.TopLevelItemContext):
        pass

    # Exit a parse tree produced by QLangParser#topLevelItem.
    def exitTopLevelItem(self, ctx:QLangParser.TopLevelItemContext):
        pass


    # Enter a parse tree produced by QLangParser#placeDecl.
    def enterPlaceDecl(self, ctx:QLangParser.PlaceDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#placeDecl.
    def exitPlaceDecl(self, ctx:QLangParser.PlaceDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#placeMember.
    def enterPlaceMember(self, ctx:QLangParser.PlaceMemberContext):
        pass

    # Exit a parse tree produced by QLangParser#placeMember.
    def exitPlaceMember(self, ctx:QLangParser.PlaceMemberContext):
        pass


    # Enter a parse tree produced by QLangParser#block.
    def enterBlock(self, ctx:QLangParser.BlockContext):
        pass

    # Exit a parse tree produced by QLangParser#block.
    def exitBlock(self, ctx:QLangParser.BlockContext):
        pass


    # Enter a parse tree produced by QLangParser#constDecl.
    def enterConstDecl(self, ctx:QLangParser.ConstDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#constDecl.
    def exitConstDecl(self, ctx:QLangParser.ConstDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#varType.
    def enterVarType(self, ctx:QLangParser.VarTypeContext):
        pass

    # Exit a parse tree produced by QLangParser#varType.
    def exitVarType(self, ctx:QLangParser.VarTypeContext):
        pass


    # Enter a parse tree produced by QLangParser#sizeVar.
    def enterSizeVar(self, ctx:QLangParser.SizeVarContext):
        pass

    # Exit a parse tree produced by QLangParser#sizeVar.
    def exitSizeVar(self, ctx:QLangParser.SizeVarContext):
        pass


    # Enter a parse tree produced by QLangParser#varAssign.
    def enterVarAssign(self, ctx:QLangParser.VarAssignContext):
        pass

    # Exit a parse tree produced by QLangParser#varAssign.
    def exitVarAssign(self, ctx:QLangParser.VarAssignContext):
        pass


    # Enter a parse tree produced by QLangParser#varNoAssign.
    def enterVarNoAssign(self, ctx:QLangParser.VarNoAssignContext):
        pass

    # Exit a parse tree produced by QLangParser#varNoAssign.
    def exitVarNoAssign(self, ctx:QLangParser.VarNoAssignContext):
        pass


    # Enter a parse tree produced by QLangParser#varParam.
    def enterVarParam(self, ctx:QLangParser.VarParamContext):
        pass

    # Exit a parse tree produced by QLangParser#varParam.
    def exitVarParam(self, ctx:QLangParser.VarParamContext):
        pass


    # Enter a parse tree produced by QLangParser#varParamDefault.
    def enterVarParamDefault(self, ctx:QLangParser.VarParamDefaultContext):
        pass

    # Exit a parse tree produced by QLangParser#varParamDefault.
    def exitVarParamDefault(self, ctx:QLangParser.VarParamDefaultContext):
        pass


    # Enter a parse tree produced by QLangParser#index.
    def enterIndex(self, ctx:QLangParser.IndexContext):
        pass

    # Exit a parse tree produced by QLangParser#index.
    def exitIndex(self, ctx:QLangParser.IndexContext):
        pass


    # Enter a parse tree produced by QLangParser#var.
    def enterVar(self, ctx:QLangParser.VarContext):
        pass

    # Exit a parse tree produced by QLangParser#var.
    def exitVar(self, ctx:QLangParser.VarContext):
        pass


    # Enter a parse tree produced by QLangParser#sizeGetter.
    def enterSizeGetter(self, ctx:QLangParser.SizeGetterContext):
        pass

    # Exit a parse tree produced by QLangParser#sizeGetter.
    def exitSizeGetter(self, ctx:QLangParser.SizeGetterContext):
        pass


    # Enter a parse tree produced by QLangParser#stateDeclaration.
    def enterStateDeclaration(self, ctx:QLangParser.StateDeclarationContext):
        pass

    # Exit a parse tree produced by QLangParser#stateDeclaration.
    def exitStateDeclaration(self, ctx:QLangParser.StateDeclarationContext):
        pass


    # Enter a parse tree produced by QLangParser#constDeclaration.
    def enterConstDeclaration(self, ctx:QLangParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by QLangParser#constDeclaration.
    def exitConstDeclaration(self, ctx:QLangParser.ConstDeclarationContext):
        pass


    # Enter a parse tree produced by QLangParser#varDeclaration.
    def enterVarDeclaration(self, ctx:QLangParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by QLangParser#varDeclaration.
    def exitVarDeclaration(self, ctx:QLangParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by QLangParser#receiveDeclaration.
    def enterReceiveDeclaration(self, ctx:QLangParser.ReceiveDeclarationContext):
        pass

    # Exit a parse tree produced by QLangParser#receiveDeclaration.
    def exitReceiveDeclaration(self, ctx:QLangParser.ReceiveDeclarationContext):
        pass


    # Enter a parse tree produced by QLangParser#sendStatement.
    def enterSendStatement(self, ctx:QLangParser.SendStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#sendStatement.
    def exitSendStatement(self, ctx:QLangParser.SendStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#gateStatement.
    def enterGateStatement(self, ctx:QLangParser.GateStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#gateStatement.
    def exitGateStatement(self, ctx:QLangParser.GateStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#measureStatement.
    def enterMeasureStatement(self, ctx:QLangParser.MeasureStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#measureStatement.
    def exitMeasureStatement(self, ctx:QLangParser.MeasureStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:QLangParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:QLangParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#functionCallStatement.
    def enterFunctionCallStatement(self, ctx:QLangParser.FunctionCallStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#functionCallStatement.
    def exitFunctionCallStatement(self, ctx:QLangParser.FunctionCallStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#ifStatement.
    def enterIfStatement(self, ctx:QLangParser.IfStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#ifStatement.
    def exitIfStatement(self, ctx:QLangParser.IfStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#forStatement.
    def enterForStatement(self, ctx:QLangParser.ForStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#forStatement.
    def exitForStatement(self, ctx:QLangParser.ForStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#whileStatement.
    def enterWhileStatement(self, ctx:QLangParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#whileStatement.
    def exitWhileStatement(self, ctx:QLangParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#ioStatement.
    def enterIoStatement(self, ctx:QLangParser.IoStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#ioStatement.
    def exitIoStatement(self, ctx:QLangParser.IoStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#breakStatement.
    def enterBreakStatement(self, ctx:QLangParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#breakStatement.
    def exitBreakStatement(self, ctx:QLangParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#continueStatement.
    def enterContinueStatement(self, ctx:QLangParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#continueStatement.
    def exitContinueStatement(self, ctx:QLangParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#returnStatement.
    def enterReturnStatement(self, ctx:QLangParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#returnStatement.
    def exitReturnStatement(self, ctx:QLangParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#blockStatement.
    def enterBlockStatement(self, ctx:QLangParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#blockStatement.
    def exitBlockStatement(self, ctx:QLangParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#exprStatement.
    def enterExprStatement(self, ctx:QLangParser.ExprStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#exprStatement.
    def exitExprStatement(self, ctx:QLangParser.ExprStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#equationStatement.
    def enterEquationStatement(self, ctx:QLangParser.EquationStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#equationStatement.
    def exitEquationStatement(self, ctx:QLangParser.EquationStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#semicolonStatement.
    def enterSemicolonStatement(self, ctx:QLangParser.SemicolonStatementContext):
        pass

    # Exit a parse tree produced by QLangParser#semicolonStatement.
    def exitSemicolonStatement(self, ctx:QLangParser.SemicolonStatementContext):
        pass


    # Enter a parse tree produced by QLangParser#equation.
    def enterEquation(self, ctx:QLangParser.EquationContext):
        pass

    # Exit a parse tree produced by QLangParser#equation.
    def exitEquation(self, ctx:QLangParser.EquationContext):
        pass


    # Enter a parse tree produced by QLangParser#varUnknown.
    def enterVarUnknown(self, ctx:QLangParser.VarUnknownContext):
        pass

    # Exit a parse tree produced by QLangParser#varUnknown.
    def exitVarUnknown(self, ctx:QLangParser.VarUnknownContext):
        pass


    # Enter a parse tree produced by QLangParser#multipleStateDecl.
    def enterMultipleStateDecl(self, ctx:QLangParser.MultipleStateDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#multipleStateDecl.
    def exitMultipleStateDecl(self, ctx:QLangParser.MultipleStateDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#superposedStateDecl.
    def enterSuperposedStateDecl(self, ctx:QLangParser.SuperposedStateDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#superposedStateDecl.
    def exitSuperposedStateDecl(self, ctx:QLangParser.SuperposedStateDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#varDecl.
    def enterVarDecl(self, ctx:QLangParser.VarDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#varDecl.
    def exitVarDecl(self, ctx:QLangParser.VarDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#assignStmt.
    def enterAssignStmt(self, ctx:QLangParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#assignStmt.
    def exitAssignStmt(self, ctx:QLangParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#functionDecl.
    def enterFunctionDecl(self, ctx:QLangParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#functionDecl.
    def exitFunctionDecl(self, ctx:QLangParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#paramList.
    def enterParamList(self, ctx:QLangParser.ParamListContext):
        pass

    # Exit a parse tree produced by QLangParser#paramList.
    def exitParamList(self, ctx:QLangParser.ParamListContext):
        pass


    # Enter a parse tree produced by QLangParser#param.
    def enterParam(self, ctx:QLangParser.ParamContext):
        pass

    # Exit a parse tree produced by QLangParser#param.
    def exitParam(self, ctx:QLangParser.ParamContext):
        pass


    # Enter a parse tree produced by QLangParser#multipleParam.
    def enterMultipleParam(self, ctx:QLangParser.MultipleParamContext):
        pass

    # Exit a parse tree produced by QLangParser#multipleParam.
    def exitMultipleParam(self, ctx:QLangParser.MultipleParamContext):
        pass


    # Enter a parse tree produced by QLangParser#functionCallStmt.
    def enterFunctionCallStmt(self, ctx:QLangParser.FunctionCallStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#functionCallStmt.
    def exitFunctionCallStmt(self, ctx:QLangParser.FunctionCallStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#argList.
    def enterArgList(self, ctx:QLangParser.ArgListContext):
        pass

    # Exit a parse tree produced by QLangParser#argList.
    def exitArgList(self, ctx:QLangParser.ArgListContext):
        pass


    # Enter a parse tree produced by QLangParser#standardArgList.
    def enterStandardArgList(self, ctx:QLangParser.StandardArgListContext):
        pass

    # Exit a parse tree produced by QLangParser#standardArgList.
    def exitStandardArgList(self, ctx:QLangParser.StandardArgListContext):
        pass


    # Enter a parse tree produced by QLangParser#namedArgList.
    def enterNamedArgList(self, ctx:QLangParser.NamedArgListContext):
        pass

    # Exit a parse tree produced by QLangParser#namedArgList.
    def exitNamedArgList(self, ctx:QLangParser.NamedArgListContext):
        pass


    # Enter a parse tree produced by QLangParser#shortIfStmt.
    def enterShortIfStmt(self, ctx:QLangParser.ShortIfStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#shortIfStmt.
    def exitShortIfStmt(self, ctx:QLangParser.ShortIfStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#ifStmt.
    def enterIfStmt(self, ctx:QLangParser.IfStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#ifStmt.
    def exitIfStmt(self, ctx:QLangParser.IfStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#forStmt.
    def enterForStmt(self, ctx:QLangParser.ForStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#forStmt.
    def exitForStmt(self, ctx:QLangParser.ForStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#whileStmt.
    def enterWhileStmt(self, ctx:QLangParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#whileStmt.
    def exitWhileStmt(self, ctx:QLangParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#ioStmt.
    def enterIoStmt(self, ctx:QLangParser.IoStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#ioStmt.
    def exitIoStmt(self, ctx:QLangParser.IoStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#constraint.
    def enterConstraint(self, ctx:QLangParser.ConstraintContext):
        pass

    # Exit a parse tree produced by QLangParser#constraint.
    def exitConstraint(self, ctx:QLangParser.ConstraintContext):
        pass


    # Enter a parse tree produced by QLangParser#format.
    def enterFormat(self, ctx:QLangParser.FormatContext):
        pass

    # Exit a parse tree produced by QLangParser#format.
    def exitFormat(self, ctx:QLangParser.FormatContext):
        pass


    # Enter a parse tree produced by QLangParser#AndExpr.
    def enterAndExpr(self, ctx:QLangParser.AndExprContext):
        pass

    # Exit a parse tree produced by QLangParser#AndExpr.
    def exitAndExpr(self, ctx:QLangParser.AndExprContext):
        pass


    # Enter a parse tree produced by QLangParser#BoolExpr.
    def enterBoolExpr(self, ctx:QLangParser.BoolExprContext):
        pass

    # Exit a parse tree produced by QLangParser#BoolExpr.
    def exitBoolExpr(self, ctx:QLangParser.BoolExprContext):
        pass


    # Enter a parse tree produced by QLangParser#IntNumExpr.
    def enterIntNumExpr(self, ctx:QLangParser.IntNumExprContext):
        pass

    # Exit a parse tree produced by QLangParser#IntNumExpr.
    def exitIntNumExpr(self, ctx:QLangParser.IntNumExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PowExpr.
    def enterPowExpr(self, ctx:QLangParser.PowExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PowExpr.
    def exitPowExpr(self, ctx:QLangParser.PowExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PostIncrementExpr.
    def enterPostIncrementExpr(self, ctx:QLangParser.PostIncrementExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PostIncrementExpr.
    def exitPostIncrementExpr(self, ctx:QLangParser.PostIncrementExprContext):
        pass


    # Enter a parse tree produced by QLangParser#MinusEqExpr.
    def enterMinusEqExpr(self, ctx:QLangParser.MinusEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#MinusEqExpr.
    def exitMinusEqExpr(self, ctx:QLangParser.MinusEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PreIncrementExpr.
    def enterPreIncrementExpr(self, ctx:QLangParser.PreIncrementExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PreIncrementExpr.
    def exitPreIncrementExpr(self, ctx:QLangParser.PreIncrementExprContext):
        pass


    # Enter a parse tree produced by QLangParser#DivEqExpr.
    def enterDivEqExpr(self, ctx:QLangParser.DivEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#DivEqExpr.
    def exitDivEqExpr(self, ctx:QLangParser.DivEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PlusExpr.
    def enterPlusExpr(self, ctx:QLangParser.PlusExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PlusExpr.
    def exitPlusExpr(self, ctx:QLangParser.PlusExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PostDecrementExpr.
    def enterPostDecrementExpr(self, ctx:QLangParser.PostDecrementExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PostDecrementExpr.
    def exitPostDecrementExpr(self, ctx:QLangParser.PostDecrementExprContext):
        pass


    # Enter a parse tree produced by QLangParser#NumExpr.
    def enterNumExpr(self, ctx:QLangParser.NumExprContext):
        pass

    # Exit a parse tree produced by QLangParser#NumExpr.
    def exitNumExpr(self, ctx:QLangParser.NumExprContext):
        pass


    # Enter a parse tree produced by QLangParser#VarExpr.
    def enterVarExpr(self, ctx:QLangParser.VarExprContext):
        pass

    # Exit a parse tree produced by QLangParser#VarExpr.
    def exitVarExpr(self, ctx:QLangParser.VarExprContext):
        pass


    # Enter a parse tree produced by QLangParser#StrExpr.
    def enterStrExpr(self, ctx:QLangParser.StrExprContext):
        pass

    # Exit a parse tree produced by QLangParser#StrExpr.
    def exitStrExpr(self, ctx:QLangParser.StrExprContext):
        pass


    # Enter a parse tree produced by QLangParser#NotExpr.
    def enterNotExpr(self, ctx:QLangParser.NotExprContext):
        pass

    # Exit a parse tree produced by QLangParser#NotExpr.
    def exitNotExpr(self, ctx:QLangParser.NotExprContext):
        pass


    # Enter a parse tree produced by QLangParser#ListExpr.
    def enterListExpr(self, ctx:QLangParser.ListExprContext):
        pass

    # Exit a parse tree produced by QLangParser#ListExpr.
    def exitListExpr(self, ctx:QLangParser.ListExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PlusEqExpr.
    def enterPlusEqExpr(self, ctx:QLangParser.PlusEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PlusEqExpr.
    def exitPlusEqExpr(self, ctx:QLangParser.PlusEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#MinusExpr.
    def enterMinusExpr(self, ctx:QLangParser.MinusExprContext):
        pass

    # Exit a parse tree produced by QLangParser#MinusExpr.
    def exitMinusExpr(self, ctx:QLangParser.MinusExprContext):
        pass


    # Enter a parse tree produced by QLangParser#FuncCallExpr.
    def enterFuncCallExpr(self, ctx:QLangParser.FuncCallExprContext):
        pass

    # Exit a parse tree produced by QLangParser#FuncCallExpr.
    def exitFuncCallExpr(self, ctx:QLangParser.FuncCallExprContext):
        pass


    # Enter a parse tree produced by QLangParser#SizeGetterExpr.
    def enterSizeGetterExpr(self, ctx:QLangParser.SizeGetterExprContext):
        pass

    # Exit a parse tree produced by QLangParser#SizeGetterExpr.
    def exitSizeGetterExpr(self, ctx:QLangParser.SizeGetterExprContext):
        pass


    # Enter a parse tree produced by QLangParser#RelExpr.
    def enterRelExpr(self, ctx:QLangParser.RelExprContext):
        pass

    # Exit a parse tree produced by QLangParser#RelExpr.
    def exitRelExpr(self, ctx:QLangParser.RelExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PreDecrementExpr.
    def enterPreDecrementExpr(self, ctx:QLangParser.PreDecrementExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PreDecrementExpr.
    def exitPreDecrementExpr(self, ctx:QLangParser.PreDecrementExprContext):
        pass


    # Enter a parse tree produced by QLangParser#VarUnknownExpr.
    def enterVarUnknownExpr(self, ctx:QLangParser.VarUnknownExprContext):
        pass

    # Exit a parse tree produced by QLangParser#VarUnknownExpr.
    def exitVarUnknownExpr(self, ctx:QLangParser.VarUnknownExprContext):
        pass


    # Enter a parse tree produced by QLangParser#AssignmentExpr.
    def enterAssignmentExpr(self, ctx:QLangParser.AssignmentExprContext):
        pass

    # Exit a parse tree produced by QLangParser#AssignmentExpr.
    def exitAssignmentExpr(self, ctx:QLangParser.AssignmentExprContext):
        pass


    # Enter a parse tree produced by QLangParser#OrExpr.
    def enterOrExpr(self, ctx:QLangParser.OrExprContext):
        pass

    # Exit a parse tree produced by QLangParser#OrExpr.
    def exitOrExpr(self, ctx:QLangParser.OrExprContext):
        pass


    # Enter a parse tree produced by QLangParser#AndEqExpr.
    def enterAndEqExpr(self, ctx:QLangParser.AndEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#AndEqExpr.
    def exitAndEqExpr(self, ctx:QLangParser.AndEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#MulEqExpr.
    def enterMulEqExpr(self, ctx:QLangParser.MulEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#MulEqExpr.
    def exitMulEqExpr(self, ctx:QLangParser.MulEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#MulDivModExpr.
    def enterMulDivModExpr(self, ctx:QLangParser.MulDivModExprContext):
        pass

    # Exit a parse tree produced by QLangParser#MulDivModExpr.
    def exitMulDivModExpr(self, ctx:QLangParser.MulDivModExprContext):
        pass


    # Enter a parse tree produced by QLangParser#EqExpr.
    def enterEqExpr(self, ctx:QLangParser.EqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#EqExpr.
    def exitEqExpr(self, ctx:QLangParser.EqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#PowEqExpr.
    def enterPowEqExpr(self, ctx:QLangParser.PowEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#PowEqExpr.
    def exitPowEqExpr(self, ctx:QLangParser.PowEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#ParenExpr.
    def enterParenExpr(self, ctx:QLangParser.ParenExprContext):
        pass

    # Exit a parse tree produced by QLangParser#ParenExpr.
    def exitParenExpr(self, ctx:QLangParser.ParenExprContext):
        pass


    # Enter a parse tree produced by QLangParser#ModEqExpr.
    def enterModEqExpr(self, ctx:QLangParser.ModEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#ModEqExpr.
    def exitModEqExpr(self, ctx:QLangParser.ModEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:QLangParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by QLangParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:QLangParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by QLangParser#OrEqExpr.
    def enterOrEqExpr(self, ctx:QLangParser.OrEqExprContext):
        pass

    # Exit a parse tree produced by QLangParser#OrEqExpr.
    def exitOrEqExpr(self, ctx:QLangParser.OrEqExprContext):
        pass


    # Enter a parse tree produced by QLangParser#receiveDecl.
    def enterReceiveDecl(self, ctx:QLangParser.ReceiveDeclContext):
        pass

    # Exit a parse tree produced by QLangParser#receiveDecl.
    def exitReceiveDecl(self, ctx:QLangParser.ReceiveDeclContext):
        pass


    # Enter a parse tree produced by QLangParser#receiveOpt.
    def enterReceiveOpt(self, ctx:QLangParser.ReceiveOptContext):
        pass

    # Exit a parse tree produced by QLangParser#receiveOpt.
    def exitReceiveOpt(self, ctx:QLangParser.ReceiveOptContext):
        pass


    # Enter a parse tree produced by QLangParser#sendStmt.
    def enterSendStmt(self, ctx:QLangParser.SendStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#sendStmt.
    def exitSendStmt(self, ctx:QLangParser.SendStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#gateStmt.
    def enterGateStmt(self, ctx:QLangParser.GateStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#gateStmt.
    def exitGateStmt(self, ctx:QLangParser.GateStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#singleQubitGate.
    def enterSingleQubitGate(self, ctx:QLangParser.SingleQubitGateContext):
        pass

    # Exit a parse tree produced by QLangParser#singleQubitGate.
    def exitSingleQubitGate(self, ctx:QLangParser.SingleQubitGateContext):
        pass


    # Enter a parse tree produced by QLangParser#multiQubitGate.
    def enterMultiQubitGate(self, ctx:QLangParser.MultiQubitGateContext):
        pass

    # Exit a parse tree produced by QLangParser#multiQubitGate.
    def exitMultiQubitGate(self, ctx:QLangParser.MultiQubitGateContext):
        pass


    # Enter a parse tree produced by QLangParser#measureStmt.
    def enterMeasureStmt(self, ctx:QLangParser.MeasureStmtContext):
        pass

    # Exit a parse tree produced by QLangParser#measureStmt.
    def exitMeasureStmt(self, ctx:QLangParser.MeasureStmtContext):
        pass


    # Enter a parse tree produced by QLangParser#emptyList.
    def enterEmptyList(self, ctx:QLangParser.EmptyListContext):
        pass

    # Exit a parse tree produced by QLangParser#emptyList.
    def exitEmptyList(self, ctx:QLangParser.EmptyListContext):
        pass


    # Enter a parse tree produced by QLangParser#nonEmptyList.
    def enterNonEmptyList(self, ctx:QLangParser.NonEmptyListContext):
        pass

    # Exit a parse tree produced by QLangParser#nonEmptyList.
    def exitNonEmptyList(self, ctx:QLangParser.NonEmptyListContext):
        pass



del QLangParser