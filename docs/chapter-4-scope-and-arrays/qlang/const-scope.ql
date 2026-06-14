num global_val = 10;
num local_val = 20;

if (T) {
    // This shadows the outer 'local_val'.
    const num local_val = 50;
    
    // Making an existing outer variable constant from within a local scope.
    const global_val;
}
// The outer 'local_val' remains 20 and is NOT constant.
local_val = 21; // Valid

// global_val = 11; // Not valid, cannot reassign const variable
