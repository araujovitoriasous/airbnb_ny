from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# Configuração da chave de API da OpenAI
openai.api_key = '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'

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')

        if user_input.startswith('http'):
            data = scrape_data_from_file()
            if data is None:
                return render_template('index.html', how_questions=True, error='Failed to scrape data from the URL!')
            return render_template('scraped_data.html', data=data)

        response = openai.Completion.create(
            engine="davinci",
            prompt=user_input,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()

        return render_template('index.html', answer=answer, show_questions=True)

    return render_template('index.html')



# Realiza o web scraping a partir de um arquivo
def scrape_data_from_file():
    try:
        with open('dados.txt', 'r') as file:
            arquivo = file.read()
        soup = BeautifulSoup(arquivo, 'html.parser')
        return scrape_data(soup)
    except Exception as e:
        print(e)
        return None

# Realiza o web scraping propriamente dito
def scrape_data(soup):
    try:
        resultados_combinados = soup.find_all("tr", attrs={"class": ["odd", "even"]})
        data = {}
        for re in resultados_combinados:
            td_tags = re.find_all("td")
            for i, td in enumerate(td_tags):
                if i not in data:
                    data[i] = []
                data[i].append(td.text)
        return data
    except Exception as e:
        print(e)
        return None



if __name__ == '__main__':
    app.run(debug=True)
