from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

from vector import retriever  #import the retriever from the vector.py file

model = OllamaLLM(model="llama3.2") #Ollama provides us with the ability to use local LLMs. we can check the available models by running `ollama list` in the terminal.

#create a template to specify how we want to interact with the model and should he do
template = "you are an expert in answering about pizza restaurants" \
"here some reviews about pizza restaurants: {reviews}" \
"Based on the reviews, answer the following question: {question}"


  # example dynamic template. "you are an expert about answering questions about {topic}. Answer the following question: {question}"

prompt = PromptTemplate.from_template(template)

#create a chain that will use the model and the prompt to answer questions:
chain = prompt | model

while True:
    print("\n\n====================================")
    question = input("Ask a question about pizza restaurants or type q to quit: ")
    if question == "q":
        break
    print("Generating answer...\n\n")

    reviews = retriever.invoke(question) # invoke the reriever with our question

    result = chain.invoke({"reviews":reviews, "question":question})

    print(result)

