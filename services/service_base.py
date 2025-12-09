from typing import Generic, TypeVar

from models import Base
from repositories.repo_base import BaseRepository

RepoType = TypeVar("RepoType", bound=BaseRepository)
ModelType = TypeVar("ModelType", bound=Base)

class BaseService(Generic[RepoType, ModelType]):
    def __init__(self, repo: RepoType) -> None:
        self.repo = repo
    
    