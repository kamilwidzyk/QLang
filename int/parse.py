import sys
import json
from antlr4 import *
from QLang.QLangLexer import QLangLexer
from QLang.QLangParser import QLangParser


def tree_to_dict(node, parser):
    """Konwertuje drzewo ANTLR na słownik Pythona (serializowalny do JSON)"""

    # TERMINAL
    if isinstance(node, TerminalNode):
        token = node.symbol
        return {
            "type": "Terminal",
            "text": node.getText(),
            "line": token.line,
            "column": token.column
        }

    # NODE PARSERA
    res = {
        "type": type(node).__name__
    }

    if hasattr(node, 'getRuleIndex'):
        res["rule"] = parser.ruleNames[node.getRuleIndex()]

    # pozycja w kodzie
    if hasattr(node, "start") and node.start:
        res["line"] = node.start.line
        res["column"] = node.start.column

    if hasattr(node, "stop") and node.stop:
        res["endLine"] = node.stop.line
        res["endColumn"] = node.stop.column

    # dzieci
    if node.children:
        res["children"] = [tree_to_dict(c, parser) for c in node.children]

    return res


def main():
    input_filename = sys.argv[1]

    input_name = ("".join(input_filename.split(".")[:-1])).split("\\")[-1]

    input_stream = FileStream(input_filename)

    lexer = QLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = QLangParser(stream)

    tree = parser.program()

    resultJSON = json.dumps(tree_to_dict(tree, parser), indent=2)

    with open(f"output/{input_name}.json", "w", encoding="utf-8") as resultFile:
        resultFile.write(resultJSON)


if __name__ == '__main__':
    main()