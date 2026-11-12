import duckdb

class DuckDBManager:
    """
    Classe responsável por gerenciar a conexão em memória do DuckDB
    e carregar as extensões necessárias para leitura de arquivos no S3 e processamento espacial.
    """
    def __init__(self):
        # Inicializa a conexão com banco de dados em memória (fast processing)
        self.con = duckdb.connect(database=":memory:")
        self._setup_extensions()

    def _setup_extensions(self):
        """Instala e carrega as extensões de sistema de arquivos HTTP/S3 e Geometria Espacial."""
        self.con.install_extension('httpfs')
        self.con.load_extension('httpfs')
        self.con.install_extension('spatial')
        self.con.load_extension('spatial')

    def execute(self, query: str):
        """Executa uma instrução SQL genérica no DuckDB."""
        return self.con.execute(query)

    def query(self, query: str):
        """Executa uma consulta SQL e retorna o resultado em memória."""
        return self.con.query(query)