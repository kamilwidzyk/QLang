// Commonly used functions

// Returns a binary list formated to string. [0, 1, 0] -> 010
// 0 and 1 literals can be swapped for something else 
// that is specified with optional arguments
function binary_to_str(obs binary_list[?], text zero="0", text one="1"){
    text result;
    iterate binary_list as bit{
        result += (bit ? zero : one);
    }
    return result;
}