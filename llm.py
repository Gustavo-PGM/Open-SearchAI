import datetime
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

current_date = datetime.datetime.now().strftime("%Y-%m")

class CustomModel(OpenAIChatCompletionsModel):
    @property
    def supports_tools(self):
        return "llama" not in self.model.lower()

model = CustomModel(
    model="SEU MODELO LOCAL",
    openai_client=AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="none")
)