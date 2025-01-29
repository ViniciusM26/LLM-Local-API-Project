from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from docx import Document
import os
import datetime
import subprocess
import re


app = FastAPI()

# Configuração de templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório para salvar os resumos
OUTPUT_DIR = "resumos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Página inicial da aplicação.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/summarize/")
async def summarize_text(request: Request, text: str = Form(...)):
    """
    Endpoint para resumir o texto e salvar no Word.
    """
    try:
        # Gerar título e resumo
        title, summary = run_llama(text)

        # Salvar o resumo em um arquivo Word com o título como nome
        file_path = save_to_word(title, summary)

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "summary": summary, "file_path": file_path},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    """
    Permite o download de um arquivo Word gerado.
    """
    file_path = os.path.join(OUTPUT_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

def run_llama(text):
    """
    Executa o modelo LLaMA via Ollama para gerar um título e um resumo.
    """
    try:
        # Comando para rodar o modelo usando Ollama
        command = ["ollama", "run", "llama3.2:1b", f"Resuma o seguinte texto e gere um título curto. Use este formato: 'Título: <título gerado>\\nResumo: <resumo gerado>'\\n\\n{text}"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")

        if result.returncode != 0:
            raise Exception(f"Ollama error: {result.stderr.strip()}")

        # Log da saída do comando
        output = result.stdout.strip()
        print(f"Saída do comando: {output}")

        # Verifica se o modelo seguiu corretamente o formato
        match = re.search(r"Título:\s*(.*?)\s*\nResumo:\s*(.*)", output, re.DOTALL | re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            summary = match.group(2).strip()
        else:
            # Alternativa: Considerar a primeira linha curta como título e o restante como resumo
            lines = output.split("\n", 1)
            if len(lines) > 1 and len(lines[0]) < 50:  # Assume que títulos são curtos
                title = lines[0].strip()
                summary = lines[1].strip()
            else:
                raise Exception("Formato de saída inesperado do modelo.")

        return title, summary
    except Exception as e:
        raise Exception(f"Erro ao executar o modelo: {str(e)}")

def sanitize_filename(title):
    """
    Remove caracteres inválidos do título para uso como nome de arquivo.
    """
    return re.sub(r'[<>:"/\\|?*]', '', title)  # Remove caracteres inválidos no Windows

def save_to_word(title, summary):
    """
    Salva o resumo em um arquivo Word com um nome baseado no título gerado pelo LLaMA.
    """
    # Garantir que o diretório OUTPUT_DIR exista
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Criar o documento Word
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(summary)

    # Limpar o título para ser um nome de arquivo válido
    sanitized_title = sanitize_filename(title)

    # Nome do arquivo baseado no título gerado
    file_name = f"{sanitized_title}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    # Salvar o documento
    doc.save(file_path)
    return file_name




