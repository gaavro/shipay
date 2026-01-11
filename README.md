## 1. 

Serviço responsável por validar o cadastro de clientes utilizando CNPJ e CEP, comparando os endereços retornados por APIs externas.


1. Recebe CNPJ e CEP.
2. Consulta serviços externos:
   - API de CNPJ → dados da empresa (UF, cidade, logradouro, bairro).
   - API de CEP → dados de endereço.
     - BrasilAPI como serviço primário (com retry).
     - ViaCEP como fallback em caso de falha (com retry).
3. Normaliza os dados de endereço (UF, cidade e logradouro).
4. Compara os endereços obtidos.
5. Retorna:
   - HTTP 200 – endereços compatíveis.
   - HTTP 404 – endereços incompatíveis.
   - HTTP 503 – indisponibilidade de serviços externos.


- Retry com backoff exponencial e failover automático.
- Endpoint síncrono, com chamadas externas assíncronas.

---

## 2. 

Abordagem orientada a eventos, mantendo o fluxo principal desacoplado.

Após a execução de um lançamento, o serviço publica um evento de forma assíncrona contendo apenas os dados necessários para o relatório:

- customer_id
- trace_id
- timestamp
- status

Esse evento é enviado para uma fila ou broker de mensagens.  
Um worker independente consome esses eventos e persiste os dados em uma base exclusiva para relatórios.

Caso ocorra qualquer falha nesse processo, o erro fica isolado e não impacta o serviço de lançamentos.

- O fluxo crítico de lançamentos não é impactado.
- Falhas no relatório não afetam o endpoint principal.
- Banco de dados separado e otimizado para leitura.
- Arquitetura desacoplada e de fácil manutenção.

---

## 3.

### Testes de Integração

Validar a integração real entre API, Redis, processo de polling e Kafka.

Cenários testados:

- Persistência do evento no banco chave/valor.
- Identificação de eventos vencidos pelo worker de scheduler.
- Publicação correta dos eventos no tópico Kafka.
- Remoção do evento do banco após publicação.
- Reagendamento em caso de falha.

---

### Testes de Performance (Load Tests)

Garantir o SLA do serviço: 1.000 RPS com P99 ≤ 30ms no endpoint principal.

---

### Testes de Stress

Avaliar o comportamento do sistema sob carga acima do esperado.

Cenários simulados:

- Alto volume de eventos agendados.
- Redis sob pressão.
- Pico de requisições simultâneas.

Monitoramento:

- Uso de CPU
- Consumo de memória

---

### Testes de Resiliência

Garantir que falhas de infraestrutura não impactem o fluxo principal.

Cenários simulados:

- Redis temporariamente indisponível.
- Kafka indisponível.
- Interrupção do processo de polling.

Ferramenta:

- Toxiproxy

---

## 4. 

- Repository contendo regras de negócio.
- Service acessando SQL diretamente.
- Middleware retornando stack trace para o cliente.
- CORS liberado para qualquer origem (*).
- Uso de funções async sem await.
- Uso de f-string em SQL, permitindo SQL Injection.
- Classes de tools com múltiplas responsabilidades (HTTP, banco, autorização e validação).

---

## 6. 

Para integração com serviços externos, utilizaria:

- Facade: concentra a complexidade das integrações em um único ponto, expondo uma interface simples para o restante da aplicação.
- Adapter: padroniza o acesso a diferentes fornecedores, facilitando a troca ou inclusão de novos serviços sem impactar o domínio.

---

## 7.

- Regras de negócio e validações concentradas nos endpoints.
- Uso excessivo de try/except Exception.
- Status HTTP inadequados para alguns cenários de regra de negócio.
- Conexão com Redis criada a cada requisição no scheduler.
- Tabela users armazenando senha em texto puro.
