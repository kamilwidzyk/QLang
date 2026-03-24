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


    # Visit a parse tree produced by QLangParser#statement.
    def visitStatement(self, ctx:QLangParser.StatementContext):
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


    # Visit a parse tree produced by QLangParser#RelExpr.
    def visitRelExpr(self, ctx:QLangParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#PowExpr.
    def visitPowExpr(self, ctx:QLangParser.PowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#OrExpr.
    def visitOrExpr(self, ctx:QLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#NumExpr.
    def visitNumExpr(self, ctx:QLangParser.NumExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#MulDivModExpr.
    def visitMulDivModExpr(self, ctx:QLangParser.MulDivModExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#EqExpr.
    def visitEqExpr(self, ctx:QLangParser.EqExprContext):
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


    # Visit a parse tree produced by QLangParser#ParenExpr.
    def visitParenExpr(self, ctx:QLangParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:QLangParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QLangParser#FuncCallExpr.
    def visitFuncCallExpr(self, ctx:QLangParser.FuncCallExprContext):
        return self.visitChildren(ctx)



del QLangParser