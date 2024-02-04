from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": """Can you provide me with a python script to sort a list of numbers.
     The constraint is that it should be testable with pytest. Next, can you provide me with a second 
     script that has a fixture list and that tests the first script in the form of a pytest test?"""}
  ]
)

print(completion.choices[0].message)