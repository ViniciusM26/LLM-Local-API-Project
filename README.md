# LLM Local com LLaMA 2 e FastAPI

Este projeto é uma aplicação web desenvolvida com FastAPI que utiliza um modelo de linguagem LLaMA 2 para gerar resumos de textos fornecidos pelo usuário. Os resumos gerados são salvos como arquivos Word e podem ser baixados diretamente pela interface web.

## Recursos Principais

- **Interface Web**: Uma página inicial simples para enviar textos e visualizar os resumos gerados.
- **Resumos Baseados em LLaMA 2**: Uso de um modelo LLaMA para resumir textos.
- **Arquivos Word**: Os resumos gerados são salvos em arquivos `.docx`.
- **Download de Arquivos**: Os arquivos podem ser baixados diretamente pela interface web.

---

## Requisitos

Antes de executar a aplicação, certifique-se de ter os seguintes requisitos instalados:

- **Python 3.8+**
- **FastAPI**
- **Jinja2**
- **Python-docx**
- **Ollama** (para rodar o modelo LLaMA)
- **Subprocesso** habilitado no ambiente

---

## Instalação

1. Clone este repositório:
```
git clone https://github.com/ViniciusM26/LLM-Local-API-Project.git
```
2. Instalando o Ollama:
```
No Windows
Baixe o instalador no site oficial:
https://ollama.com/download
Siga as instruções do instalador para concluir a instalação.

Baixar o Modelo Utilizado:
O projeto utiliza o modelo LLaMA 3, que pode ser baixado com o seguinte comando: ollama pull llama3.2:1b

Testar a Instalação
Após a instalação, execute o seguinte comando para testar se o Ollama está funcionando corretamente: ollama run llama3.2:1b

Se tudo estiver configurado corretamente, o terminal abrirá um prompt onde você pode digitar comandos para o modelo.

Agora, seu ambiente está pronto para rodar a API de resumo e geração de títulos! 🚀
```
3. Crie um ambiente virtual:
```
python -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate
```
4. Instale as dependências:
```
pip install -r requirements.txt
```
## Como usar

1. Inicie o servidor FastAPI:
```
uvicorn main:app --reload
```
2. Acesse a aplicação no navegador em:
```
http://127.0.0.1:8000
```
3. Insira o texto que deseja resumir no campo apropriado e clique em Resumir.

4. O resumo será exibido na página e poderá ser baixado como um arquivo Word.


   


   
   

