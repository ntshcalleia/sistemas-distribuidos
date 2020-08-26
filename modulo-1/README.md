# Laboratório 1 - Introdução à programação com sockets

## Descrição do trabalho
Servidor de *echo* que envia de volta para o emissor a mensagem recebida. O servidor, ou receptor, está no arquivo `server.py`, enquanto que o emissor, ou o lado ativo, está localizado no arquivo `client.py`.

## Instruções de uso
### Inicializando o servidor
Comece ativando o lado passivo para poder receber conexões. Use o seguinte comando para inicializar o servidor:
```bash
python3 server.py
```
O host e porta padrões são localhost e 5000, mas podem ser alterados usando os argumentos --HOST e --PORT:
```bash
python3 server.py --PORT 5001 --HOST '192.168.0.5'
```

### Inicializando o cliente
Agora que o servidor está escutando você pode se conectar à ele com o script `client.py`:
```bash
python3 client.py
```
Caso o servidor esteja em outra máquina e/ou você tenha alterado as configurações você também precisa alterá-las também no lado do cliente:
```bash
python3 client.py --PORT 5001 --HOST '192.168.0.5'
```

### Enviando mensagens
Com o programa ativo rodando, digite sua mensagem e pressione ENTER para enviá-la:
```
Type your message:
Olá, mundo!
```

### Interrompendo a conexão
A conexão pode ser encerrada a qualquer momento usando o comando `/close`:
```
Type your message:
/close
```