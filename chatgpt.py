# pip install openai
# MAC/LINUX: export OPENAI_API_KEY=...
# WINDOWS: setx OPENAI_API_KEY "..."

from openai import OpenAI
client = OpenAI(
    api_key="..."
)

completion = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  messages=[
    {"role": "system", "content": "QA Chatbot that helps with testing questions."},
    {"role": "user", "content": "How should I validate html inputs?"},
    {"role": "assistant", "content": "You can use the HTML5 form validation feature to validate the input fields."}    
  ],
  # 0-2
  temperature=0.2
)

print(completion.choices[0].message)

