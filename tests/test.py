import subprocess
import os
import importlib.util
import sys

import colorama

SYNTAX_ERRORS = "[--- TEST ---](D) SYNTAX_ERRORS=1"

def path_from_root(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return os.path.join(parent_dir, rel_path)

def prepare_test_run():
    """ Runs preparation for running in test mode"""

    bat_file = "prepare_test.bat"

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

    bat_file = "run_test.bat"
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
    test_lines = [line for line in lines if line.startswith("[--- TEST ---](D) ")]
    return test_lines

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

def run_tests_in_directory(root_dir):
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
                        func = getattr(module, attr_name)
                        print(f"{colorama.Fore.GREEN}     >>>>> Running {attr_name} <<<<<{colorama.Style.RESET_ALL}")

                        if callable(func):
                            test_name = attr_name[len("test_"):]

                            # 👇 relative path instead of absolute
                            rel_path = os.path.relpath(file_path, os.getcwd())
                            key = f"{rel_path}:{test_name}"

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
    subdir = "tests"

    # If argument provided → run only that subdirectory
    if len(sys.argv) > 1:
        subdir = path_from_root(f"tests/{sys.argv[1]}")
    else:
        subdir = path_from_root("tests")

    failed_passed = run_tests_in_directory(subdir)

    print(f"{colorama.Fore.BLACK}\n\n{colorama.Back.GREEN}          #####>-- Test results: --<#####          {colorama.Style.RESET_ALL}\n")
    passed_count = sum(1 for result in failed_passed.values() if result)
    total_count = len(failed_passed)

    for key, value in failed_passed.items():
        print(f"  {f'{colorama.Fore.GREEN}PASSED{colorama.Style.RESET_ALL}' if value else f'{colorama.Fore.RED}FAILED{colorama.Style.RESET_ALL}'} | {key}")

    print(f"\n{colorama.Fore.WHITE}{colorama.Style.BRIGHT}Summary: {passed_count}/{total_count} tests passed.\n{colorama.Style.RESET_ALL}")