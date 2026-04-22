# Generated from ../QLang/QLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QLangParser import QLangParser
else:
    from QLangParser import QLangParser

# This class defines a complete generic visitor for a parse tree produced by QLangParser.

class QLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QLangParser#program.
    def visitProgram(self, ctx:QLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#topLevelItem.
    def visitTopLevelItem(self, ctx:QLangParser.TopLevelItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#placeDecl.
    def visitPlaceDecl(self, ctx:QLangParser.PlaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#placeMember.
    def visitPlaceMember(self, ctx:QLangParser.PlaceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#functionDecl.
    def visitFunctionDecl(self, ctx:QLangParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#paramList.
    def visitParamList(self, ctx:QLangParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#param.
    def visitParam(self, ctx:QLangParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#block.
    def visitBlock(self, ctx:QLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#stateDeclaration.
    def visitStateDeclaration(self, ctx:QLangParser.StateDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#obsDeclaration.
    def visitObsDeclaration(self, ctx:QLangParser.ObsDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#numDeclaration.
    def visitNumDeclaration(self, ctx:QLangParser.NumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#receiveDeclaration.
    def visitReceiveDeclaration(self, ctx:QLangParser.ReceiveDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#sendStatement.
    def visitSendStatement(self, ctx:QLangParser.SendStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#gateStatement.
    def visitGateStatement(self, ctx:QLangParser.GateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#measureStatement.
    def visitMeasureStatement(self, ctx:QLangParser.MeasureStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:QLangParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#functionCallStatement.
    def visitFunctionCallStatement(self, ctx:QLangParser.FunctionCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#ifStatement.
    def visitIfStatement(self, ctx:QLangParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#forStatement.
    def visitForStatement(self, ctx:QLangParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#whileStatement.
    def visitWhileStatement(self, ctx:QLangParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#ioStatement.
    def visitIoStatement(self, ctx:QLangParser.IoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#breakStatement.
    def visitBreakStatement(self, ctx:QLangParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#continueStatement.
    def visitContinueStatement(self, ctx:QLangParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#returnStatement.
    def visitReturnStatement(self, ctx:QLangParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#blockStatement.
    def visitBlockStatement(self, ctx:QLangParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#exprStatement.
    def visitExprStatement(self, ctx:QLangParser.ExprStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#equationStatement.
    def visitEquationStatement(self, ctx:QLangParser.EquationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#semicolonStatement.
    def visitSemicolonStatement(self, ctx:QLangParser.SemicolonStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#equation.
    def visitEquation(self, ctx:QLangParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#stateDecl.
    def visitStateDecl(self, ctx:QLangParser.StateDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#stateDef.
    def visitStateDef(self, ctx:QLangParser.StateDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#obsDecl.
    def visitObsDecl(self, ctx:QLangParser.ObsDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#obsDef.
    def visitObsDef(self, ctx:QLangParser.ObsDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#numDecl.
    def visitNumDecl(self, ctx:QLangParser.NumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#receiveDecl.
    def visitReceiveDecl(self, ctx:QLangParser.ReceiveDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#receiveOpt.
    def visitReceiveOpt(self, ctx:QLangParser.ReceiveOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#sendStmt.
    def visitSendStmt(self, ctx:QLangParser.SendStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#gateStmt.
    def visitGateStmt(self, ctx:QLangParser.GateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#singleQubitGate.
    def visitSingleQubitGate(self, ctx:QLangParser.SingleQubitGateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#multiQubitGate.
    def visitMultiQubitGate(self, ctx:QLangParser.MultiQubitGateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#measureStmt.
    def visitMeasureStmt(self, ctx:QLangParser.MeasureStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#assignStmt.
    def visitAssignStmt(self, ctx:QLangParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#functionCallStmt.
    def visitFunctionCallStmt(self, ctx:QLangParser.FunctionCallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#ifStmt.
    def visitIfStmt(self, ctx:QLangParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#forStmt.
    def visitForStmt(self, ctx:QLangParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#whileStmt.
    def visitWhileStmt(self, ctx:QLangParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#ioStmt.
    def visitIoStmt(self, ctx:QLangParser.IoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#constraint.
    def visitConstraint(self, ctx:QLangParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#format.
    def visitFormat(self, ctx:QLangParser.FormatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#argList.
    def visitArgList(self, ctx:QLangParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#AndExpr.
    def visitAndExpr(self, ctx:QLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#BoolExpr.
    def visitBoolExpr(self, ctx:QLangParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PowExpr.
    def visitPowExpr(self, ctx:QLangParser.PowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PostIncrementExpr.
    def visitPostIncrementExpr(self, ctx:QLangParser.PostIncrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#MinusEqExpr.
    def visitMinusEqExpr(self, ctx:QLangParser.MinusEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PreIncrementExpr.
    def visitPreIncrementExpr(self, ctx:QLangParser.PreIncrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#DivEqExpr.
    def visitDivEqExpr(self, ctx:QLangParser.DivEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PlusExpr.
    def visitPlusExpr(self, ctx:QLangParser.PlusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PostDecrementExpr.
    def visitPostDecrementExpr(self, ctx:QLangParser.PostDecrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#NumExpr.
    def visitNumExpr(self, ctx:QLangParser.NumExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#VarExpr.
    def visitVarExpr(self, ctx:QLangParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#StrExpr.
    def visitStrExpr(self, ctx:QLangParser.StrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#NotExpr.
    def visitNotExpr(self, ctx:QLangParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PlusEqExpr.
    def visitPlusEqExpr(self, ctx:QLangParser.PlusEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#MinusExpr.
    def visitMinusExpr(self, ctx:QLangParser.MinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#FuncCallExpr.
    def visitFuncCallExpr(self, ctx:QLangParser.FuncCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#RelExpr.
    def visitRelExpr(self, ctx:QLangParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PreDecrementExpr.
    def visitPreDecrementExpr(self, ctx:QLangParser.PreDecrementExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#OrExpr.
    def visitOrExpr(self, ctx:QLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#AndEqExpr.
    def visitAndEqExpr(self, ctx:QLangParser.AndEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#MulEqExpr.
    def visitMulEqExpr(self, ctx:QLangParser.MulEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#MulDivModExpr.
    def visitMulDivModExpr(self, ctx:QLangParser.MulDivModExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#EqExpr.
    def visitEqExpr(self, ctx:QLangParser.EqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PowEqExpr.
    def visitPowEqExpr(self, ctx:QLangParser.PowEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#ParenExpr.
    def visitParenExpr(self, ctx:QLangParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#ModEqExpr.
    def visitModEqExpr(self, ctx:QLangParser.ModEqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:QLangParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#OrEqExpr.
    def visitOrEqExpr(self, ctx:QLangParser.OrEqExprContext):
        return self.visitChildren(ctx)



del QLangParser