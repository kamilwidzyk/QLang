from __future__ import annotations

from typing import Any, TYPE_CHECKING

from int.exception.internal import InternalException
from int.exception.network_only_var import NetworkNotVariableException
from ..exception.packet_size_must_be import PacketSizeNotIntegerException
from ..exception.invalid_payload import PacketPayloadInvalidException

from ..script_errors import ScriptErrors
from ..consts import *
from ..expression import Expression, TYPE_BOOL, TYPE_INT, TYPE_LIST, TYPE_NUM, TYPE_OBS, TYPE_STATE, TYPE_TEXT
from ..variable import Variable
from ..obs import Obs, ObsRegister
from ..text import Text
from ..num import Num
from ..state import State, StateRegister
from ..QLang.QLangParser import QLangParser
from .expression.variable_expression import handle_variable_expression, is_variable_expression

if TYPE_CHECKING:
    from ..place import Place


def _parse_string_token(token_text: str) -> str:
    """
    Parse raw string to actual string value, handling escape sequences
    """
    text = token_text[1:-1]
    text = text.replace('\\n', '\n')
    text = text.replace('\\t', '\t')
    text = text.replace('\\r', '\r')
    text = text.replace('\\\\', '\\')
    text = text.replace("\\'", "'")
    text = text.replace('\\"', '"')
    text = text.replace('\\`', '`')
    return text


def _is_quantum_type(var_type: str) -> bool:
    """
    Returns True if the given type is a quantum type 
    """
    return var_type == TYPE_STATE


def _extract_place_name(value: Any):
    """
    Extracts raw place name
    """
    while hasattr(value, 'get_value'):
        value = value.get_value()
    if isinstance(value, Text):
        return value.value
    return value


def _resolve_place_id(self: Place, identifier: str, pos: ScriptErrors.Position) -> str:
    """
    Returns the actual place name for a given identifier, checking both quantum network and local scopes.
    """
    if self.quantum_network is not None and identifier in getattr(self.quantum_network, 'valid_places', set()):
        return identifier

    if self.scopes.exists(identifier):
        variable = self.scopes.get(identifier)
        resolved = _extract_place_name(variable)
        if isinstance(resolved, str):
            return resolved
        return str(resolved)

    return identifier


def _type_from_token(token_text: str) -> str:
    """
    Converts type to internal representation
    """
    if token_text == 'obs':
        return TYPE_OBS
    if token_text == 'state':
        return TYPE_STATE
    if token_text == 'num':
        return TYPE_NUM
    if token_text == 'text':
        return TYPE_TEXT
    return token_text


def _evaluate_size(self: Place, size_block: Any) -> int:
    """
    Evaluates the size of a packet
    """
    if size_block.expr() is None:
        # Dynamic size marker '?'
        return -100

    expr = self.handle_block(size_block.expr(), size_block)
    if expr.type != TYPE_INT:
        # code PSNI-1
        raise PacketSizeNotIntegerException(
            ScriptErrors.Position.extract(size_block), 
            code="1")

    if expr.value <= 0:
        # code PSNI-2
        raise PacketSizeNotIntegerException(
            ScriptErrors.Position.extract(size_block), 
            code="2")

    return expr.value


def _derive_packet_size(variable: Any, explicit_size: int | None = None) -> int:
    """
    Derives packet size based on variable/expression and explicit size (if provided)
    """
    if explicit_size is not None:
        return explicit_size
    if isinstance(variable, Variable):
        if variable.index is not None and len(variable.index) > 0:
            variable = variable.get()
    if isinstance(variable, Expression):
        if variable.type == TYPE_LIST and isinstance(variable.value, (list, tuple)):
            return len(variable.value)
        return 1
    if isinstance(variable, Variable):
        if variable.type == TYPE_STATE:
            if variable.is_list:
                return len(variable.data)
            return 1
        if variable.type == TYPE_OBS and variable.is_list:
            return len(variable.data)
        if variable.type in [TYPE_NUM, TYPE_TEXT] and variable.is_list:
            return len(variable.data)
        if variable.type in [TYPE_NUM, TYPE_TEXT]:
            return 1
        if hasattr(variable.data, '__len__'):
            return len(variable.data)
        return 1
    if isinstance(variable, (list, tuple)):
        return len(variable)
    return 1


def _serialize_value(value: Any, var_type: Any) -> Any:
    """
    Prepare value for travel thru the network
    """
    if isinstance(value, list):
        return [_serialize_value(v, var_type) for v in value]

    if isinstance(value, Expression):
        # Avoid calling `get_value()` for quantum `State` expressions
        # because `State.get_value()` raises (state is opaque).
        if value.type == TYPE_STATE:
            # If the expression is a list of states, serialize each entry
            if isinstance(value.value, list):
                return _serialize_value(value.value)
            # If the underlying value is a State, serialize its uid
            if isinstance(value.value, State):
                return {'__qstate__': True, 'uid': value.value.uid}
            # Fallback: try to serialize the raw value
            return _serialize_value(value.value)

    if isinstance(value, State):
        return {'__qstate__': True, 'uid': value.uid}

    if var_type == TYPE_OBS:
        return {'__obs__': int(value.get_value() if hasattr(value, 'get_value') else value)}

    if isinstance(value, Obs):
        return {'__obs__': int(value.get())}

    if isinstance(value, Num):
        return {'__num__': value.get_value()} 

    if isinstance(value, Text):
        return {'__text__': value.value}

    return value


