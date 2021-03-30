# Create Alarms Cloudwatch

Este repositório contém uma aplicação que cria os alertas no cloudwatch para as instancias que estão rodando


## Sumário

- [Requerimentos](#requerimentos)
    - [Sistema](#sistema)
    - [Desenvolvimento](#desenvolvimento)
- [Setup](#setup)
    - [Dependências](#dependências)
- [Uso](#uso)
    - [Execução](#execução)

## Requerimentos

### Sistema

- [AWS Lambda]()
- [AWS Cloudwatch]()
- [AWS Cloudformation]()
- [Amazon SNS]()

### Desenvolvimento

- [AWS SAM]()
- [Python]()

## Setup

### Dependências 

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

## Uso

### Execução

- Clonar esse repositório na sua maquina:
```bash
git clone https://github.com/matusalem-santos/create-alarms-cloudwatch.git
```
- Entrar no repositóro clonado: 
```bash
    cd create-alarms-cloudwatch
``` 

- Buildar o aplicativo:
```bash
    sam build
``` 

- Realizar o deploy do aplicativo:
```bash
    sam deploy --guided
``` 

##### OBS
- Validar se o AWS CLI está configurado com as credenciais da sua conta na AWS
- Verificar se as credenciais tem permissão para criar todos os serviços dessa stack

