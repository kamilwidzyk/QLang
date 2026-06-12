from typing import Any, TYPE_CHECKING

import colorama

from ...num import Num
from ...obs import Obs

if TYPE_CHECKING:
    from place import Place

from ...consts import *
from ...variable import Variable
from ...function import Function
from ...expression import Expression
from ...text import Text
from ...state import State
from ...sim.data.history import QuantumHistory
from ...sim.data.state import QuantumState



def handle_debug(self: Place, block: Any):
    """
    Handles debug IO operation
    """
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