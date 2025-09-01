from flask import Flask, render_template, request, redirect, url_for, session, Response
import pandas as pd
import io
from weasyprint import HTML
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid # Usado para criar nomes de arquivo únicos

# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# --- CONFIGURAÇÃO ---
# Define o caminho para a pasta de arquivos temporários
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)


# --- FUNÇÕES AUXILIARES ---

def criar_links(url):
    """Transforma URLs em links HTML clicáveis"""
    if isinstance(url, str) and url.startswith('http'):
        return f'<a href="{url}" target="_blank">{url}</a>'
    return url

def processar_csv(file, palavras_chave):
    """Processa o arquivo CSV e retorna os dados filtrados"""
    df = pd.read_csv(file, skiprows=5)
    regex_busca = '|'.join(palavras_chave)
    
    coluna_descricao = 'Relato'
    necessidades = df[df[coluna_descricao].astype(str).str.contains(regex_busca, case=False, na=False)].copy()
    
    colunas_resultado = ['Data', 'Cliente', 'Endereco', 'OS Digital', 'Relato']
    return df, necessidades[colunas_resultado]

def gerar_estatisticas(df_original, df_filtrado, palavras_chave):
    """Gera estatísticas simples dos dados"""
    total = len(df_original)
    filtrados = len(df_filtrado)
    
    stats = {
        'total': total,
        'filtrados': filtrados,
        'percentual': round((filtrados/total)*100, 1) if total > 0 else 0,
        'por_palavra': {}
    }
    
    for palavra in palavras_chave:
        if not df_filtrado.empty:
            count = int(df_filtrado['Relato'].str.contains(palavra, case=False, na=False).sum())
            if count > 0:
                stats['por_palavra'][palavra] = count
    
    return stats

def salvar_historico(filename, stats):
    """Salva o histórico de processamentos na sessão"""
    hist = session.get('historico', [])
    hist.insert(0, {
        'arquivo': filename,
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'encontrados': stats['filtrados'],
        'total': stats['total']
    })
    session['historico'] = hist[:10]

# --- NOVA FUNÇÃO PARA LER OS DADOS DO ARQUIVO TEMPORÁRIO ---
def get_dataframe_from_temp_file():
    """Pega o nome do arquivo da sessão e o lê como um DataFrame."""
    temp_filename = session.get('temp_filename')
    if not temp_filename:
        return None
    
    # Constrói o caminho completo e seguro para o arquivo
    file_path = os.path.join(TEMP_FOLDER, temp_filename)
    
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None


# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        session['custom_keywords'] = [k.strip() for k in keywords if k.strip()]
        return redirect(url_for('index'))
    
    current_keywords = session.get('custom_keywords', ['solicitar peça', 'quebrado', 'trocar cabo', 'soldar', 'trocar', 'instalar'])
    return render_template('config.html', keywords=', '.join(current_keywords))

@app.route('/historico')
def historico():
    hist = session.get('historico', [])
    return render_template('historico.html', historico=hist)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'arquivo_excel' not in request.files:
        return redirect(url_for('index', error='Nenhum arquivo selecionado'))
    
    file = request.files['arquivo_excel']
    if file.filename == '':
        return redirect(url_for('index', error='Nenhum arquivo selecionado'))

    if not file.filename.lower().endswith('.csv'):
        return redirect(url_for('index', error='Por favor, selecione um arquivo .csv'))

    try:
        palavras_chave = session.get('custom_keywords', ['solicitar peça', 'quebrado', 'trocar cabo', 'soldar', 'trocar', 'instalar'])
        
        df_original, resultado_final = processar_csv(file, palavras_chave)
        stats = gerar_estatisticas(df_original, resultado_final, palavras_chave)
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        # 1. Gerar um nome de arquivo único e seguro
        temp_filename = f"{uuid.uuid4().hex}.csv"
        file_path = os.path.join(TEMP_FOLDER, temp_filename)
        
        # 2. Salvar o DataFrame de resultados nesse arquivo
        resultado_final.to_csv(file_path, index=False)
        
        # 3. Salvar APENAS o nome do arquivo na sessão (é bem pequeno!)
        session['temp_filename'] = temp_filename
        # --- FIM DA MUDANÇA PRINCIPAL ---
        
        session['last_stats'] = stats
        salvar_historico(file.filename, stats)
        
        resultado_para_exibicao = resultado_final.copy()
        if not resultado_final.empty:
            resultado_para_exibicao['OS Digital'] = resultado_para_exibicao['OS Digital'].apply(criar_links)
        
        tabela_html = resultado_para_exibicao.to_html(
            classes="table table-striped table-hover", table_id="tabela-resultados",
            index=False, justify="left", border=0, escape=False
        )
        
        return render_template('resultado.html', 
                             table=tabela_html, 
                             has_results=not resultado_final.empty,
                             stats=stats,
                             palavras_utilizadas=palavras_chave)
        
    except Exception as e:
        # Adiciona um log do erro no terminal para depuração
        print(f"Ocorreu um erro: {e}")
        return redirect(url_for('index', error=f'Erro ao processar o arquivo: {str(e)}'))

