from requests_html import HTMLSession
import re
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from tkinter import *




generation_config = {
    "max_output_tokens": 2048,
    "temperature": 1,
    "top_p": 1,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

def generate(urlstring):
  session = HTMLSession()
  home = session.get(urlstring)
  homeText = re.sub("\n"," ",home.text)
  homeText = re.sub(r'<[^>]+>', ' ', homeText)
  homeText = re.sub(r'{[^}]+}', ' ', homeText)


  homeText = re.sub(r'\s+', ' ', homeText)
  homeText = re.sub(r'Join now to see.*', ' ', homeText)
  homeText = re.sub(r'.*"description":', ' ', homeText)
  homeText = re.sub(r'Like Comment Share', ' ', homeText)
  vertexai.init(project="eurecax", location="us-central1")
  model = GenerativeModel("gemini-1.0-pro-002")
  responses = model.generate_content(
      [(homeText + "\n\n find only the following: company name, number of employees, core capabilities, operating location, technology field")],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )
  out = ""
  for response in responses:
     print(response.text, end="")

  


top = Tk()
url = StringVar(top, "https://www.linkedin.com/company/chaos1/")

frame= Frame(top, padx=2 , pady=2, width=1000, height=500)
frame.pack(expand=TRUE)

L1 = Label(frame, text="URL")
L1.pack( side = LEFT)

E1 = Entry(frame, bd =5, textvariable=url, width=50)
E1.pack( side = LEFT)

def request():
  print(url.get())
  generate(url.get())

E1 = Button(frame, text="Generate", command=request)
E1.pack( side = LEFT)

top.mainloop()