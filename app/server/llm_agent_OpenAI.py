from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-4o-mini",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text);