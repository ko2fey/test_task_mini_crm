from fastapi.exceptions import HTTPException

class ServiceException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
    

class NotFoundException(ServiceException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=404, 
            detail=detail
        )

class ForbiddenDeleteException(ServiceException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=403, 
            detail=detail
        )

class FailedUpdateException(ServiceException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500, 
            detail=detail
        )

class DatabaseException(ServiceException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code, 
            detail=detail
        )

class UnexpectedException(ServiceException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code, 
            detail=detail
        )