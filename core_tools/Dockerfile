FROM ubuntu:jammy

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ="Europe/Madrid"

# Azure Credentials
ENV username=user
ENV password=pass

# https://dev.to/grigorkh/fix-tzdata-hangs-during-docker-image-build-4o9m
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update -y && apt install -y sudo dialog curl wget git libicu-dev vim \
    && sudo apt install -y software-properties-common && sudo add-apt-repository -y ppa:deadsnakes/ppa \
    && sudo apt update -y \
    && sudo apt install -y python3.9 \
    && sudo apt install -y python3.9-venv && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.9 get-pip.py && wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb \
    && sudo dpkg -i packages-microsoft-prod.deb \
    && sudo apt-get update && sudo apt-get -y install azure-functions-core-tools-4 \
    && echo '' >> requirements.txt \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
