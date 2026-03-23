import sys
import json
from typing import Any, Tuple

from .logger import log, INIT, INFO, FATAL, SUCCESS

"""
This file contains functions for loading input files into memory
"""

def load_json(path: str) -> Any:
    """
    Loads and parses the JSON tree, then returns it

    Args:
        path (str): Path to JSON file

    Returns:
        Any: Parsed JSON structure
    """

    log(INIT, INFO, "Loading JSON tree...", end=False)
    try:
        json_content = open(path).read()
        tree = json.loads(json_content)
    except FileNotFoundError:
        log(INIT, FATAL, "JSON input file not found")
        exit()
    except json.JSONDecodeError:
        log(INIT, FATAL, "JSON input file: can't decode")

    log(INIT, SUCCESS, "OK", only_msg=True)
    return tree


def load_script(path: str) -> str:
    """
    Loads script file and returns it

    Args:
        path (str): Path to QLang file

    Returns:
        str: QLang file content
    """
    log(INIT, INFO, "Loading QLang script...", end=False)
    try:
        script = open(path).read()
    except FileNotFoundError:
        log(INIT, FATAL, "QLang script file not found")
        exit()
    
    log(INIT, SUCCESS, "OK", only_msg=True)
    return script

def load_input_files() -> Tuple[Any, str]:
    """
    Loads both JSON and QLang input files

    Returns:
        Tuple[Any, str]: Parsed JSON structure + QLang file content
    """
    arg_len = len(sys.argv)
    if(arg_len != 3):
        log(INIT, FATAL, "Required arguments missing!")
        log(INIT, FATAL, "Args: <JSON tree path> <QLang script path>")
        exit()
    
    tree = load_json(sys.argv[1])
    script = load_script(sys.argv[2])

    return tree, script