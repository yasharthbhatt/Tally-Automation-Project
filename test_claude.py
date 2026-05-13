from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in 1 line"}
    ]
)

print(response.content[0].text)