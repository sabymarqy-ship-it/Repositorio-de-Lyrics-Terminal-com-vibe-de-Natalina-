# ❄️ Natal Lyrics Sync - Terminal Edition

Um script Python criativo que traz o clima natalino para o terminal! Ele sincroniza a letra da música ** Vibe Natalina** com um efeito visual de neve caindo, simulando a interface de letras do Spotify.

## 🚀 Funcionalidades

* **Sincronização em Tempo Real:** As letras mudam conforme o tempo exato da música.
* **Efeito de Neve:** Partículas de neve dinâmicas que caem ao fundo enquanto a letra é exibida.
* **Interface Estilizada:** Utiliza códigos ANSI para cores pastel e negritos diretamente no terminal.
* **Layout Responsivo:** Detecta o tamanho da sua janela de terminal para ajustar a renderização.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Bibliotecas nativas:** `time`, `sys`, `os`, `random` (não precisa instalar nada via pip!).

## 📖 Como Funciona

O código utiliza **Sequências de Escape ANSI** para controlar o cursor do terminal. Em vez de imprimir uma linha após a outra, o script:
1. Limpa a tela.
2. Move o cursor para posições específicas para desenhar a neve.
3. Reposiciona o cursor para escrever o título e a letra no centro/esquerda.
4. Repete esse ciclo a cada 0.08 segundos para criar o efeito de animação.

## 💻 Como Rodar

1. Certifique-se de ter o Python instalado.
2. Salve o código em um arquivo chamado `nome_do_arquivo.py`.
3. Abra o terminal na pasta do arquivo e execute:
   ```bash
   python nome_do_arquivo.py
