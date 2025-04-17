FROM ubuntu:22.04
LABEL maintainer="Cloned from Bitbucket Pipelines <pipelines-feedback@atlassian.com>"

# Args
ARG BUILD_DATE
ARG REVISION
ARG BUILD_VERSION
ARG DEBIAN_FRONTEND=noninteractive

# Labels
LABEL \
    org.opencontainers.image.authors="USP" \
    org.opencontainers.image.created=$BUILD_DATE \
    org.opencontainers.image.title="usp/default-image" \
    org.opencontainers.image.description="Cloned from default image for Bitbucket Pipelines" \
    org.opencontainers.image.revision=$REVISION \
    org.opencontainers.image.version=$BUILD_VERSION

# Install base dependencies
RUN apt-get update \
    && apt-get install -y \
       software-properties-common \
    && add-apt-repository ppa:git-core/ppa -y \
    && apt-get install -y \
       autoconf \
       build-essential \
       ca-certificates \
       pkg-config \
       wget \
       xvfb \
       curl \
       git \
       ant \
       ssh-client \
       unzip \
       iputils-ping \
       zip \
       jq \
       gettext-base \
       tar \
       parallel \
       default-jre \
       python3-setuptools \
       python3-pip \
    && curl -L "https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip \
    && curl -LO https://releases.hashicorp.com/terraform/1.5.6/terraform_1.5.6_linux_amd64.zip \
    && unzip terraform_1.5.6_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_1.5.6_linux_amd64.zip \
    && ln -s /usr/bin/python3.10 /usr/bin/python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Test Docker Compose install
RUN docker-compose --version

# Install nvm with node and npm
ENV NODE_VERSION=18.16.1 \
    NVM_DIR=/root/.nvm \
    NVM_VERSION=0.39.2 \
    NVM_SHA256=c1e672cd63737cd3e166ad43dffcb630a3bea07484705eae303c4b6c3e42252a

RUN curl https://raw.githubusercontent.com/nvm-sh/nvm/v$NVM_VERSION/install.sh -o install_nvm.sh \
    && echo "${NVM_SHA256} install_nvm.sh" | sha256sum -c - \
    && bash install_nvm.sh \
    && rm -rf install_nvm.sh \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# Set node path
ENV NODE_PATH=$NVM_DIR/v$NODE_VERSION/lib/node_modules

# Default to UTF-8 file.encoding
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    LANGUAGE=C.UTF-8

# Xvfb provide an in-memory X-session for tests that require a GUI
ENV DISPLAY=:99

# Set the path.
ENV PATH=$NVM_DIR:$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Create dirs and users
RUN mkdir -p /opt/atlassian/bitbucketci/agent/build \
    && sed -i '/[ -z \"PS1\" ] && return/a\\ncase $- in\n*i*) ;;\n*) return;;\nesac' /root/.bashrc \
    && useradd --create-home --shell /bin/bash --uid 1000 pipelines

WORKDIR /opt/atlassian/bitbucketci/agent/build
ENTRYPOINT ["/bin/bash"]
