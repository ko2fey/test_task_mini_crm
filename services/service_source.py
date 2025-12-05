import schemas
from repositories.repo_source import SourceRepository

class SourceService:
    def __init__(self, repo):
        self.repo: SourceRepository = repo

    def get_contacts(self, id: int):
        contacts = self.repo.get_list_contacts(id)
        response = {
            'objects': contacts,
            'total_count': len(contacts)
        }
        return response