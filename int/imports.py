import os
import re

from antlr4 import InputStream, CommonTokenStream

from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser

SOURCE_IMPORT_RE = re.compile(r'<<\s*"(?P<path>[^"]+)"\s*>>')
DIRECT_INPUT_RE = re.compile(r'<<\s*""(?P<path>[^"]+)""\s*>>')


def _resolve_import_path(path: str, base_dir: str | None) -> str:
    path = path.strip()
    if os.path.isabs(path):
        return os.path.normpath(path)

    cwd = os.getcwd()
    candidate_dirs = []
    if base_dir is not None:
        candidate_dirs.append(base_dir)
    candidate_dirs.append(cwd)

    for candidate_dir in candidate_dirs:
        candidate_path = os.path.normpath(os.path.join(candidate_dir, path))
        if os.path.exists(candidate_path):
            return candidate_path

    return os.path.normpath(os.path.join(candidate_dirs[0], path))


def _read_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as handle:
        return handle.read()


def _escape_for_ql_string(value: str) -> str:
    value = value.replace('\\', '/')
    return value.replace('"', '\\"')


def preprocess_text(text: str, base_dir: str | None) -> str:
    def handle_direct_input(match) -> str:
        path = _resolve_import_path(match.group('path'), base_dir)
        content = _read_text_file(path)
        return preprocess_text(content, os.path.dirname(path))

    def handle_source_import(match) -> str:
        path = _resolve_import_path(match.group('path'), base_dir)
        return f'__ql_import_source__("{_escape_for_ql_string(path)}");'

    text = DIRECT_INPUT_RE.sub(handle_direct_input, text)
    text = SOURCE_IMPORT_RE.sub(handle_source_import, text)
    return text


def parse_ql_text(text: str):
    input_stream = InputStream(text)
    lexer = QLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = QLangParser(token_stream)
    return parser.program()
