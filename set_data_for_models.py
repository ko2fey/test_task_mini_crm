from database import get_db

from repositories.repo_operator import OperatorRepository
from repositories.repo_source import SourceRepository
from repositories.repo_priorities import PriorityRepository


operators = [
    {
        "name": "Первак",
        "max_loading": 10,
        "active": True
    },
    {
        "name": "Вторяк",
        "max_loading": 10,
        "active": True
    },
    {
        "name": "Третьяк",
        "max_loading": 10,
        "active": True
    },
]

sources = [
    {"name": "Telegram bot"},
    {"name": "Vk group"},
    {"name": "WatsApp bot"},
]

priorities = [
    {
        "operator_id": 1,
        "source_id": 1,
        "weight": 10
    },
    {
        "operator_id": 1,
        "source_id": 2,
        "weight": 10
    },
    {
        "operator_id": 1,
        "source_id": 3,
        "weight": 10
    },
    {
        "operator_id": 2,
        "source_id": 1,
        "weight": 7
    },
    {
        "operator_id": 2,
        "source_id": 2,
        "weight": 7
    },
    {
        "operator_id": 3,
        "source_id": 2,
        "weight": 5
    },
    {
        "operator_id": 3,
        "source_id": 3,
        "weight": 5
    },
]

def set_operators(db):
    operator_repo = OperatorRepository(db)
    
    for operator in operators:
        operator_repo.create(operator)

def set_sources(db):
    source_repo = SourceRepository(db)
    
    for source in sources:
        source_repo.create(source)

def set_priority(db):
    priority_repo = PriorityRepository(db)
    
    for priority in priorities:
        priority_repo.create(priority)
        
db = next(get_db())
set_operators(db)
set_sources(db)
set_priority(db)