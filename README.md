# Simulador de Entregas por Drones

Este projeto simula a alocação de pedidos em drones seguindo regras de capacidade, alcance e prioridade, com o objetivo de minimizar o número de viagens.

---
## Como Executar

### 1. Executar o Simulador
Execute o comando no terminal:
```
python simulador_drones.py
```

O programa irá:
- Gerar pedidos de exemplo
- Alocar pedidos em viagens
- Distribuir viagens entre drones
- Exibir um resumo da alocação

---
## Como rodar os Testes Unitários

O projeto utiliza o módulo `unittest` da biblioteca padrão.

Para executar todos os testes:
```
python -m unittest discover tests
```

Ou executar somente o arquivo de testes:
```
python -m unittest tests/test_simulador.py
```

---
## O que os Testes Validam
- Cálculo de distância
- Cálculo de rota mínima estimada
- Alocação de pedidos em viagens
- Tratamento de erros para pedidos que excedem capacidade ou alcance

---
## Melhorias Futuras
- Entrada de pedidos
- Interface para visualização das rotas