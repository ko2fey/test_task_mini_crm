from fastapi.exceptions import HTTPException

class RepositoryException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(RepositoryException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=404, 
            detail=detail
        )

class ForbiddenDeleteException(RepositoryException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=403, 
            detail=detail
        )

class FailedUpdateException(RepositoryException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500, 
            detail=detail
        )

class DatabaseException(RepositoryException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code, 
            detail=detail
        )

class UnexpectedException(RepositoryException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code, 
            detail=detail
        )