@app.route('/download/excel')
def download_excel():
    # USA A NOVA FUNÇÃO
    df = get_dataframe_from_temp_file() 
    if df is None:
        return redirect(url_for('index', error="Os resultados expiraram. Por favor, processe o arquivo novamente."))
    
    stats = session.get('last_stats', {})
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tarefas Encontradas')
        stats_df = pd.DataFrame([
            ['Total de Registros', stats.get('total', 'N/A')],
            ['Tarefas Encontradas', stats.get('filtrados', 'N/A')],
            ['Taxa de Ocorrência (%)', stats.get('percentual', 'N/A')],
            ['Data de Geração', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ], columns=['Métrica', 'Valor'])
        stats_df.to_excel(writer, index=False, sheet_name='Estatísticas')
    
    output.seek(0)
    
    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=relatorio_filtrado.xlsx"}
    )

@app.route('/download/pdf')
def download_pdf():
    # USA A NOVA FUNÇÃO
    df = get_dataframe_from_temp_file()
    if df is None:
        return redirect(url_for('index', error="Os resultados expiraram. Por favor, processe o arquivo novamente."))
    
    stats = session.get('last_stats', {})
    palavras_utilizadas = session.get('custom_keywords', [])
    
    df_render = df.copy()
    if not df.empty:
        df_render['OS Digital'] = df_render['OS Digital'].apply(criar_links)

    tabela_html = df_render.to_html(index=False, escape=False, classes="tabela-pdf") if not df.empty else "<p>Nenhuma tarefa encontrada.</p>"
    
    # O HTML para o PDF continua o mesmo
    full_html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
          h1 {{ color: #0056b3; }}
          .header {{ padding: 20px; margin-bottom: 20px; border-radius: 5px; background-color: #f8f9fa; }}
          .stats {{ display: flex; justify-content: space-around; margin: 20px 0; background-color: #e9ecef; padding: 15px; border-radius: 5px; }}
          .stat-box {{ text-align: center; }}
          .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
          .palavras-chave {{ background-color: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #ffc107; }}
          .tabela-pdf {{ border-collapse: collapse; width: 100%; font-size: 10px; }}
          .tabela-pdf th, .tabela-pdf td {{ text-align: left; padding: 6px; border: 1px solid #ddd; }}
          .tabela-pdf th {{ background-color: #f2f2f2; }}
          a {{ color: #007bff; text-decoration: none; }}
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Relatório de Tarefas com Ação Necessária</h1>
          <p><strong>Gerado em:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
        </div>
        <div class="stats">
          <div class="stat-box"><div class="stat-number">{stats.get('total', 'N/A')}</div><div>Total de Registros</div></div>
          <div class="stat-box"><div class="stat-number">{stats.get('filtrados', 'N/A')}</div><div>Tarefas Encontradas</div></div>
          <div class="stat-box"><div class="stat-number">{stats.get('percentual', 'N/A')}%</div><div>Taxa de Ocorrência</div></div>
        </div>
        <div class="palavras-chave"><h3>Palavras-chave utilizadas:</h3><p>{', '.join(palavras_utilizadas)}</p></div>
        {tabela_html}
      </body>
    </html>
    """
    
    pdf = HTML(string=full_html).write_pdf()

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=relatorio_filtrado.pdf"}
    )

if __name__ == '__main__':
    app.run(debug=True)