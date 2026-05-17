from typing import Any


class QuantumResponse:
    class Status:
        OK = "ok"
        ERROR = "error"

    def __init__(self, status: Status, content: Any):
        self.status = status
        self.content = content

    @classmethod
    def ok(cls, content: Any) -> QuantumResponse:
        return cls(QuantumResponse.Status.OK, content)
    
    @classmethod
    def error(cls, error: Any) -> QuantumResponse:
        return cls(QuantumResponse.Status.ERROR, error)
    
    def is_ok(self) -> bool:
        return self.status == QuantumResponse.Status.OK
    
    def is_error(self) -> bool:
        return self.status == QuantumResponse.Status.ERROR
    
    def get_content(self) -> Any:
        return self.content
    
    def get_error(self) -> Any:
        return self.content
    
    
