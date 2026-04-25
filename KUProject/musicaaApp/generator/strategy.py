from abc import ABC, abstractmethod
from musicaaApp.model.form import Form


class SongGeneratorStrategy(ABC):

    @abstractmethod
    def generate(self, form: Form) -> str:
        """
        Initiate song generation.
        Returns a task_id (str) tracking the generation process.
        """
        pass

    @abstractmethod
    def get_status(self, task_id: str) -> dict:
        """
        Check the status of a generation job.
        Returns a dictionary containing at least:
        - 'status': e.g., 'pending', 'generating', 'ready', 'error'
        - 'audio_url': URL to the generated audio (if ready)
        - 'error_msg': Error details (if error)
        """
        pass