def _serialize_variable(variable: Variable) -> Any:
    """
    Duplicate from older version
    """
    print("Serializing variable:", variable.name, "of type:", variable.type)
    print("serialized: ", _serialize_value(variable.data, variable.type))
    return _serialize_value(variable.data, variable.type)


def _deserialize_state_payload(payload: Any) -> Any:
    """
    Parse received payload of state variable
    """
    if isinstance(payload, list):
        return [_deserialize_state_payload(item) for item in payload]

    if isinstance(payload, dict) and payload.get('__qstate__'):
        return State(client=None, uid=payload['uid'])

    # code: PPI-1
    raise PacketPayloadInvalidException(
        ScriptErrors.Position.extract(payload) if hasattr(payload, 'start') else ScriptErrors.Position(0, 0), 
        code="1"
    )

def _deserialize_value(self: Place, payload: Any, var_type: str) -> Any:
    """
    Deserializes any value received thru the network
    """
    if var_type == TYPE_STATE:
        if isinstance(payload, dict) and payload.get('__qstate__'):
            return State(client=self.quantum_client, uid=payload['uid'])
        if isinstance(payload, list):
            return [_deserialize_value(self, item, TYPE_STATE) for item in payload]
        
        # code: PPI-2
        raise PacketPayloadInvalidException(
                ScriptErrors.Position.extract(payload) if hasattr(payload, 'start') else ScriptErrors.Position(0, 0), 
                code="2"
            )

    if var_type == TYPE_OBS:
        if isinstance(payload, dict) and payload.get('__obs__') is not None:
            return payload['__obs__']
        if isinstance(payload, list):
            result = []
            for item in payload:
                result.append(_deserialize_value(self, item, var_type))
            return result
        
        return payload

    if var_type == TYPE_NUM:
        if isinstance(payload, dict) and payload.get('__num__') is not None:
            return payload['__num__']
        if isinstance(payload, list):
            result = []
            for item in payload:
                result.append(_deserialize_value(self, item, var_type))
            return result
        return payload

    if var_type == TYPE_TEXT:
        if isinstance(payload, dict) and payload.get('__text__') is not None:
            return payload['__text__']
        if isinstance(payload, list):
            result = []
            for item in payload:
                result.append(_deserialize_value(self, item, var_type))
            return result
        return payload

    return payload


def _get_receive_filters(self: Place, block: Any, pos: ScriptErrors.Position) -> tuple[str | None, str | None]:
    """
    Extract packet receive filters
    """
    src_id = None
    msg_id = None
    receive_filters = block.receiveFilter() if hasattr(block, 'receiveFilter') else block.receiveOpt()
    for opt in receive_filters:
        if opt.FROM():
            if opt.STRING() is not None:
                src_id = _parse_string_token(opt.STRING().getText())
            elif opt.ID() is not None:
                src_id = _resolve_place_id(self, opt.ID().getText(), pos)
        if (hasattr(opt, 'NAMED') and opt.NAMED()) or (hasattr(opt, 'AS') and opt.AS()):
            if opt.STRING() is not None:
                msg_id = _parse_string_token(opt.STRING().getText())
            elif opt.ID() is not None:
                msg_id = _resolve_place_id(self, opt.ID().getText(), pos)
    return src_id, msg_id


def _get_available_filters(self: Place, block: Any, pos: ScriptErrors.Position) -> tuple[bool | None, str | None, str | None]:
    """
    Extract packet available filters
    """
    quantum = None
    src_id = None
    msg_id = None
    for filt in block.availableFilter():
        if filt.varType() is not None:
            var_type = filt.varType().getText()
            quantum = _is_quantum_type(_type_from_token(var_type))
        elif filt.FROM() is not None:
            if filt.STRING() is not None:
                src_id = _parse_string_token(filt.STRING().getText())
            elif filt.ID() is not None:
                src_id = _resolve_place_id(self, filt.ID().getText(), pos)
        elif filt.NAMED() is not None:
            if filt.STRING() is not None:
                msg_id = _parse_string_token(filt.STRING().getText())
            elif filt.ID() is not None:
                msg_id = _resolve_place_id(self, filt.ID().getText(), pos)
    return quantum, src_id, msg_id


