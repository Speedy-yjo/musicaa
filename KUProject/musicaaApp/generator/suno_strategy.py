import requests
from django.conf import settings
from .strategy import SongGeneratorStrategy
from musicaaApp.model.form import Form


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Suno API strategy that integrates with SunoApi.org to generate music.
    Requires SUNO_API_KEY to be set in settings.
    """

    BASE_URL = "https://api.sunoapi.org/api/v1"

    def __init__(self):
        self.api_key = getattr(settings, 'SUNO_API_KEY', '')
        if not self.api_key or self.api_key == 'your_api_key_here':
            print("Warning: SUNO_API_KEY is not configured properly.")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, form: Form) -> str:
        # Preparing parameters matching the new sunoapi.org schema
        payload = {
            "prompt": f"Mood: {form.mood}. Genre: {form.genre}. Occasion: {form.occasion}. {form.prompt}",
            "instrumental": False,
            "model": "V3_5",
            "customMode": False,
            "callBackUrl": "https://httpbin.org/post"
        }

        endpoint = f"{self.BASE_URL}/generate"
        response = requests.post(endpoint, json=payload, headers=self._get_headers())
        
        response.raise_for_status()
        data = response.json()
        
        # Check if the API returned an error inside a 200 OK
        if data.get("code") != 200:
            raise Exception(f"SunoAPI Error: {data.get('msg')}")

        # Extract taskId
        task_id = data.get("data", {}).get("taskId")
        if not task_id and "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            task_id = data["data"][0].get("id")

        return task_id

    def get_status(self, task_id: str) -> dict:
        endpoint = f"{self.BASE_URL}/generate/record-info"
        params = {"taskId": task_id}

        response = requests.get(endpoint, params=params, headers=self._get_headers())
        response.raise_for_status()
        data = response.json()

        if data.get("code") != 200:
            return {"status": "ERROR", "audio_url": None, "error_msg": data.get("msg")}

        record = data.get("data", {})
        status = record.get("status", "PENDING")
        
        # Audio URL is buried in response -> sunoData -> [0] -> streamAudioUrl
        audio_url = None
        suno_data = record.get("response", {}).get("sunoData", [])
        if suno_data and len(suno_data) > 0:
            audio_url = suno_data[0].get("streamAudioUrl") or suno_data[0].get("audioUrl")

        return {
            "status": status,
            "audio_url": audio_url,
            "error_msg": None
        }
