from tests.test import *

def test_errors_import_source_file_not_found() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\import_source\\file_not_found\\file_not_found.ql")

    expected_entries = [
        "FNF-1"
    ]
    
    entries = extract_error_entries_from_log()
    
    # Just check the error codes
    codes = [entry["ERROR_CODE"] for entry in entries]
    
    for entry in expected_entries:
        if entry not in codes:
            print("ERROR_ENTRY: {} [MISSING]".format(entry))
            return False
        else:
            print("ERROR_ENTRY: {} [OK]".format(entry))
            codes.remove(entry)

    for entry in codes:
        print("ERROR_ENTRY: {} [UNEXPECTED]".format(entry))

    if len(codes) > 0:
        return False
    
    return True
