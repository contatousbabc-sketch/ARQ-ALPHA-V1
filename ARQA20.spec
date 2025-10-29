# -*- mode: python ; coding: utf-8 -*-
# ARQA2 - PyInstaller Spec File

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Caminho para o diretório do prophet (ajuste se o seu ambiente Python estiver em outro lugar)
# Isso tenta encontrar o local do pacote prophet no ambiente de execução do script spec
import prophet
prophet_dir = os.path.dirname(prophet.__file__)
# Certifique-se de que prophet_dir está correto
print(f"Diretório do Prophet detectado: {prophet_dir}")

# Coleta dados de pacotes importantes
spacy_data = collect_data_files('spacy')
flask_data = collect_data_files('flask')

# Adicione o diretório do prophet como uma tupla (caminho_origem, destino_no_executavel)
# O destino 'prophet' significa que ele será colocado dentro de _internal/prophet
prophet_data = [(prophet_dir, 'prophet')]

# --- ADICIONE/ATUALIZE ESTAS LINHAS NO SEU ARQA2.spec ---
# Caminho real onde o Playwright instalou os navegadores
browsers_path = os.path.join(os.environ['LOCALAPPDATA'], 'ms-playwright')
# Certifique-se de que browsers_path está correto e que os navegadores estejam instalados
print(f"Diretório dos navegadores do Playwright: {browsers_path}")
if not os.path.exists(browsers_path):
    print(f"AVISO: Diretório de navegadores do Playwright não encontrado: {browsers_path}")
    print("Execute 'playwright install' antes de rodar o PyInstaller.")
else:
    print("Navegadores do Playwright encontrados. Incluindo no pacote...")
# Adiciona os navegadores ao pacote, copiando para 'playwright/driver/package/.local-browsers' dentro do executável
playwright_browsers_data = [(browsers_path, 'playwright/driver/package/.local-browsers')]
# --- FIM DA ADIÇÃO/ATUALIZAÇÃO ---

# Hidden imports críticos (mantenha sua lista existente, talvez adicione 'prophet' também se necessário)
hidden_imports = [
    'flask', 'flask_cors', 'flask_socketio',
    'werkzeug', 'jinja2', 'markupsafe',
    'requests', 'urllib3', 'certifi',
    'pandas', 'numpy', 'scipy',
    'PIL', 'PIL.Image',
    'selenium', 'selenium.webdriver',
    'beautifulsoup4', 'bs4',
    'lxml', 'lxml.etree',
    'spacy', 'spacy.cli',
    'openai', 'anthropic',
    'google.generativeai', 'groq',
    'yaml', 'pyyaml',
    'dotenv', 'python-dotenv',
    'aiohttp', 'aiofiles', 'asyncio',
    'supabase', 'postgrest',
    'PyPDF2', 'reportlab', 'openpyxl',
    'matplotlib', 'seaborn', 'plotly',
    'nltk', 'textblob', 'vaderSentiment',
    'sklearn', 'scikit-learn',
    'cv2', 'pytesseract',
    'webdriver_manager',
    # Adicione 'prophet' aqui também
    'prophet',
    # Adicione outros módulos que podem ser importados dinamicamente ou não detectados automaticamente
    # Exemplos baseados no warn-ARQA2.txt e estrutura do projeto:
    'services',
    'routes',
    'engine',
    'utils',
    'ubie',
    'ubie.agent',
    'ubie.services',
    'ubie.config',
    'database',
    'external_ai_verifier', # Adicione esta linha para reconhecer a pasta como pacote
    'external_ai_verifier.src', # Adicione esta linha para reconhecer a subpasta como pacote
    'external_ai_verifier.src.external_review_agent', # Adicione esta linha para o módulo específico
    # Se os módulos abaixo forem importados dinamicamente, adicione-os:
    # 'services.groq_client', # Exemplo de módulo mencionado no warn como 'missing'
    # 'config_checker',
    # 'external_review_agent', # Este módulo parece opcional ou ausente no momento - REMOVA esta linha se existir
    # 'auto_save_manager',
]

a = Analysis(
    ['src\\run.py'],
    pathex=[],
    binaries=[],
    # Corrigindo a inclusão de dados
    # Copia src/templates para _internal/templates (onde Flask espera por padrão)
    # Copia src/static para _internal/static (onde Flask espera por padrão)
    # Copia .env para a pasta do executável
    # Copia external_ai_verifier para a pasta do executável
    # Copia o arquivo .whl do spacy para ser instalado em tempo de execução se necessário
    # Copia os navegadores do playwright
    datas=[
        ('src/templates', 'templates'), # Importante: Copia a pasta templates para o local padrão do Flask
        ('src/static', 'static'),      # Importante: Copia a pasta static para o local padrão do Flask
        ('.env', '.'),                 # Copia .env para a pasta ARQA2 em dist
        ('external_ai_verifier', 'external_ai_verifier'), # Copia pasta para dist/ARQA2/
        # Exemplo de inclusão de um arquivo específico (como o .whl do spacy)
        ('src/engine/pt_core_news_sm-3.8.0-py3-none-any.whl', 'engine'), # Copia .whl para dist/ARQA2/engine/
        # Inclua outros arquivos de dados necessários aqui, por exemplo:
        # ('src/relatorios_intermediarios', 'relatorios_intermediarios'),
        # ('src/analyses_data', 'analyses_data'), # Cuidado com dados que são escritos em tempo de execução
        # ('src/downloaded_images', 'downloaded_images'), # Cuidado com dados que são escritos em tempo de execução
        # ('src/screenshots', 'screenshots'), # Cuidado com dados que são escritos em tempo de execução
        # ('src/viral_data', 'viral_data'), # Cuidado com dados que são escritos em tempo de execução
        # ('src/viral_images_data', 'viral_images_data'), # Cuidado com dados que são escritos em tempo de execução
    ] + spacy_data + flask_data + prophet_data + playwright_browsers_data, # Adicione '+ playwright_browsers_data' aqui
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib.tests', 'numpy.tests'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ARQA2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Mantenha como True ou False conforme sua necessidade
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None, # Adicione um caminho para um ícone .ico se desejar
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ARQA2',
)