from tests.test import *

def test_errors_spellcheck_var() -> bool:
    run_in_test_mode("tests\\errors\\spellcheck\\spellcheck_var.ql")

    expected_entries = [
        "CFV-3"
    ]
    
    entries = extract_error_entries_from_log()
    codes = [entry["ERROR_CODE"] for entry in entries]
    
    # Verify that the suggestion is actually in the printed output
    log_content = ""
    try:
        with open("logs/int_out.log", "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        print(f"ERROR reading log: {e}")
        return False
        
    if "Did you mean" not in log_content or "very_long_variable_name" not in log_content:
        print("ERROR_ENTRY: Spellcheck suggestion not found in log output")
        return False

    for entry in expected_entries:
        if entry not in codes:
            print("ERROR_ENTRY: {} [MISSING]".format(entry))
            return False
        else:
            print("ERROR_ENTRY: {} [OK]".format(entry))
            codes.remove(entry)

    if len(codes) > 0:
        return False
    
    return True

def test_errors_spellcheck_func() -> bool:
    run_in_test_mode("tests\\errors\\spellcheck\\spellcheck_func.ql")

    expected_entries = [
        "NFTC-1"
    ]
    
    entries = extract_error_entries_from_log()
    codes = [entry["ERROR_CODE"] for entry in entries]
    
    log_content = ""
    try:
        with open("logs/int_out.log", "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        print(f"ERROR reading log: {e}")
        return False
        
    if "Did you mean" not in log_content or "my_awesome_function" not in log_content:
        print("ERROR_ENTRY: Spellcheck suggestion not found in log output for function")
        return False

    for entry in expected_entries:
        if entry not in codes:
            print("ERROR_ENTRY: {} [MISSING]".format(entry))
            return False
        else:
            print("ERROR_ENTRY: {} [OK]".format(entry))
            codes.remove(entry)

    if len(codes) > 0:
        return False
    
    return True

def test_errors_spellcheck_size() -> bool:
    run_in_test_mode("tests\\errors\\spellcheck\\spellcheck_size.ql")
    entries = extract_error_entries_from_log()
    codes = [entry["ERROR_CODE"] for entry in entries]
    
    try:
        with open("logs/int_out.log", "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        print(f"ERROR reading log: {e}")
        return False
        
    if "Did you mean" not in log_content or "my_array" not in log_content:
        print("ERROR_ENTRY: Spellcheck suggestion not found in log output for size operator")
        return False

    if "CFV-1" not in codes:
        print("ERROR_ENTRY: CFV-1 [MISSING]")
        return False
    
    print("ERROR_ENTRY: CFV-1 [OK]")
    return True

def test_errors_spellcheck_parent() -> bool:
    run_in_test_mode("tests\\errors\\spellcheck\\spellcheck_parent.ql")
    entries = extract_error_entries_from_log()
    codes = [entry["ERROR_CODE"] for entry in entries]
    
    try:
        with open("logs/int_out.log", "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        print(f"ERROR reading log: {e}")
        return False
        
    if "Did you mean" not in log_content or "parent_var" not in log_content:
        print("ERROR_ENTRY: Spellcheck suggestion not found in log output for parent scope")
        return False

    if "CFV-6" not in codes:
        print("ERROR_ENTRY: CFV-6 [MISSING]")
        return False
    
    print("ERROR_ENTRY: CFV-6 [OK]")
    return True

def test_errors_spellcheck_no_match() -> bool:
    run_in_test_mode("tests\\errors\\spellcheck\\spellcheck_no_match.ql")
    entries = extract_error_entries_from_log()
    codes = [entry["ERROR_CODE"] for entry in entries]
    
    try:
        with open("logs/int_out.log", "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        print(f"ERROR reading log: {e}")
        return False
        
    if "Did you mean" in log_content:
        print("ERROR_ENTRY: Spellcheck suggestion unexpectedly found in log output for no match")
        return False

    if "CFV-3" not in codes:
        print("ERROR_ENTRY: CFV-3 [MISSING]")
        return False
    
    print("ERROR_ENTRY: CFV-3 [OK]")
    return True

