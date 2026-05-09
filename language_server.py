import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'int'))

from pygls.server import LanguageServer
from pygls.protocol import LanguageServerProtocol
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    SemanticTokens,
    SemanticTokensLegend,
    SemanticTokenTypes,
    SemanticTokenModifiers,
    Diagnostic,
    DiagnosticSeverity,
    Range,
    Position,
    Hover,
    MarkupContent,
    MarkupKind,
)
from antlr4 import InputStream, CommonTokenStream
from int.QLang.QLangLexer import QLangLexer
from int.QLang.QLangParser import QLangParser
from int.QLang.QLangVisitor import QLangVisitor
from typing import Dict, List, Optional, Tuple

# Define token types for semantic highlighting
TOKEN_TYPES = [
    SemanticTokenTypes.Variable,
    SemanticTokenTypes.Function,
    SemanticTokenTypes.Type,
]

TOKEN_MODIFIERS = [
    SemanticTokenModifiers.Definition,
]

class Symbol:
    def __init__(self, name: str, symbol_type: str, position: Position, var_type: Optional[str] = None):
        self.name = name
        self.symbol_type = symbol_type  # 'variable' or 'function'
        self.position = position
        self.var_type = var_type  # for variables: 'num', 'obs', 'state'

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.errors: List[Tuple[Range, str, str]] = []
        self.semantic_tokens: List[Tuple[int, int, int, int, int]] = []  # line, start_char, length, token_type, modifiers

    def add_symbol(self, name: str, symbol_type: str, position: Position, var_type: Optional[str] = None):
        self.symbols[name] = Symbol(name, symbol_type, position, var_type)

    def get_symbol(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def add_error(self, range_: Range, title: str, message: str):
        self.errors.append((range_, title, message))

    def add_semantic_token(self, line: int, start_char: int, length: int, token_type: int, modifiers: int = 0):
        self.semantic_tokens.append((line, start_char, length, token_type, modifiers))

class QLangAnalyzer(QLangVisitor):
    def __init__(self, text: str):
        self.text = text
        self.symbol_table = SymbolTable()
        self.lines = text.split('\n')

    def get_position(self, ctx) -> Position:
        start = ctx.start
        return Position(line=start.line - 1, character=start.column)

    def get_range(self, ctx) -> Range:
        start = ctx.start
        stop = ctx.stop
        return Range(
            start=Position(line=start.line - 1, character=start.column),
            end=Position(line=stop.line - 1, character=stop.column + len(stop.text))
        )

    def visitVarDecl(self, ctx):
        var_type = ctx.varType().getText().lower()
        for assign in ctx.varAssign():
            var_name = assign.ID().getText()
            pos = self.get_position(assign)
            self.symbol_table.add_symbol(var_name, 'variable', pos, var_type)
            # Add semantic token for definition
            start = assign.ID().symbol
            line = start.line - 1
            start_char = start.column
            length = len(var_name)
            token_type = TOKEN_TYPES.index(SemanticTokenTypes.Variable)
            modifiers = 1 << TOKEN_MODIFIERS.index(SemanticTokenModifiers.Definition)
            self.symbol_table.add_semantic_token(line, start_char, length, token_type, modifiers)
        return self.visitChildren(ctx)

    def visitFunctionDecl(self, ctx):
        func_name = ctx.ID().getText()
        pos = self.get_position(ctx)
        return_type = ctx.varType().getText().lower()
        self.symbol_table.add_symbol(func_name, 'function', pos, return_type)
        # Add semantic token
        start = ctx.ID().symbol
        line = start.line - 1
        start_char = start.column
        length = len(func_name)
        token_type = TOKEN_TYPES.index(SemanticTokenTypes.Function)
        modifiers = 1 << TOKEN_MODIFIERS.index(SemanticTokenModifiers.Definition)
        self.symbol_table.add_semantic_token(line, start_char, length, token_type, modifiers)
        return self.visitChildren(ctx)

    def visitVar(self, ctx):
        var_name = ctx.ID().getText()
        symbol = self.symbol_table.get_symbol(var_name)
        if symbol:
            # Add semantic token for use
            start = ctx.ID().symbol
            line = start.line - 1
            start_char = start.column
            length = len(var_name)
            token_type = TOKEN_TYPES.index(SemanticTokenTypes.Variable)
            self.symbol_table.add_semantic_token(line, start_char, length, token_type)
        else:
            range_ = self.get_range(ctx)
            self.symbol_table.add_error(range_, "Undefined variable", f"Variable '{var_name}' is not defined")
        return self.visitChildren(ctx)

    def visitFuncCallExpr(self, ctx):
        func_name = ctx.ID().getText()
        symbol = self.symbol_table.get_symbol(func_name)
        if symbol:
            start = ctx.ID().symbol
            line = start.line - 1
            start_char = start.column
            length = len(func_name)
            token_type = TOKEN_TYPES.index(SemanticTokenTypes.Function)
            self.symbol_table.add_semantic_token(line, start_char, length, token_type)
        else:
            range_ = self.get_range(ctx)
            self.symbol_table.add_error(range_, "Undefined function", f"Function '{func_name}' is not defined")
        return self.visitChildren(ctx)

    def visitAssignStmt(self, ctx):
        var_ctx = ctx.var()
        expr_ctx = ctx.expr()
        var_name = var_ctx.ID().getText()
        symbol = self.symbol_table.get_symbol(var_name)
        if symbol and symbol.var_type == 'num':
            # Check if expr is string
            expr_text = expr_ctx.getText()
            if expr_text.startswith('"') and expr_text.endswith('"'):
                range_ = self.get_range(expr_ctx)
                self.symbol_table.add_error(range_, "Type mismatch", "Cannot assign string to num variable")
        return self.visitChildren(ctx)

server = LanguageServer("qlang-language-server", "1.0.0")
server.semantic_tokens_legend = SemanticTokensLegend(token_types=TOKEN_TYPES, token_modifiers=TOKEN_MODIFIERS)

def encode_semantic_tokens(tokens):
    if not tokens:
        return []
    sorted_tokens = sorted(tokens, key=lambda x: (x[0], x[1]))
    data = []
    prev_line = 0
    prev_start = 0
    for line, start, length, token_type, modifiers in sorted_tokens:
        delta_line = line - prev_line
        delta_start = start if delta_line == 0 else start
        data.extend([delta_line, delta_start, length, token_type, modifiers])
        prev_line = line
        prev_start = start
    return data

@server.feature(TEXT_DOCUMENT_DID_OPEN)
@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params):
    uri = params.text_document.uri
    text = params.text_document.text if hasattr(params, 'text_document') and hasattr(params.text_document, 'text') else params.content_changes[0].text

    # Parse
    input_stream = InputStream(text)
    lexer = QLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = QLangParser(token_stream)
    tree = parser.program()

    # Analyze
    analyzer = QLangAnalyzer(text)
    analyzer.visit(tree)

    # Store
    if not hasattr(ls, 'analyzers'):
        ls.analyzers = {}
    ls.analyzers[uri] = analyzer

    # Send diagnostics
    diagnostics = []
    for range_, title, message in analyzer.symbol_table.errors:
        diagnostics.append(Diagnostic(
            range=range_,
            severity=DiagnosticSeverity.Error,
            message=f"{title}: {message}",
            source="qlang"
        ))
    ls.publish_diagnostics(uri, diagnostics)

@server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params):
    uri = params.text_document.uri
    position = params.position

    analyzer = getattr(ls, 'analyzers', {}).get(uri)
    if analyzer:
        for range_, title, message in analyzer.symbol_table.errors:
            if range_.start.line <= position.line <= range_.end.line and \
               range_.start.character <= position.character <= range_.end.character:
                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"**{title}**\n\n{message}"
                    ),
                    range=range_
                )
    return None

@server.feature(TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL)
def semantic_tokens(ls: LanguageServer, params):
    uri = params.text_document.uri
    analyzer = getattr(ls, 'analyzers', {}).get(uri)
    if analyzer:
        data = encode_semantic_tokens(analyzer.symbol_table.semantic_tokens)
        return SemanticTokens(data=data)
    return SemanticTokens(data=[])

if __name__ == '__main__':
    server.start_io()