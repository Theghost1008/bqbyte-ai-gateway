class FlowiseError(Exception):
    """Base exceptions for Flowise-related failures"""

class FlowiseTimeoutError(FlowiseError):
    """Raised when the Flowise service doesnt respond within timeout"""

class FlowiseConnectionError(FlowiseError):
    """Raised when the gateway fails to connect with Flowise service"""

class FlowiseResponseError(FlowiseError):
    """Raised when Flowise service returns an unsuccessfull HTTP response"""