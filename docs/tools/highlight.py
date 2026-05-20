"""
Lightweight QLang -> LaTeX syntax highlighter.
Scans the parent docs directory for .ql files, parses them with the generated
ANTLR lexer/parser and emits a .tex file next to each .ql with a single
\\begin{lstlisting}[escapeinside={(*@}{@*)}] ... \\end{lstlisting} block where
language tokens are wrapped with LaTeX color commands.

This script runs as a simple watcher: it polls for file mtime changes and
re-generates .tex outputs for new/modified .ql files.

Usage: run in background from the repository root or let make_auto.bat start it.
"""

import sys
import os
import time
from antlr4 import FileStream, CommonTokenStream, Token

# Ensure the repository root is on sys.path so we can import generated lexer/parser
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, '..', '..'))
if not os.path.exists(os.path.join(REPO_ROOT, 'int')):
    # Walk upward until we find the repository root containing int/
    candidate = THIS_DIR
    while True:
        parent = os.path.dirname(candidate)
        if parent == candidate:
            break
        if os.path.exists(os.path.join(parent, 'int')):
            REPO_ROOT = parent
            break
        candidate = parent

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from int.QLang.QLangLexer import QLangLexer
    from int.QLang.QLangParser import QLangParser
except Exception as e:
    print("Failed to import generated ANTLR lexer/parser:", e)
    print("sys.path:", sys.path[:5])
    raise


# Simple LaTeX escaping for token text used inside \textcolor{..}{...}
_LATEX_ESCAPES = {
    '\\': '\\textbackslash{}',
    '%': '\\%',
    '&': '\\&',
    '#': '\\#',
    '_': '\\_',
    '{': '\\{',
    '}': '\\}',
    '$': '\\$',
    '^': '\\^{ }',
    '~': '\\~{}',
    '"': '\\string"',
    "'": '\\string\'',
}


def escape_for_latex(s: str) -> str:
    # Replace problematic characters inside \textcolor braces
    out = []
    for ch in s:
        out.append(_LATEX_ESCAPES.get(ch, ch))
    return ''.join(out)


# Basic token->color mapping. Token names are taken from QLangLexer.symbolicNames
NUMBER_COLOR = 'codebox_number'
STRING_COLOR = 'codebox_string'
COMMENT_COLOR = 'codebox_comment'
OP_COLOR = 'codebox_operator'
IDENT_COLOR = 'black'

# Keyword styles mapped to ((color, weight), keyword set).
KEYWORD_STYLES = [
    (('codebox_builtin_operator', 'normal'), {
        'reset', 'measure', 'measureX', 'superpose', 'not', 'H',
        'superpose', 'shift', 'S', 'X', 'Y', 'Z', 'dual_not', 'phase_not',
        'entangle', 'CNOT', 'entangle_phase', 'CZ', 'swap'
    }),
    (('codebox_builtin_function', 'normal'), {
        'println', 'print', 'debug', 'input'
    }),
    (('codebox_control', 'bold'), {
        'if', 'else', 'for', 'while', 'break', 'continue', 'return',
        'from', 'to', 'step', 'elif', 'else if'
    }),
    (('codebox_constant', 'bold'), {
        'NULL', 'T', 'F'
    }),
    (('codebox_type', 'bold'), {
        'num', 'obs', 'text', 'state', 'place', 'function', 'const'
    })
]

PUNCTUATION = set('()[]{};.,:')
OPERATORS = set(['+','-','*','/','%','**','==','!=','<','>','<=','>=','&&','||','!','=',"'",'"','$','@','^', '->'])


def lexer_token_name(ttype: int, lexer: QLangLexer):
    if 0 <= ttype < len(lexer.symbolicNames):
        name = lexer.symbolicNames[ttype]
        if name:
            return name

    token_names = getattr(lexer, '_token_names_cache', None)
    if token_names is None:
        token_names = {}
        lexer_cls = type(lexer)
        for attr in dir(lexer_cls):
            if attr.isupper():
                value = getattr(lexer_cls, attr)
                if isinstance(value, int):
                    token_names[value] = attr
        lexer._token_names_cache = token_names

    return token_names.get(ttype)


