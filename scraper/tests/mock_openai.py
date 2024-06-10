class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.chat = MockChat()

class MockChat:
    def __init__(self):
        self.completions = MockCompletions()

class MockCompletions:
    def create(self, messages, model):
        content = self.generate_content(messages[0]['content'])
        mock_response = MockResponse(content)
        return mock_response

    def generate_content(self, prompt):
        if "Check if all the items in the list are valid names." in prompt:
            if "['Alice', 'Bob', 'Charlie']" in prompt:
                return "all items are valid names"
            else:
                return "some items are not valid names"
        content = "```python\ndef extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n```"
        return content

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content