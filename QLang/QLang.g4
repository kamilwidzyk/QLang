grammar QLang;

// --- REGUŁY PARSERA ---

// Cały program jest plikiem składającym się z instukcji
// nowe linie nie mają znaczenia
// pusty plik też jest poprawnym programem
program : statement* EOF ;

// Każda z instrukcji może być
// - deklaracją zmiennej
// - bramką kwantową
// - pomiarem
// - instrukcją warunkową
// - pętlą
// - definicją funkcji
// - wywołaniem funkcji
// - wyświetleniem informacji
// - wczytaniem informacji
// - przypisaniem
// Każda z instrukcji kończy się średnikiem
statement
    : varDeclaration ';'
    | quantumGate ';'
    | measurement ';'
    | ifStatement
    | loopStatement
    | functionDefinition
    | functionCall ';'
    | printStatement ';'
    | inputStatement ';'
    | assignment ';'
    ;

// Deklaracje zmiennych
// typ może być 'state' lub 'obs' 
// deklaracja może być wielokrotna lub rejestr lub z przypisaniem
varDeclaration
    : 'state' (idList | idWithArray | stateSuperposed)
    | 'obs' (idList | idWithArray | idAssign)
    ;

// lista nazw po przecinku
idList : IDENTIFIER (',' IDENTIFIER)* ;
// nazwa i nawiasy kwadratowe z indeksem/rozmiarem
idWithArray : IDENTIFIER '[' (NUMBER | expression) ']' ;
// przypisanie - nazwa = wartość
idAssign : IDENTIFIER '=' (NUMBER | BINARY | HEX) ;
// inicjalizacja stanu w superpozycji
stateSuperposed : IDENTIFIER '=' 'superposed' ;

// Bramki kwantowe
// - Bramka jednoqubitowa: <bramka> <cel>
// - Bramka dwukubitowa: <bramka> <control> -> <cel>
// - Operacja swap: swap <cel1> <cel2>
quantumGate
    : SINGLE_QUBIT_GATE target
    | TWO_QUBIT_GATE control '->' target
    | 'swap' target target
    ;

// Wszystkie możliwe bramki jedno i dwu qubitowe
SINGLE_QUBIT_GATE : 'H' | 'superpose' | 'S' | 'X' | 'Y' | 'Z' | 'not' | 'phase_not' ;
TWO_QUBIT_GATE : 'CNOT' | 'entangle' | 'CZ' | 'entangle_phase' ;

// qubit kontrolny i docelowy może być jednym qubitem lub jednym z rejestru
target : IDENTIFIER ('[' expression ']')? ;
control : IDENTIFIER ('[' expression ']')? ;

// Pomiar
measurement
    : target '=' ('measure' | 'measureX') target
    ;

// Instrukcje sterujące
ifStatement
    : 'if' '(' expression ')' '{' statement* '}' ('else' '{' statement* '}')?
    ;

loopStatement
    : 'for' IDENTIFIER 'from' expression 'to' expression ('step' expression)? '{' statement* '}'
    | 'while' '(' expression ')' '{' statement* '}'
    ;

// Funkcje
functionDefinition
    : 'function' IDENTIFIER '(' idList? ')' '{' statement* ('return' expression ';')? '}'
    ;

functionCall
    : IDENTIFIER '(' (expression (',' expression)*)? ')'
    ;

// Operacje na danych (Obserwacje)
assignment : target '=' expression ;

expression
    : '(' expression ')'
    | '!' expression
    | expression ('**') expression
    | expression ('*' | '/' | '%') expression
    | expression ('+' | '-') expression
    | expression ('<' | '>' | '<=' | '>=') expression
    | expression ('==' | '!=') expression
    | expression ('&&' | '||') expression
    | terminalValue
    | functionCall
    ;

terminalValue
    : NUMBER
    | BINARY
    | HEX
    | 'T' | 'F'
    | IDENTIFIER ('[' expression ']')?
    ;

// Wyjście/Wejście
printStatement
    : ('print' | 'println' | 'debug') '(' (expression | STRING)? (',' ('BIN' | 'HEX'))? ')'
    ;

inputStatement
    : 'input' '(' target (',' ('BIN' | 'HEX'))? ')'
    ;

// --- REGUŁY LEKSERA ---

// Słowa kluczowe (wybrane)
STATE : 'state' ;
OBS   : 'obs' ;
IF    : 'if' ;
ELSE  : 'else' ;

// Typy danych i identyfikatory
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER     : [0-9]+ ;
BINARY     : '0b' [01]+ ;
HEX        : '0x' [0-9a-fA-F]+ ;
STRING     : '"' (~["\r\n])* '"' ;

// --- CHANNELS / SKIPS ---
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;
WS            : [ \t\r\n]+    -> skip ;