def token_color(token, lexer: QLangLexer):
    ttype = token.type
    if ttype == Token.EOF:
        return None
    sym = lexer_token_name(ttype, lexer)

    text = token.text or ''

    # Strings
    if sym == 'STRING':
        return STRING_COLOR
    # Numbers
    if sym in ('INT_NUMBER', 'NUMBER'):
        return NUMBER_COLOR
    # Comments (if the lexer defines COMMENT or LINE_COMMENT)
    if sym and 'COMMENT' in sym:
        return COMMENT_COLOR
    # Keywords by token text, exact case-sensitive match
    for (color, weight), keyword_set in KEYWORD_STYLES:
        if text in keyword_set:
            return color, weight
    # Punctuation
    if text in PUNCTUATION:
        return OP_COLOR
    # Operators
    if text in OPERATORS:
        return OP_COLOR
    # Identifiers (IDs)
    if sym == 'ID':
        return IDENT_COLOR

    # Fallback: no color
    return None


def process_file(path: str):
    try:
        stream = FileStream(path, encoding='utf-8')
    except Exception:
        with open(path, 'rb') as f:
            data = f.read()
        stream = FileStream(path, encoding='utf-8')

    lexer = QLangLexer(stream)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    out_parts = []
    for tok in tokens.tokens:
        if tok.type == Token.EOF:
            break
        color = token_color(tok, lexer)
        txt = tok.text
        if txt is None:
            txt = ''

        # Preserve exact whitespace/newlines — listings will keep them.
        if color:
            # escape for LaTeX inside the \textcolor braces
            esc = escape_for_latex(txt)
            if isinstance(color, tuple):
                color_name, weight = color
                if weight == 'bold':
                    out_parts.append(f"(*@\\textcolor{{{color_name}}}{{\\textbf{{{esc}}}}}@*)")
                else:
                    out_parts.append(f"(*@\\textcolor{{{color_name}}}{{{esc}}}@*)")
            else:
                out_parts.append(f"(*@\\textcolor{{{color}}}{{{esc}}}@*)")
        else:
            # No color, add raw text but escape the sequence that would accidentally
            # create the listings escape markers
            safe = txt.replace('(*@', '(*@{}').replace('@*)', '{@*)')
            out_parts.append(safe)

    colored_code = ''.join(out_parts)

    tex_path = os.path.splitext(path)[0] + '.tex'
    header = '% Auto-generated by docs/tools/highlight.py - do not edit\n'
    header += '\\begin{codebox}\n'
    footer = '\\end{codebox}\n'

    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(colored_code)
        f.write('\n')
        f.write(footer)

    print(f'Wrote {tex_path}')


def scan_and_process(docs_root: str):
    mtimes = {}

    # initial pass
    ql_files = []
    for root, _, files in os.walk(docs_root):
        for name in files:
            if name.endswith('.ql'):
                ql_files.append(os.path.join(root, name))

    for p in ql_files:
        try:
            m = os.path.getmtime(p)
        except OSError:
            m = 0
        mtimes[p] = m
        process_file(p)

    print('Initial highlighting done. Watching for changes...')

    try:
        while True:
            time.sleep(1)
            # collect current files
            current = {}
            for root, _, files in os.walk(docs_root):
                for name in files:
                    if name.endswith('.ql'):
                        p = os.path.join(root, name)
                        try:
                            current[p] = os.path.getmtime(p)
                        except OSError:
                            current[p] = 0

            # check for new or modified
            for p, m in current.items():
                if p not in mtimes or mtimes[p] != m:
                    print('Change detected:', p)
                    try:
                        process_file(p)
                    except Exception as e:
                        print('Error while processing', p, e)
                    mtimes[p] = m

            # check for deleted
            removed = set(mtimes.keys()) - set(current.keys())
            for p in removed:
                print('File removed:', p)
                texp = os.path.splitext(p)[0] + '.tex'
                try:
                    os.remove(texp)
                    print('Removed', texp)
                except OSError:
                    pass
                del mtimes[p]

    except KeyboardInterrupt:
        print('Watcher stopped by user')


if __name__ == '__main__':
    docs_root = os.path.abspath(os.path.join(THIS_DIR, '..'))
    print('Docs root:', docs_root)
    scan_and_process(docs_root)
