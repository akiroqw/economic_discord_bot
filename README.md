# Akiro DiscordBot

## Introduction

A project in which an economic bot was developed specifically for your discord server. It contains various functions for building an economy on your server.

![Introduction](https://i.pinimg.com/originals/74/5c/c9/745cc90fcc688569610f84bc5d2b2fd6.gif)"

## Technologies were used in this project:

* [Python] (https://www.python.org /): a simple syntactic programming language;
* [SQLite] (https://sqlite.org/index.html ): SQLite is a software library that provides a relational database management system. It is a serverless, self-contained SQL database engine with zero configuration and transactions. SQLite is widely used in various applications due to its compact size, low maintenance costs and ease of use;
* [Discord Developer Portal] (https://discord.com/developers/applications ): website for registering your application;
* [Discord.py ] (https://discord py.readthedocs.io/en/latest /): library for integration with discord;

## Requirement

* To have Python version 3.11.3 installed (during development we started with version 3.11.3, so we cannot guarantee that earlier versions will work);
* Create a .env file, fill it with the following data:

```py
TOKEN = "" Bot Token
NAME = "" Bot Name
ID = "" Client ID(App)
PREFIX = "!" Prefix (To call the command)
```
* or we can change the config file and enter this data here:

```py
setting = {
    'TOKEN' : "",
    'NAME BOT' : "",
    'ID'       : "",
    'PREFIX'   : ""
}
```

## GAMIFICAÇÃO

A gamificação do bot é feita através de 2 tipos, a xp e níveis, o xp é dividido em semanal e por canal, os níveis são calculados de forma geral;

### XP

O cálculo do xp vai seguir essas regras:
* Por mensagem:
  * Mínimo de 2 palavras;
  * Máximo por mensagem, 40 pontos;
  * Número de caracteres não repetidos / 3;
* Reações a mensagens:
  * Disponíveis em alguns canais;
  * Badlist de emojis, remove pontos, 200 pontos, remove a reação;
  * Goodlist de emojis, 5 emojis, 2x pontos, 100 pontos base;
* Tempo de canais de voz:
  * Conferir quais informações recebemos para avaliar os pontos
* Compartilhamento de tela:
  * Conferir quais informações recebemos para avaliar os pontos


#### pymongo operações

Essas informações que estão sendo mostradas é apenas para enteder como deve ser utilizado o pymongo

* **Insert**
```py
data = {
  'nome': 'Jef',
  'idade': 45
}

responseData = collection.insert_one(data)
# responseData é do tipo InsertOneResult, só vi que tem o inserted_id até agora
```
[Infos sobre InsertOneResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.InsertOneResult)

* **Replace**
```py
data = {
  'nome': 'Jef',
  'idade': 45
}

responseData = collection.replace_one({'nome': 'Mateus'}, data)
# responseData é do tipo UpdateResult, só vi que tem matched_count,modified_count e upserted_id de informações relevantes
```
[Infos sobre UpdateResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult)

* **Update**
```py

responseData = collection.update_one({'nome': 'Mateus'}, {'$inc': {'idade': 2}}, upsert)
# responseData é do tipo UpdateResult, só vi que tem matched_count,modified_count e upserted_id de informações relevantes
# incrementa o valor idade em 2
# upsert é um valor booleano, que vai definir se é necessário inserir o objeto ou não
```
[Infos sobre UpdateResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult)
* Outros operadores interessantes:
  * $set: vai definir um valor específico
  * $mul: vai múltiplicar a propriedade pelo valor especificado
  * $rename: vai trocar o campo
  * $setOnInsert: se a query não resultar em nada, e o objeto tiver que ser inserido, adiciona os campos
  * $unset: remove o campo
* Para arrays:
  * $: atualiza o primeiro que encontrar na condição
  * $[]: atualiza todos os elementos encontrados
  * $[\<identifiers\>]: atualiza todos que combinarem com a condição dentro do parênteses

[Infos sobre Update Operators](https://docs.mongodb.com/manual/reference/operator/update/#std-label-update-operators)


* **update_many**
```py
responseData = collection.update_many(
    {'valor': 10}, {'$set': {'teste2':'novo'}})
# procura todo lugar onde valor é igual a 10, e altera/adiciona o campo teste2 = novo
```
[Infos sobre UpdateResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult)

