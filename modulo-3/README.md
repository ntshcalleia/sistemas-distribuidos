# Laboratório 3 - Aplicação cliente/servidor multitarefa

## Descrição do trabalho
Aplicação distribuída que conta a frequência de palavras em arquivos texto.

**Entrada:** nome do arquivo texto, que deverá estar localizado no servidor

**Saída:** lista com 10 palavras mais frequentemente usadas no arquivo, ordenada da mais frequente para a menos frequente, assim como o número de ocorrências de cada palavra.

A aplicação é uma aplicação distribuída baseada em arquitetura de sistema cliente/servidor com dois níveis:
- O lado do cliente implementa a camada de interface com o usuário, que pode solicitar o processamento de vários arquivos em uma única execução da aplicação
- O servidor implementa as camadas de processamento e de acesso aos dados.

## Instruções de uso
O cliente está localizado unicamente no arquivo `client.py`, enquanto que os demais arquivos pertencem ao servidor.
### Servidor
#### Inicializando o servidor
Você pode inicializar o servidor com a seguinte chamada:
```bash
python3 server.py
```
O host e porta padrões são localhost e 5000, mas podem ser alterados usando as flags `--HOST` e `--PORT`:
```bash
python3 server.py --PORT 5001 --HOST '192.168.0.5'
```
#### Banco de dados
A aplicação busca por arquivos salvos na pasta `database` do servidor, mas caso ele esteja localizado em outra pasta você pode consultá-lo indicando o diretório do mesmo na chamada.
O servidor irá inicialmente consultar `cache.json`, pois caso o arquivo desejado já tenha sido consultado o resultado estará armazenado no mesmo. Se for a primeira consulta o servidor irá processar o arquivo e registrar as informações no arquivo cache.
- **E se o documento tiver sido alterado desde a última consulta?**
  Para saber se o documento foi alterado desde a última consulta nós usamos a função `getmtime` do módulo `os`, que registra a data e horário em que foi realizada a última modificação ao arquivo. Se o documento tiver sido alterado descartamos o resultado anterior e processamos o arquivo novamente. Estrutura do arquivo `cache.json`:
```
{
	"example1.txt": {
		"result": [["hello", 3], ["world", 3], ...],
		"mtime": 1599616785.3462708
	}, "example2.txt": {
		...
	},
	...
}
```

### Cliente
#### Solicitando um arquivo
```bash
python3 client.py nome-do-arquivo.txt
```
#### Solicitando múltiplos arquivos em uma só chamada
Você também pode passar uma lista de arquivos para solicitar vários documentos em uma única chamada. O nome dos arquivos deve ser separado por um espaço:
```bash
python3 client.py nome-do-arquivo-1.txt nome-do-arquivo-2.txt nome-do-arquivo-3.txt
```
#### Modo interativo
Para inicializar a aplicação no modo interativo basta usar a flag `-i`. O modo interativo permite que você continue consultando arquivos até desejar encerrar a aplicação:
```
python3 client.py -i
Enter filename(s):
nome-do-arquivo.txt
```
```
Enter filename(s):
nome-do-arquivo-1.txt nome-do-arquivo-2.txt nome-do-arquivo-3.txt
```
Você pode encerrar o modo interativo com o comando `/exit`:
```
Enter filename(s):
/exit
```