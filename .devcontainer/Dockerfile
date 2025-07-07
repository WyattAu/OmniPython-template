# syntax=docker/dockerfile:1.4
FROM bitnami/python:3.13-debian-12

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System packages and user configuration
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN install_packages --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    procps \
    less \
    iproute2 \
    sudo \
    ssh \
    libssl-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    libopenblas-dev \
    ffmpeg \
    zsh \
    fonts-powerline \
    && mkdir /workspace \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m --shell /usr/bin/zsh $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown $USERNAME:$USERNAME /workspace \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# User environment setup
USER $USERNAME
ENV PATH="/home/$USERNAME/.local/bin:${PATH}"
WORKDIR /workspace

# Oh My Zsh and Powerlevel10k configuration
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k \
    && { \
    echo 'export TERM="xterm-256color"'; \
    echo 'ZSH_THEME="powerlevel10k/powerlevel10k"'; \
    echo 'plugins=(git python pip docker docker-compose gh debian common-aliases virtualenv poetry pyenv)'; \
    echo 'POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true'; \
    echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh'; \
    } >> ~/.zshrc

#RUN poetry config virtualenvs.in-project true

# Python tooling installation
RUN python -m pip install --user --upgrade pip setuptools wheel \
    && python -m pip install --user pipx \
    && python -m pipx ensurepath \
    && pipx install pdm \
    && pipx install poetry \
    && pipx install black \
    && pipx install ruff \
    && pipx install mypy \
    && pipx install pytest \
    && pipx install pre-commit \
    && pipx install debugpy
#    && pipx install pipenv

ENV SHELL=/bin/zsh
