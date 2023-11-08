import openai

API_KEY_FILE = "openai_api_key.txt"
CACHE_FILE = "chat_response.txt"
GPT_3_5_TURBO = "gpt-3.5-turbo"
GPT_4 = "gpt-4"


class OpenAIApi:
    def __init__(self):
        with open("openai_api_key.txt", 'r') as f:
            openai.api_key = f.read()

    def chat(self, system_instructions, prompt, skip_cache=False, use_gpt4=False):
        response_string = None
        if not skip_cache:
            response_string = self.read_from_cache()
        if response_string:
            return response_string
        response = openai.ChatCompletion.create(
            model=GPT_4 if use_gpt4 else GPT_3_5_TURBO,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ]
        )
        response_string = response.choices[0]["message"]["content"]
        self.write_to_cache(response_string)
        return response_string

    def read_from_cache(self):
        with open(CACHE_FILE, 'r') as f:
            return f.read()

    def write_to_cache(self, string_to_write):
        with open(CACHE_FILE, 'w') as f:
            f.write(string_to_write)