def handle_send_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles send statement
    """
    if self.quantum_network is None:
        # code: I-1
        raise InternalException(
            pos=pos,
            msg='Quantum network is not initialized.',
            code="1"
        )

    expr_ctx = block.expr()
    if not is_variable_expression(expr_ctx):
        # code: NNV-1
        raise NetworkNotVariableException(
                ScriptErrors.Position.extract(expr_ctx), 
                code="1"
            )

    variable = handle_variable_expression(self, expr_ctx, block, ScriptErrors.Position.extract(expr_ctx), return_variable=True)

    size = None

    target_id = None
    msg_id = None
    target_node = None
    as_node = None
    for i in range(block.getChildCount()):
        child = block.getChild(i)
        if child.getText() == 'to':
            target_node = block.getChild(i + 1)
        elif child.getText() == 'as':
            as_node = block.getChild(i + 1)
            
    if target_node is not None:
        if target_node.getSymbol().type == QLangParser.STRING:
            target_id = _parse_string_token(target_node.getText())
        else:
            target_id = _resolve_place_id(self, target_node.getText(), pos)
            
    if as_node is not None:
        if as_node.getSymbol().type == QLangParser.STRING:
            msg_id = _parse_string_token(as_node.getText())
        else:
            msg_id = _resolve_place_id(self, as_node.getText(), pos)

    if isinstance(variable, Variable) and variable.index is not None and len(variable.index) > 0:
        expr = variable.get()
        payload = _serialize_value(expr.get_value()) if isinstance(expr, Expression) else _serialize_value(expr)
        packet_size = _derive_packet_size(expr, size)
        quantum_flag = _is_quantum_type(variable.type)
    else:
        if isinstance(variable, list):
            payload = _serialize_value(variable)
        else:
            payload = _serialize_variable(variable)
        packet_size = _derive_packet_size(variable, size)
        quantum_flag = _is_quantum_type(variable.type)

    self.quantum_network.send(
            src_id=self.name,
            msg_id=msg_id,
            target_id=target_id,
            quantum=quantum_flag,
            size=packet_size,
            data=payload,
            log_packet=self.packet_log_enabled,
        )

def handle_receive_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handle receive statement
    """
    if self.quantum_network is None:
        # code: I-2
        raise InternalException(
            pos=pos,
            msg='Quantum network is not initialized.',
            code="2"
        )

    var_type = _type_from_token(block.varType().getText())
    var_name = block.ID().getText() if hasattr(block, 'ID') else block.varNoAssign().ID().getText()
    dimensions = []
    size_vars = block.sizeVar() if hasattr(block, 'sizeVar') else block.varNoAssign().sizeVar()
    for size_var in size_vars:
        dimensions.append(_evaluate_size(self, size_var))

    if len(dimensions) == 0:
        dimensions = [0]

    src_id, msg_id = _get_receive_filters(self, block, pos)
    quantum = _is_quantum_type(var_type)

    packet_size = None if dimensions[0] == -100 else (dimensions[0] if dimensions[0] != 0 else 1)
    if isinstance(packet_size, int) and packet_size <= 0:
        # code: PSNI-3
        raise PacketSizeNotIntegerException(
            ScriptErrors.Position.extract(size_vars[0]) if size_vars else pos, 
            code="3"
        )

    payload = self.quantum_network.wait_for(
        target_id=self.name,
        src_id=src_id,
        msg_id=msg_id,
        quantum=quantum,
        size=packet_size,
        log_packet=self.packet_log_enabled,
    )

    if var_type == TYPE_STATE:
        received_data = _deserialize_value(self, payload, TYPE_STATE)
        var = Variable(var_name, var_type, dimensions, quantum_client=self.quantum_client, initial_data=received_data)
    else:
        var = Variable(var_name, var_type, dimensions, quantum_client=self.quantum_client)
        deserialized = _deserialize_value(self, payload, var_type)
        if dimensions != [0]:
            var.set(Expression(TYPE_LIST, deserialized))
        else:
            if var_type == TYPE_OBS:
                var.set(Expression(TYPE_BOOL, bool(deserialized)))
            elif var_type == TYPE_NUM:
                var.set(Expression(TYPE_NUM, deserialized))
            elif var_type == TYPE_TEXT:
                var.set(Expression(TYPE_TEXT, deserialized))
            else:
                var.set(Expression(TYPE_INT, deserialized))

    print("Receive scope create")
    print(var_name, var, type(var))
    print(var.get().get_value())
    self.scopes.create(var_name, var)


def handle_available_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handle available expression
    """
    if hasattr(block, 'availableExpr'):
        block = block.availableExpr()

    if self.quantum_network is None:
        # code: I-3
        raise InternalException(
            pos=pos,
            msg='Quantum network is not initialized.',
            code="3"
        )

    quantum, src_id, msg_id = _get_available_filters(self, block, pos)
    is_available = self.quantum_network.peek(
        target_id=self.name,
        src_id=src_id,
        msg_id=msg_id,
        quantum=quantum,
        size=None,
    )
    return Expression(TYPE_BOOL, is_available)
