
#  Raio-X Urbano de Vitória-ES: Análise Espacial de Edificações com DuckDB & Kepler.gl

Este projeto aplica conceitos de **Engenharia de Software** e **Big Data Espacial** para processar, filtrar e analisar dados massivos de edificações capixabas (provenientes do Open Buildings / AWS S3) em altíssima velocidade, utilizando **DuckDB Spatial** em arquitetura modular e gerando visualizações urbanas 3D interativas.

---

## Destaques do Projeto

- **Processamento em Streaming na Nuvem:** Leitura direta de arquivos GeoParquet particionados na AWS S3 através do DuckDB, sem a necessidade de baixar gigabytes de dados localmente.
- **Arquitetura Limpa:** Separação clara de responsabilidades dividida entre gerência de banco, pipeline de dados, visualização e configurações externas (`settings.yaml`).
- **Classificação Urbana:** Categorização das construções por porte (compactas, médias e grandes complexos) baseada na área em metros quadrados.
- **Visualização 3D:** Geração de mapas interativos via Kepler.gl para análise.

---

## Arquitetura do Repositório

```text
raio_x_urbano_duckdb/
├── config/
│   └── settings.yaml          # Parâmetros globais, S3 e Bounding Box geográfica
├── data/
│   └── output/                # Saídas geradas (FlatGeobuf .fgb e Mapa HTML)
├── src/
│   ├── __init__.py
│   ├── database.py            # Gerenciador de conexão in-memory e extensões DuckDB
│   ├── pipeline.py            # Extração streaming, filtros espaciais e classificação
│   └── visualizer.py          # Renderizador de mapas 3D interativos (Kepler.gl)
├── main.py                    # Ponto de entrada principal da aplicação
├── requirements.txt           # Dependências e bibliotecas do projeto
└── .gitignore                 # Arquivos ignorados
```
## Tecnologias Utilizadas

- **Python 3.14.3**
- **DuckDB & DuckDB Spatial Extension:** Processamento analítico e computação espacial.
- **GeoPandas & PyArrow:** Manipulação e leitura de dados geoespaciais.
- **Kepler.gl:** Visualização cartográfica web em 3D.
- **FlatGeobuf (.fgb):** Formato binário espacial de alta performance.
- **PyYAML:** Gestão de configurações desacopladas.

---

## Como Executar o Projeto Localmente

Siga os passos abaixo para configurar o ambiente e rodar o pipeline no seu computador:

### 1. Clonar o Repositório

```bash
git clone https://github.com/douglastein/raio-x-urbano-duckdb.git
cd raio-x-urbano-duckdb
```

### 2. Criar e Ativar o Ambiente Virtual

**No Windows (CMD / PowerShell):**

```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar a Região de Interesse (Opcional)

Abra o arquivo `config/settings.yaml` e ajuste as coordenadas da bbox (Bounding Box) caso queira analisar outra cidade ou região do Brasil:

```yaml
bbox:
  xmin: -40.35
  ymin: -20.35
  xmax: -40.25
  ymax: -20.25
```

### 5. Executar a Pipeline

```bash
python main.py
```

O script irá conectar no S3, filtrar os dados da região configurada, exportar o arquivo otimizado para `data/output/edificacoes_vitoria.fgb` e compilar o mapa interativo.

---

## Visualização do Resultado

Após a execução bem-sucedida, abra o arquivo gerado no seu navegador:

```text
data/output/mapa_3d_urbano.html
```

Você verá uma maquete 3D interativa das edificações urbanas segmentadas por cores.



## Autor

Desenvolvido por Douglas Stein Sabino.

Se tiver dúvidas ou sugestões, sinta-se à vontade para conectar comigo no [LinkedIn](www.linkedin.com/in/douglas-s-02a221121).

---
