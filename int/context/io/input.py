from typing import Any, TYPE_CHECKING

import random

from .common import convert_value

if TYPE_CHECKING:
    from place import Place

from ...exception.test_mode import TestModeException
from ...exception.cant_find_variable import CantFindVariableException
from ...exception.spellcheck import get_spellcheck_suggestion
from ...exception.direct_quantum_access import DirectQuantumAccessException
from ...exception.obs_not_indexed import ObsNotIndexedException
from ...script_errors import ScriptErrors
from ...expression import TYPE_STATE, TYPE_TEXT, TYPE_NUM, TYPE_INT, TYPE_FLOAT, Expression
from ...logger import log, IN_OUT, DEBUG


def handle_input(self: Place, block: Any, parent: Any, pos: Any):

    if self.console.test_mode:
        # code: TM-1
        raise TestModeException(
            pos=ScriptErrors.Position.extract(parent) if parent else pos,
            error="input() not supported in TEST MODE",
            code="1"
        )
    
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
        # code: CFV-5
        suggestion = get_spellcheck_suggestion(var_name, self.scopes.get_all_names())
        raise CantFindVariableException(
            pos=parent_pos,
            var_name=var_name,
            code="5",
            suggestion=suggestion
        )

    variable = self.scopes.get(var_name)

    if variable.type == TYPE_STATE:
        # code: DQA-3
        raise DirectQuantumAccessException(
            pos=ScriptErrors.Position.extract(parent) if parent else pos,
            var_name=var_name,
            code="3"
        )

    # check if variable can be indexed
    if index is not None and variable.type == "Obs":
        # code: ONI-1
        raise ObsNotIndexedException(
            pos=ScriptErrors.Position.extract(parent) if parent else pos,
            var_name=var_name,
            code="1"
        )
    

    # update to given constraint if possible
    if constraint_min is not None:
        min_val = constraint_min
    if constraint_max is not None:
        max_val = constraint_max

    if variable.type == TYPE_NUM:
        max_val = float('inf') if constraint_max is None else max_val
        min_val = float('-inf') if constraint_min is None else min_val  # if no constraints, allow any number
    elif variable.type == TYPE_TEXT:
        max_val = float('inf') if constraint_max is None else max_val
        min_val = 0 if constraint_min is None else min_val
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

        # check text input first
        if variable.type == TYPE_TEXT:
            text_len = len(console_in)

            # Get actual values if they are Expressions
            resolved_min = convert_value(min_val) if isinstance(min_val, Expression) else min_val
            resolved_max = convert_value(max_val) if isinstance(max_val, Expression) else max_val

            if text_len >= resolved_min and text_len <= resolved_max: # if text length is within the allowed range, accept the input
                value = console_in # valid value received -> end of loop
                break

            # Text input format violation
            invalid = [
                "That's not gonna work.", "What even is that input.", "Try again, but correctly.",
                "I can't work with that.", "Rejected.", "Input denied.", "Nice try, but no.",
                "Be serious.", "No idea what that is.", "Nah.", "Hard no.", "Rejected in 0ms.",
                "Absolutely not.", "Fail.", "Not today.", "Not a chance.", "Try harder.",
                "Wrong.", "No.", "Nope.", "That's a no.", "Do better.",
                "Denied.", "I can't let that slide."
            ]
            self.console.write(f"[{random.sample(invalid, 1)[0]} I need text of length {resolved_min}-{resolved_max}] ")
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


        resolved_min = convert_value(min_val) if isinstance(min_val, Expression) else min_val
        resolved_max = convert_value(max_val) if isinstance(max_val, Expression) else max_val

        # user input is invalid, show a message what is expected on the input
        format_str = {None: "decimal", "BIN": "binary", "HEX": "hexadecimal"}[format]
        invalid = [
            "That's not gonna work.", "What even is that input.", "Try again, but correctly.",
            "I can't work with that.", "Rejected.", "Input denied.", "Nice try, but no.",
            "Be serious.", "No idea what that is.", "Nah.", "Hard no.", "Rejected in 0ms.",
            "Absolutely not.", "Fail.", "Not today.", "Not a chance.", "Try harder.",
            "Wrong.", "No.", "Nope.", "That's a no.", "Do better.",
            "Denied.", "I can't let that slide."
        ]

        self.console.write(f"[{random.sample(invalid, 1)[0]} I need a number in range {resolved_min}-{resolved_max} in {format_str} format] ")

    # set value to the variable and update variable in the scope
    if variable.type == TYPE_TEXT:
        value_type = TYPE_TEXT
    else:
        value_type = TYPE_FLOAT if variable.type == "Num" else TYPE_INT
    variable.set(Expression(value_type, value))
    self.scopes.set(var_name, variable)