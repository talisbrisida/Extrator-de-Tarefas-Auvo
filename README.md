Extrator de Tarefas Auvo.

Uma aplicação web simples construída com Flask para analisar relatórios de tarefas exportados do sistema Auvo em formato .csv. A ferramenta filtra as tarefas que contêm palavras-chave específicas (como "quebrado", "trocar peça", etc.) e exibe os resultados de forma organizada, com estatísticas e opções de download.

📸 Screenshot
Dica: Tire um print da sua tela de resultados e adicione aqui! Um bom screenshot ajuda muito a entender o projeto rapidamente.

✨ Funcionalidades Principais
Upload de Arquivos: Envio de relatórios de tarefas no formato .csv.

Filtragem por Palavras-chave: Filtra as linhas do relatório com base em uma lista de palavras-chave customizáveis.

Visualização Interativa: Exibe os resultados em uma tabela com busca dinâmica.

Painel de Estatísticas: Apresenta um resumo dos dados, incluindo total de registros, tarefas encontradas e taxa de ocorrência.

Exportação de Relatórios: Permite o download dos resultados filtrados nos formatos .xlsx (Excel) e .pdf.

Configuração Flexível: Uma página dedicada para alterar as palavras-chave usadas na busca.

Histórico de Processamentos: Guarda um histórico dos últimos 10 arquivos analisados durante a sessão.

🛠️ Tecnologias Utilizadas
Backend: Python 3, Flask

Manipulação de Dados: Pandas

Geração de PDF: WeasyPrint

Frontend: HTML5, CSS3, Bootstrap 5, JavaScript

🚀 Instalação e Execução
Siga os passos abaixo para executar o projeto em seu ambiente local.

Pré-requisitos
Python 3.10+

pip (gerenciador de pacotes do Python)

git (para clonar o repositório)

Passos
Clone o repositório:

git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd meu_extrator

Crie e ative um ambiente virtual:

# Criar o ambiente
python -m venv venv

# Ativar no Windows (Prompt de Comando)
.\venv\Scripts\activate

# Ativar no Linux ou macOS
source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Configure as variáveis de ambiente:

Crie um arquivo chamado .env na raiz do projeto.

Adicione a seguinte linha a ele:

SECRET_KEY='SUA_CHAVE_SECRETA_SUPER_SEGURA_AQUI'

Para gerar uma chave segura, use o terminal do Python:

import secrets; secrets.token_hex(32)

Crie a pasta de arquivos temporários:

Na raiz do projeto, crie uma pasta chamada temp.

Executando a Aplicação
Com o ambiente virtual ativado, execute o seguinte comando:

python app.py

Abra seu navegador e acesse: http://127.0.0.1:5000

📝 Uso
Acesse a aplicação pelo navegador.

(Opcional) Vá para a página de Configurações para ajustar as palavras-chave que serão usadas na busca.

Na página inicial, clique em "Selecionar arquivo" e escolha o seu relatório .csv exportado do Auvo.

Clique em "Processar Relatório".

Visualize os resultados na tabela, utilize a busca para filtrar e, se desejar, faça o download em Excel ou PDF.
