import os
import openai
import gradio as gr
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

# if you have OpenAI API key as an environment variable (e.g. .env file), enable the below
openai.api_key = os.getenv("OPENAI_API_KEY")

# set username and password for authentication
GRADIO_USERNAME = os.getenv("GRADIO_USERNAME")
GRADIO_PASSWORD = os.getenv("GRADIO_PASSWORD")


# Input configurations
start_sequence = "\nAI:"
restart_sequence = "\nHuman: "
prompt = "The following is a conversation with an AI story teller.\
    The AI is helpful, creative, clever, and very friendly.\
    \n\nHuman: Hello, who are you?\
    \nAI: I am an AI that can write imaginative and captivating short stories.\
    What would you like your story to be about?\
    \nHuman:"
storyteller_base = "I want you to act as a storyteller.\
    You will come up with entertaining stories that are engaging,\
    imaginative and captivating for the audience. \
    It can be fairy tales, educational stories or any other type of stories \
    which has the potential to capture people's attention and imagination. \
    Depending on the target audience, you may choose specific themes \
    or topics for your storytelling session e.g., if it’s children \
    then you can talk about animals; If it’s adults then history-based tales \
    might engage them better etc. \
    My first request is to tell me the story of\n "
examples = [
    "A venture capitalist who prioritized profit over ethics",
    "Brave dinasour who stood up for his friends in difficult situations",
]


# Functions for OpenAI interactions
def openai_create(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=1400,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].text

# Functions for OpenAI interactions
def openai_create_from_base(prompt, base):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=base+prompt,
    temperature=0.9,
    max_tokens=1400,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].text

# Gradio requires that we have input and outputs
def davinci_chat(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    # logic is different if the history exists
    if not history:
        output = openai_create_from_base(
            prompt=inp, 
            base=storyteller_base)
    else:
        output = openai_create(
            prompt=inp)
    history.append((input, output))
    return history, history

block = gr.Blocks()
with block:
    gr.Markdown("""<h1><center>Generate a story with an AI assistant</center></h1>
    """)
    message = gr.Textbox(
        placeholder=prompt)
    examples=examples
    chatbot = gr.Chatbot()
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(
        fn=davinci_chat, 
        inputs=[message, state], 
        outputs=[chatbot, state])

block.launch(
    share=False, 
    auth=(GRADIO_USERNAME, GRADIO_PASSWORD),
    debug=True)