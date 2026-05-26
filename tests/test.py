import subprocess
import os
import importlib.util
import sys
import re

import colorama

SYNTAX_ERRORS = "[--- TEST ---](D) SYNTAX_ERRORS=1"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def path_from_root(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return os.path.join(parent_dir, rel_path)


def strip_ansi_codes(line: str) -> str:
    return re.sub(r'\x1b\[[0-9;]*m', '', line)


def prepare_test_run():
    """ Runs preparation for running in test mode"""

    bat_file = "antlr\\prepare_test.bat"

    bat_path = path_from_root(bat_file)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    # Run it as if executed from its own directory
    subprocess.run(
        [bat_path],
        cwd=parent_dir,
        shell=True
    )

def run_in_test_mode(ql_path: str):
    """ Runs the interpreter in test mode with a given .ql file, logs are in logs dir"""

    bat_file = "antlr\\run_test.bat"
    argument = ql_path

    bat_path = path_from_root(bat_file)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    # Run it as if executed from its own directory
    subprocess.run(
        [bat_path, argument],
        cwd=parent_dir,
        shell=True
    )

def extract_test_lines_from_log():
    int_log_path = path_from_root("logs\\int_out.log")
    log_text = open(int_log_path, "r", encoding="utf-8").read()
    lines = log_text.splitlines()
    cleaned_lines = [strip_ansi_codes(line) for line in lines]
    test_lines = [line for line in cleaned_lines if line.startswith("[--- TEST ---](D) ")]
    return test_lines

ERROR_LINE_PREFIX = "[--- TEST ---](D) ERROR_"

def extract_error_entries_from_log() -> list:
    """Parse structured runtime error data from the interpreter test log."""
    entries = {}
    for line in extract_test_lines_from_log():
        if not line.startswith(ERROR_LINE_PREFIX):
            continue

        payload = line[len("[--- TEST ---](D) "):]
        if "=" not in payload:
            continue

        key, value = payload.split("=", 1)
        if "[" not in key or not key.endswith("]"):
            continue

        field, index_text = key.split("[", 1)
        index_text = index_text[:-1]
        try:
            index = int(index_text)
        except ValueError:
            continue

        entries.setdefault(index, {})[field] = value

    return [entries[i] for i in sorted(entries)]


def get_error_entry(line_start: int, line_end: int, col_start: int, col_end: int, code: str) -> dict | None:
    """Return the runtime error entry dict matching the expected coordinates and code."""
    for entry in extract_error_entries_from_log():
        if (entry.get("ERROR_LINE_START") == str(line_start) and
            entry.get("ERROR_LINE_END") == str(line_end) and
            entry.get("ERROR_COL_START") == str(col_start) and
            entry.get("ERROR_COL_END") == str(col_end) and
            entry.get("ERROR_CODE") == code):
            return entry
    return None


def find_error_entry(line_start: int, line_end: int, col_start: int, col_end: int, code: str) -> bool:
    """Return True if the test log contains a runtime error entry matching the expected coordinates and code."""
    return get_error_entry(line_start, line_end, col_start, col_end, code) is not None


def format_error_entry(entry: dict, status: str | None = None) -> str:
    """Format a parsed runtime error entry for printing."""
    parts = [
        f"ERROR_ENTRY: line {entry.get('ERROR_LINE_START')}..{entry.get('ERROR_LINE_END')}",
        f"col {entry.get('ERROR_COL_START')}..{entry.get('ERROR_COL_END')}",
        f"code={entry.get('ERROR_CODE')}"
    ]
    message = entry.get('ERROR_MESSAGE')
    if message:
        parts.append(f"message={message}")

    line = ", ".join(parts)
    if status:
        line = f"{line} [{status}]"
    return line


def highlight_entry_line(line: str, ok: bool) -> str:
    if ok:
        return colorama.Fore.GREEN + line + colorama.Style.RESET_ALL
    return colorama.Fore.RED + line + colorama.Style.RESET_ALL


def compare_error_entry(entry: dict, expected: dict) -> list:
    """Compare an actual error entry against expected fields and return mismatch strings."""
    mismatches = []
    for field, expected_value in expected.items():
        actual_value = entry.get(field)
        expected_str = str(expected_value)
        if actual_value != expected_str:
            field_name = field.replace("ERROR_", "").lower()
            mismatches.append(f"{field_name}: {actual_value} (expected: {expected_str})")
    return mismatches


def extract_error_box_from_log() -> str:
    """Extract the formatted error box from the raw interpreter log for visual confirmation."""
    int_log_path = path_from_root("logs\\int_out.log")
    raw_lines = open(int_log_path, "r", encoding="utf-8").read().splitlines()

    start_index = None
    for index, line in enumerate(raw_lines):
        stripped = strip_ansi_codes(line)
        if stripped.startswith("[--- TEST ---](D) ERROR_CODE"):
            start_index = index + 1
            break

    if start_index is None:
        return ""

    # Skip any blank lines after the ERROR_CODE entry.
    while start_index < len(raw_lines) and strip_ansi_codes(raw_lines[start_index]).strip() == "":
        start_index += 1

    if start_index >= len(raw_lines):
        return ""

    box_lines = []
    for index in range(start_index, len(raw_lines)):
        box_lines.append(raw_lines[index])
        if "╯" in strip_ansi_codes(raw_lines[index]):
            break

    if not box_lines:
        return ""

    return "\n".join(box_lines)


def print_error_entry(line_start: int, line_end: int, col_start: int, col_end: int, code: str) -> bool:
    """Print a matching runtime error entry if found and return True, otherwise return False."""
    expected = {
        "ERROR_LINE_START": str(line_start),
        "ERROR_LINE_END": str(line_end),
        "ERROR_COL_START": str(col_start),
        "ERROR_COL_END": str(col_end),
        "ERROR_CODE": code,
    }

    entry = get_error_entry(line_start, line_end, col_start, col_end, code)
    if entry is not None:
        print(highlight_entry_line(format_error_entry(entry, "OK"), True))
        error_box = extract_error_box_from_log()
        if error_box:
            for line in error_box.splitlines():
                if strip_ansi_codes(line).strip():
                    print(line)
        return True

    expected_line = format_error_entry(expected, "FAIL")
    print(highlight_entry_line(expected_line, False))
    print(f"No exact error match found for expected entry.")

    entries = extract_error_entries_from_log()
    if not entries:
        print("No error entries found at all.")
        return False

    for index, entry in enumerate(entries):
        actual_line = format_error_entry(entry)
        print(f"Actual error entry #{index}: {actual_line}")
        mismatches = compare_error_entry(entry, expected)
        if mismatches:
            print("  " + "; ".join(mismatches))

    error_box = extract_error_box_from_log()
    if error_box:
        print("Formatted error box from log:")
        for line in error_box.splitlines():
            if strip_ansi_codes(line).strip():
                print(line)

    return False


def read_place_files_as_dict() -> dict:
    result = {}
    directory = path_from_root("logs")

    for filename in os.listdir(directory):
        if filename.startswith("Place"):
            file_path = os.path.join(directory, filename)

            if os.path.isfile(file_path):
                # Extract key:
                # Remove "Place"
                remainder = filename[len("Place"):]

                # Remove leading space (if present)
                remainder = remainder.lstrip()

                # Take text up to first space
                key = remainder.split(" ", 1)[0]

                # Optional: remove file extension from key
                key = os.path.splitext(key)[0]

                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                result[key] = content

    return result

def run_tests_in_directory(root_dir, test_name=None):
    results = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]

        for filename in filenames:
            if filename.endswith(".py"):
                print(f"{colorama.Fore.BLUE}Running tests in {filename}...{colorama.Style.RESET_ALL}")
                file_path = os.path.join(dirpath, filename)

                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)

                try:
                    spec.loader.exec_module(module)
                except Exception:
                    continue

                for attr_name in dir(module):
                    #print(f"  Checking {attr_name}...")
                    if attr_name.startswith("test_"):
                        if test_name and attr_name != test_name:
                            continue
                        func = getattr(module, attr_name)
                        print(f"{colorama.Fore.GREEN}     >>>>> Running {attr_name} <<<<<{colorama.Style.RESET_ALL}")

                        if callable(func):
                            test_name_short = attr_name[len("test_"):] if attr_name.startswith("test_") else attr_name

                            # 👇 relative path instead of absolute
                            rel_path = os.path.relpath(file_path, os.getcwd())
                            key = f"{rel_path}:{test_name_short}"

                            try:
                                result = func()
                                results[key] = bool(result)
                            except Exception:
                                results[key] = False
                        
                        print(f"{colorama.Fore.YELLOW}     >>>>> Finished {attr_name} <<<<<{colorama.Style.RESET_ALL}")

    return results

if __name__ == "__main__":
    # Default: run all tests
    prepare_test_run()
    subdir = path_from_root("tests")
    test_name = None

    # If argument provided → run only that subdirectory
    if len(sys.argv) > 1:
        subdir = path_from_root(f"tests/{sys.argv[1]}")
    # If second argument provided → run only that test function
    if len(sys.argv) > 2:
        test_name = "test_" +sys.argv[2]

    failed_passed = run_tests_in_directory(subdir, test_name)

    print(f"{colorama.Fore.BLACK}\n\n{colorama.Back.GREEN}          #####>-- Test results: --<#####          {colorama.Style.RESET_ALL}\n")
    passed_count = sum(1 for result in failed_passed.values() if result)
    total_count = len(failed_passed)

    for key, value in failed_passed.items():
        print(f"  {f'{colorama.Fore.GREEN}PASSED{colorama.Style.RESET_ALL}' if value else f'{colorama.Fore.RED}FAILED{colorama.Style.RESET_ALL}'} | {key}")

    print(f"\n{colorama.Fore.WHITE}{colorama.Style.BRIGHT}Summary: {passed_count}/{total_count} tests passed.\n{colorama.Style.RESET_ALL}")
