from ..config import settings

class GeminiClient:
    def __init__(self):
        self.client = None
        self.import_error = None

        if settings.GOOGLE_API_KEY.strip():
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            except Exception as exc:
                self.import_error = exc

    def generate(self, prompt: str, model: str) -> str:
        if self.client is None:
            if self.import_error:
                raise RuntimeError(
                    f"Gemini SDK could not be loaded: {self.import_error}. "
                    "Run: pip install -r requirements.txt"
                )
            raise RuntimeError(
                "Gemini API key is missing. Add GOOGLE_API_KEY to .env "
                "or keep AI_DEMO_MODE=true for local testing."
            )

        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()


gemini_client = GeminiClient()
