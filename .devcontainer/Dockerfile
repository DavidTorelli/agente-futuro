FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

# Instalación de herramientas necesarias
RUN apt-get update && apt-get install -y \
    git \
    curl \
    zsh \
    vim \
    sudo \
    passwd \
    file \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    bash \
    python3-dev \
    pre-commit \
    tesseract-ocr tesseract-ocr-eng \
    libgl1 libglib2.0-0

# --- Añadir Node.js + npm + herramientas JS ---
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest && \
    npm install -g reveal-md @redocly/openapi-cli swagger-ui-watcher
    
RUN  apt-get clean && rm -rf /var/lib/apt/lists/*

# Create user no root
RUN useradd -m -s /bin/zsh vscode && chown -R vscode:vscode /home/vscode

# Switch to user
USER vscode
WORKDIR /home/vscode

# Instalar Oh My Zsh y Powerlevel10k como usuario vscode
RUN git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh && \
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k && \
    sed -i 's|ZSH_THEME="robbyrussell"|ZSH_THEME="powerlevel10k/powerlevel10k"|' ~/.zshrc && \
    echo '\n[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh' >> ~/.zshrc && \
    echo 'exec zsh' >> ~/.bashrc && \
    echo '\nexport PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Añadir configuración de Powerlevel10k (después de haber creado ~/.zshrc)
COPY --chown=vscode:vscode .devcontainer/.p10k.zsh /home/vscode/.p10k.zsh

# Workspace final
WORKDIR /workspace/ai-solver
CMD ["sleep", "infinity"]
