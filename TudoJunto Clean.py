import os
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

data_limite = datetime(2024, 1, 31)  # Definir a data limite aqui

if datetime.now().date() > data_limite.date():
    messagebox.showinfo("Limite Expirado", "O período de uso deste programa expirou.")
    sys.exit()


def verificar_arquivo_svg_modelo():
    # Verificar se o arquivo SVG modelo existe
    if not os.path.exists('assrj.svg'):
        print("Arquivo SVG modelo não encontrado.")
        return False
    return True


def criar_diretorio_saida(output_dir):
    # Verificar se o diretório de saída existe, senão criar
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def substituir_campos_svg(nome, cargo, telefone1, telefone2):
    # Abrir o arquivo SVG modelo
    with open('assrj.svg', 'r') as svg_file:
        svg_content = svg_file.read()

    # Substituir os campos pelos novos valores no conteúdo do SVG
    svg_content = svg_content.replace('nomefuncionario', nome)
    svg_content = svg_content.replace('cargofuncionario', cargo)
    svg_content = svg_content.replace('telefone1', telefone1)
    svg_content = svg_content.replace('telefone2', telefone2)

    return svg_content


def gerar_arquivo_svg(nome, svg_content):
    # Salvar o conteúdo modificado em um novo arquivo SVG
    output_dir = 'out'
    criar_diretorio_saida(output_dir)
    svg_output_path = os.path.join(output_dir, f'{nome}.svg')

    with open(svg_output_path, 'w') as svg_file:
        svg_file.write(svg_content)

    # Exibir mensagem de sucesso
    print("Arquivo SVG gerado com sucesso.")


def salvar():
    # Obter os valores dos campos de entrada de texto
    novo_nome = nome_entry.get()
    novo_cargo = cargo_entry.get()
    novo_telefone1 = telefone1_entry.get()
    novo_telefone2 = telefone2_entry.get()

    # Verificar a data limite
    #    if verificar_data_limite():
    #        janela.quit()
    #        return

    # Verificar o arquivo SVG modelo
    if not verificar_arquivo_svg_modelo():
        janela.quit()
        return

    # Gerar o conteúdo do novo arquivo SVG
    svg_content = substituir_campos_svg(novo_nome, novo_cargo, novo_telefone1, novo_telefone2)

    # Gerar o arquivo SVG
    gerar_arquivo_svg(novo_nome, svg_content)

    # Fechar a janela
    janela.quit()


# Criar a janela
janela = tk.Tk()
janela.geometry('300x200')
janela.resizable(width=0, height=0)

# Criar os campos de entrada de texto
nome_label = tk.Label(janela, text='Nome:')
nome_entry = tk.Entry(janela, width=30)  # Aumentar o tamanho do campo Nome
cargo_label = tk.Label(janela, text='Cargo:')
cargo_entry = tk.Entry(janela, width=30)  # Aumentar o tamanho do campo Cargo
telefone1_label = tk.Label(janela, text='Telefone 1:')
telefone1_entry = tk.Entry(janela, width=20)  # Aumentar o tamanho do campo Telefone 1
telefone2_label = tk.Label(janela, text='Telefone 2:')
telefone2_entry = tk.Entry(janela, width=20)  # Aumentar o tamanho do campo Telefone 2

# Posicionar os componentes na janela
nome_label.grid(row=0, column=0)
nome_entry.grid(row=0, column=1)
cargo_label.grid(row=1, column=0)
cargo_entry.grid(row=1, column=1)
telefone1_label.grid(row=2, column=0)
telefone1_entry.grid(row=2, column=1)
telefone2_label.grid(row=3, column=0)
telefone2_entry.grid(row=3, column=1)

# Criar um botão para salvar as alterações
salvar_button = tk.Button(janela, text='Salvar', command=salvar)
salvar_button.grid(row=4, column=1)

# Caminhos possíveis para a instalação do Inkscape
inkscape_paths = [
    "C:\\Program Files\\Inkscape\\bin\\inkscape.exe",
    "C:\\Program Files\\Inkscape\\inkscape.exe",
    "C:\\Program Files (x86)\\Inkscape\\bin\\inkscape.exe",
    "C:\\Program Files (x86)\\Inkscape\\inkscape.exe"
]

# Encontrar o caminho válido para o Inkscape
inkscape_path = None
for path in inkscape_paths:
    if os.path.exists(path):
        inkscape_path = path
        break

if inkscape_path is None:
    print("Inkscape não encontrado. Abortando.")
    sys.exit()

# Iniciar o loop principal da janela
janela.mainloop()

valid_input_types = ["svg", "pdf", "eps", "emf", "wmf"]
valid_output_types = ["eps", "pdf", "png", "svg"]

source_type = "svg"  # Resposta padrão para a primeira pergunta
output_type = "png"  # Resposta padrão para a segunda pergunta
dpi = "96"  # Resposta padrão para a terceira pergunta

if source_type not in valid_input_types:
    print("Entrada inválida! Por favor, use um dos seguintes tipos de arquivo: ", valid_input_types)
    sys.exit()

if output_type not in valid_output_types:
    print("Entrada inválida! Por favor, use um dos seguintes tipos de arquivo: ", valid_output_types)
    sys.exit()

if source_type == output_type:
    print("Entrada e Saída são iguais. Não há nada para fazer. Saindo...")
    sys.exit()

# Contar quantos arquivos precisam ser convertidos
total = 0
for root, dirs, files in os.walk("."):
    for file in files:
        if file.lower().endswith("." + source_type):
            total += 1

print(f"Conversão iniciada. Serão processados {total} arquivo(s).\n")

count = 0
# Percorrer todos os arquivos encontrados com a extensão de origem definida
for root, dirs, files in os.walk("."):
    for file in files:
        if file.lower().endswith("." + source_type):
            count += 1
            out_folder = os.path.join(root, "out")
            os.makedirs(out_folder, exist_ok=True)

            print(
                f"{os.path.join(root, file)} -> {os.path.join(out_folder, os.path.splitext(file)[0] + '.' + output_type)} [{count}/{total}]")

            subprocess.run([
                inkscape_path,
                "--batch-process",
                f"--export-filename={os.path.join(out_folder, os.path.splitext(file)[0] + '.' + output_type)}",
                f"--export-dpi={dpi}",
                os.path.join(root, file)
            ])

print()
print(f"{count} arquivo(s) convertido(s) de {source_type} para {output_type}! (Salvo na pasta 'out')\n")
