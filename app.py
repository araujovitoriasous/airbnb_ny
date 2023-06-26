from flask import Flask, render_template, request
import openai
import pandas as pd

app = Flask(__name__)

# Configuration of OpenAI API key
openai.api_key = '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'

# Global variable to store the CSV data
csv_data = None

# Main route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pergunta', methods=['POST', 'GET'])
def pergunta():
    global csv_data

    if request.method == 'POST':
        if csv_data is None:
            csv_data = scrape_data_from_xlsx()
            if csv_data is None:
                return render_template('index.html', how_questions=True, error='Failed to extract data!')

        question = request.form.get('question')

        if question:
            resposta = responder_pergunta(question, csv_data)
            return render_template('index.html', answer=resposta, show_questions=True)

    return render_template('index.html')

# Perform web scraping from the website
def scrape_data_from_xlsx():
    xlsx_filename = 'AB_NYC_2019.xlsx'
    df = pd.read_excel(xlsx_filename)
    return df

# Function to answer questions using OpenAI ChatGPT
def responder_pergunta(pergunta, data):
    perguntas = [
        "Qual é o menor valor de aluguel?",
        "Qual é o maior valor de aluguel?",
        "Qual é o bairro mais citado?",
        "Qual é o bairro mais caro?",
        "Qual é o bairro menos citado?",
        "Qual é o bairro menos caro?",
        "Qual é a média de valores?",
        "Qual é a acomodação mais frequente?"
    ]

    # Check if the question is in the list of questions
    if pergunta not in perguntas:
        return "Desculpe, não posso responder a essa pergunta."

    # Prepare the prompt for the specific question
    prompt = f"Pergunta: {pergunta}\nDados: {data}\nResposta:"

    # Generate the response using OpenAI ChatGPT
    resposta = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        n=1,
        stop=None,
        temperature=0.7
    )

    return resposta.choices[0].text

if __name__ == '__main__':
    app.run(debug=True)
