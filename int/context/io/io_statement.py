from typing import Any, TYPE_CHECKING

import colorama

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister
from ...num import Num

import random
from ...logger import log, DEBUG, IN_OUT

from ...expression import *
from ...variable import Variable
from ...function import Function
from ...text import Text
from ...state import State

from ...sim.data.consts import QuantumID, QuantumMeasurement, QuantumPrefix
from ...sim.data.event import QuantumEvent
from ...sim.data.gates import QuantumGate, QuantumGates
from ...sim.data.graph import EntaglementGraph
from ...sim.data.history import QuantumHistory
from ...sim.data.state import QuantumState

if TYPE_CHECKING:
    from place import Place

def handle_io_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # first child can be 'print', 'println' or 'input', 'debug'

    def convert_value(value):
        print("Converting value: ", value)
        result = None
        if isinstance(value, (Num, ObsRegister, Text)):
            result = value.get_value()
            if isinstance(result, bool):
                result = int(result)
        if isinstance(value, Expression):
            result = convert_value(value.get())
        if isinstance(value, Variable):
            result = convert_value(value.get())
        if isinstance(value, list):
            result = [convert_value(x) for x in value]
        if isinstance(value, (int, float, str)):
            result = value
        if isinstance(value, bool):
            result = 'T' if value else 'F'
        if isinstance(value, Obs):
            result = 'T' if value.get_value() else 'F'

        while hasattr(result, 'get_value'):
            result = result.get_value()

        print("Converted value: ", result)
        return result
    
    
    
    def handle_print(add_newline=False):
        nonlocal block

        # no expr -> print a newline if enabled
        if not block.expr():
            if add_newline:
                self.console.write("\n")
            return
        
        # Get all expressions
        exprs = []
        for i in range(len(block.expr())):
            exprs.append(self.handle_block(block.expr(i), block))

       
        # Print all args separated by space
        print_parts = []
        for expr in exprs:
            print_parts.append(str(convert_value(expr)))
        print_text = ' '.join(print_parts)

        # add a newline if the command was println
        if add_newline:
            self.console.write(print_text + "\n")
        else:
            self.console.write(print_text)

    def handle_input():
        nonlocal block
        # INPUT '(' ID ('[' expr ']')? (',' format)? (',' constraint)? ')'

        if self.console.test_mode:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos,
                error_type="RUNTIME ERROR",
                title="Input not supported in TEST MODE",
                msg="This program asks for input(), but TEST_MODE does not provide interactive console input.",
            )
            exit()
        
        # variable name(ID) is required
        var_name = block.ID().getText()

        # variable index is optional
        index = None
        if block.expr():
            index = self.handle_block(block.expr(), block)

        # format is optional(BIN, HEX)
        format = None
        if block.format_():
            format = self.handle_block(block.format_(), block)
        
        # constraint is optional(value range: min..max or range(min, max))
        constraint_min = None
        constraint_max = None
        if block.constraint():
            constraint_min, constraint_max = self.handle_block(block.constraint(), block)

        # check if variable exists
        if not self.scopes.exists(var_name):
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="You Error", 
                msg="No variable. You forgot to make it, input lost to the void."
            )
            exit()

        variable: Obs | ObsRegister | Num = self.scopes.get(var_name)

        # check if the variable is of correct type
        if variable.type not in ["Obs", "ObsRegister", "Num"]:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="Type Error", 
                msg="Not how this works. I need an observation(s)."
            )
            exit()

        # check if variable can be indexed
        if index is not None and variable.type == "Obs":
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="Index Error", 
                msg="You are looking too deep into something that can only be 0 or 1."
            )
            exit()
        

        # update to given constraint if possible
        if constraint_min is not None:
            min_val = constraint_min
        if constraint_max is not None:
            max_val = constraint_max

        if variable.type == "Num":
            max_val = float('inf') if constraint_max is None else max_val
            min_val = float('-inf') if constraint_min is None else min_val
        else:
            max_val = variable.data.max_val() if constraint_max is None else max_val
            min_val = 0 if constraint_min is None else min_val
        value = None

        # Try forever to get a value from the user
        while True:
            # read a line from the console window(not the terminal)
            log(IN_OUT, DEBUG, f"{self.name}: Waiting for console input...")
            console_in = self.console.read("")
            log(IN_OUT, DEBUG, f"{self.name}: Console input: {console_in}")

            if console_in is None:
                continue
            
            # check formatting
            if format is not None:
                if format == "BIN" and console_in.startswith("0b"):
                    try:
                        value = int(console_in, 2)
                        if value >= min_val and value <= max_val:
                            break # valid value received -> end of loop
                    except:
                        pass # not a number
                elif format == "HEX" and console_in.startswith("0x"):
                    try:
                        value = int(console_in, 16)
                        if value >= min_val and value <= max_val:
                            break # valid value received -> end of loop
                    except:
                        pass # not a number
            else:
                try:
                    if variable.type == "Num":
                        value = float(console_in)
                    else:
                        value = int(console_in)

                    if value >= min_val and value <= max_val:
                        break # valid value received -> end of loop
                except:
                    pass # not a number
            
            # user input is invalid, show a message what is expected on the input
            format_str = {None: "decimal", "BIN": "binary", "HEX": "hexadecimal"}[format]
            invalid = [
                "That's not gonna work.", "What even is that input.", "Try again, but correctly.",
                "I can't work with that.", "Rejected.", "Input denied.", "Nice try, but no.",
                "Be serious.", "No idea what that is.", "Nah.", "Hard no.", "Rejected in 0ms.",
                "Absolutely not.", "Fail.", "Not today.", "Not a chance.", "Try harder.",
                "LOL, no.", "Wrong.", "No.", "Nope.", "That's a no.", "Do better.",
                "Denied.", "I can't let that slide."
            ]

            self.console.write(f"[{random.sample(invalid, 1)[0]} I need a number in range {min_val}-{max_val} in {format_str} format] ")

        # set value to the variable and update variable in the scope
        value_type = TYPE_FLOAT if variable.type == "Num" else TYPE_INT
        variable.set(Expression(value_type, value))
        self.scopes.set(var_name, variable)

    def handle_debug():
        nonlocal block
        
        # DEBUG '(' expr ')'

        is_reference = False
        value = None

        if block.expr():
            value = self.handle_block(block.expr(0), block)

        if block.reference():
            value = self.handle_block(block.reference(), block)
            is_reference = True

        if value is None:
            self.console.write("DEBUG None\n")
            return

        debug_lines = []

        def value_to_lines(val):
            if isinstance(val, int):
                return [
                    "Type: int", "Value: " + str(val)
                ]
            if isinstance(val, float):
                return [
                    "Type: float", "Value: " + str(val)
                ]
            if isinstance(val, str):
                return [
                    "Type: str", f"Length: {len(val)}", "Value: " + val
                ]
            if isinstance(val, list):
                lines = ["Type: list", f"Length: {len(val)}", "Value: ["]
                for item in val:
                    item_lines = value_to_lines(item)
                    lines.extend(["\t" + line for line in item_lines])
                lines.append("]")
                return lines
            if isinstance(val, Num):
                return [
                    "Type: Num", f"Value: {val.get()} (is_float: {val.is_float})"
                ]
            if isinstance(val, Obs):
                return [
                    "Type: Obs", f"Value: {val.get()}"
                ]
            if isinstance(val, ObsRegister):
                return [
                    "Type: ObsRegister", f"Size: {val.size}", f"Value: {val.get()}"
                ]
            if isinstance(val, Text):
                return [
                    "Type: Text", f"Length: {len(val.get())}", f"Value: {val.get()}"
                ]
            if isinstance(val, State):
                state_lines = [
                    "Type: State", f"UID: {val.uid}"
                ]
        
                # Quantum state -> some additional info
                # get_history() -> QuantumHistory
                # get_stabilizers() -> list[str]
                # get_state_info() -> QuantumState
                history: QuantumHistory = val.get_history()
                stabilizers: list[str] = val.get_stabilizers()
                state: QuantumState = val.get_state_info()

                state_lines.append("History:")
                for event in history.as_list():
                    state_lines.append(f"\t{str(event)}")

                state_lines.append("Stabilizers:")
                for stab in stabilizers:
                    state_lines.append(f"\t{str(stab)}")

                state_lines.append("State:")
                state_lines.append(f"\tX: {state.x}")
                state_lines.append(f"\tZ: {state.z}")
                state_lines.append(f"\tPhase: {state.phase}")


                return state_lines
            

            return [
                "Unknown type: " + str(type(val)), "Value: " + str(val)
            ]


        if is_reference:
            # this should be a variable or function
            if isinstance(value, Variable):
                # information to display: name, type, dimensions, data, is_list, index
                # for data use a separate print handler
                debug_lines.append("===== Variable Reference =====")
                debug_lines.append(f"Name:       {value.name}")
                debug_lines.append(f"Type:       {value.type}")
                debug_lines.append(f"Dimensions: {value.dimensions}")
                debug_lines.append(f"Is List:    {value.is_list}")
                debug_lines.append(f"Index:      {value.index}")
                if value.data is not None:
                    debug_lines.append("Data: ")
                    value_lines = value_to_lines(value.data)
                    debug_lines.extend(["\t" + x for x in value_lines])

                        



            elif isinstance(value, Function):
                # information to display: name, params(list + count), body(likely not), pos, type
                debug_lines.append("===== Function Reference =====")
                debug_lines.append(f"Name:            {value.name}")
                debug_lines.append(f"Parameter Count: {len(value.params)}")
                for i, param in enumerate(value.params):
                    debug_lines.append(f"\tParam {i}: {param.name}")
                    debug_lines.append(f"\t\tType: {param.type}")
                    debug_lines.append(f"\t\tSize: {param.size}")
                    if param.initial_value is not None:
                        debug_lines.append(f"\t\tInitial Value: ")
                        param_value_lines = value_to_lines(param.initial_value)
                        debug_lines.extend(["\t\t\t" + x for x in param_value_lines])
                debug_lines.append(f"Body Length:     {len(value.body)}")
                debug_lines.append(f"Position:        {value.pos}")
            elif isinstance(value, Variable) and isinstance(value.data, State):
                # State variable reference - query the quantum server
                debug_lines.append("===== Quantum State Reference =====")
                debug_lines.append(f"Variable Name:   {value.name}")
                debug_lines.append(f"Type:            {value.type}")
                debug_lines.append(f"State UID:       {value.data.uid}")
                
                try:
                    # Get and display quantum history
                    history = value.data.get_history()
                    debug_lines.append("Quantum History:")
                    if history:
                        if hasattr(history, '__iter__') and not isinstance(history, str):
                            for i, entry in enumerate(history):
                                debug_lines.append(f"\t[{i}] {entry}")
                        else:
                            debug_lines.append(f"\t{history}")
                    else:
                        debug_lines.append("\t(empty)")
                except Exception as e:
                    debug_lines.append(f"Quantum History: ERROR - {str(e)}")
                
                try:
                    # Get and display stabilizers
                    stabilizers = value.data.get_stabilizers()
                    debug_lines.append("Stabilizers:")
                    if stabilizers:
                        if hasattr(stabilizers, '__iter__') and not isinstance(stabilizers, str):
                            for i, stab in enumerate(stabilizers):
                                debug_lines.append(f"\t[{i}] {stab}")
                        else:
                            debug_lines.append(f"\t{stabilizers}")
                    else:
                        debug_lines.append("\t(empty)")
                except Exception as e:
                    debug_lines.append(f"Stabilizers: ERROR - {str(e)}")
                
                try:
                    # Get and display state information
                    state_info = value.data.get_state_info()
                    debug_lines.append("State Information:")
                    if state_info:
                        if hasattr(state_info, '__dict__'):
                            for key, val in state_info.__dict__.items():
                                debug_lines.append(f"\t{key}: {val}")
                        else:
                            debug_lines.append(f"\t{state_info}")
                    else:
                        debug_lines.append("\t(empty)")
                except Exception as e:
                    debug_lines.append(f"State Information: ERROR - {str(e)}")
            else:
                self.console.write(f"DEBUG Unsupported reference type: {type(value)}\n")
                return
        elif isinstance(value, Expression):
            debug_lines.append("===== Expression =====")
            debug_lines.append(f"Type:  {value.type}")
            debug_lines.append(f"Shape: {value.shape}")
            if value.value is not None:
                if isinstance(value.value, State):
                    debug_lines.append("Value: ")
                    debug_lines.append(f"\tState UID: {value.value.uid}")
                    try:
                        history = value.value.get_history()
                        debug_lines.append("\tQuantum History:")
                        if history:
                            if hasattr(history, '__iter__') and not isinstance(history, str):
                                for i, entry in enumerate(history):
                                    debug_lines.append(f"\t\t[{i}] {entry}")
                            else:
                                debug_lines.append(f"\t\t{history}")
                    except Exception as e:
                        debug_lines.append(f"\tQuantum History: ERROR - {str(e)}")
                    try:
                        stabilizers = value.value.get_stabilizers()
                        debug_lines.append("\tStabilizers:")
                        if stabilizers:
                            if hasattr(stabilizers, '__iter__') and not isinstance(stabilizers, str):
                                for i, stab in enumerate(stabilizers):
                                    debug_lines.append(f"\t\t[{i}] {stab}")
                            else:
                                debug_lines.append(f"\t\t{stabilizers}")
                    except Exception as e:
                        debug_lines.append(f"\tStabilizers: ERROR - {str(e)}")
                else:
                    debug_lines.append("Value: ")
                    debug_lines.extend(["\t" + x for x in value_to_lines(value.value)])
            if value.variable is not None:
                debug_lines.append("Variable: ")
                debug_lines.extend(["\t" + x for x in value_to_lines(value.variable.data)])
        else:
            debug_lines.append("===== Value =====")
            debug_lines.extend(value_to_lines(value))



        debug_lines = [f"{colorama.Fore.RED}DEBUG{colorama.Style.RESET_ALL} {str(line)}" for line in debug_lines]
        self.console.write("\n".join(debug_lines) + "\n")
        

        return


        if isinstance(value, Variable):
            debug_info = f"DEBUG {value.name}: type={value.type}, dimensions={value.dimensions}"
            if value.data is not None:
                debug_info += f", data={value.data}"
            self.console.write(debug_info + "\n")
            return

        return        

        # TODO: make the debug output more structured, not just everything in one line
        # make it multiline and more readable

        def format_variable_value(var):
            if isinstance(var, Num):
                return f"Num(value={var.value}, is_float={var.is_float})"
            elif isinstance(var, Obs):
                return f"Obs(value={var.get()})"
            elif isinstance(var, ObsRegister):
                return f"ObsRegister(value={var.get()})"
            elif isinstance(var, list):
                return f"[{', '.join(format_variable_value(x) for x in var)}]"
            else:
                return str(var)
        
        if isinstance(variable, Variable):
            debug_info += f"Variable(type={variable.type}, dimensions={variable.dimensions}"
            if len(index) == 0:
                if variable.data is None:
                    debug_info += ", data=None"
                else:
                    debug_info += f", data={format_variable_value(variable.data)}"
                debug_info += ")"
            else:
                try:
                    if variable.is_list:
                        indexed_value = variable.data
                        for idx in index if isinstance(index, list) else [index]:
                            indexed_value = indexed_value[idx]
                        debug_info += f", indexed_value={format_variable_value(indexed_value)})"
                    else:
                        debug_info += ", not a list, cannot index)"
                except Exception as e:
                    debug_info += f", error accessing index: {e})"
        elif isinstance(variable, Function):
            debug_info += f"Function(param_count={len(variable.params)}"
            
            for p in variable.params or []:
                debug_info += f", param_{p.name}={{name: {p.name}, type: {p.type}, size: {p.size}, initial_value: {format_variable_value(p.initial_value)}}}"
            
            debug_info += f", body_length={len(variable.body)}"
            # position in code
            debug_info += f", pos={variable.pos})"


            
        else:
            debug_info += f"Other(type={type(variable)}, value={variable})"
        
        self.console.write(debug_info + "\n")



    stmt_type = block.getChild(0).getText()

    if stmt_type == "print":
        handle_print()
    elif stmt_type == "println":
        handle_print(add_newline=True)
    elif stmt_type == "debug":
        handle_debug()

    elif stmt_type == "input":
        handle_input()
        
