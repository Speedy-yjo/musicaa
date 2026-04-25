import uuid
import random
from .strategy import SongGeneratorStrategy
from musicaaApp.model.form import Form


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Mock strategy that simulates song generation without making external API calls.
    It produces predictable outputs suitable for local development and testing.
    """

    def generate(self, form: Form) -> str:
        # Generate a fake task ID
        # Since it is a mock, we can generate a consistent format string like 'mock_task_xxx'
        fake_task_id = f"mock_task_{uuid.uuid4().hex[:8]}"
        print(f"[Mock Generator] Started generating mock song for form '{form.name}'. Task ID: {fake_task_id}")
        return fake_task_id

    def get_status(self, task_id: str) -> dict:
        # Simulate status check
        print(f"[Mock Generator] Checking status for Task ID: {task_id}")
        
        # We can randomize status, but to be somewhat predictable,
        # we could just always return SUCCESS in this mock for straightforward testing.
        return {
            'status': 'SUCCESS',
            'audio_url': 'https://example.com/mock-audio-file.mp3',
            'error_msg': None
        }
