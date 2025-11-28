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
## Como Rodar os Testes Unitários

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
## O Que os Testes Validam
- Cálculo de distância
- Cálculo de rota mínima estimada
- Alocação de pedidos em viagens
- Tratamento de erros para pedidos que excedem capacidade ou alcance

---
## Melhorias Futuras
- Algoritmos de roteamento mais eficientes (Clarke-Wright, 2-opt, simulated annealing)
- Entrada de pedidos via JSON ou CSV
- Sistema de relatório e métricas
- Interface gráfica para visualização das rotas

---
## Licença
Este projeto pode ser utilizado livremente para fins acadêmicos e de prototipação.