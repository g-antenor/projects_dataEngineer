import subprocess
import time

## Verificando conexão com o banco de dados
def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
            if "accepting connections" in result.stdout:
                print("Conectado com sucesso ao Postgres")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Erro na conexão com o Postgres: {e}")
            retries += 1
            print(
                f"Tentando uma nova conexão em {delay_seconds} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay_seconds)
    print("Maximo de tentativas alcançadas")
    return False

## Validando se a conexão foi bem sucedida
if not wait_for_postgres(host="source_postgres"):
    exit(1)

## Proxima etapa, inicialização do ELT
print("Starting ELT script...")

## Configurando conexões com o DB
# Origem
source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'source_postgres'
}

# Destino
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'destination_postgres'
}

# Comandos
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
] 

# Automatizar autenticação para rodar o comando 
subprocess_env = dict(PGPASSWORD=source_config['password'])

subprocess.run(dump_command, env=subprocess_env, check=True)

load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql',
] 

subprocess_env = dict(PGPASSWORD=destination_config['password'])
subprocess.run(load_command, env=subprocess_env, check=True)


print('Fim do ELT script...')

