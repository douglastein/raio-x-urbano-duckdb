import yaml
import logging
from src.database import DuckDBManager
from src.pipeline import SpatialPipeline
from src.visualizer import SpatialVisualizer

def load_config(config_path: str = "config/settings.yaml") -> dict:
    """Carrega o arquivo de configuração YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():    
    config = load_config()
    
    #Inicializando uma conexão DuckDB
    db_manager = DuckDBManager()
    
    pipeline = SpatialPipeline(db_manager, config)
    total_records = pipeline.extract_and_filter()
    
    if total_records == 0:
        logging.warning("Nenhum registro encontrado para a bounding box informada. Verifique as coordenadas em settings.yaml.")
        return
        
    #Exportando dados processados
    pipeline.export_to_flatgeobuf()
    visualizer = SpatialVisualizer(
        fgb_path=config['output']['flatgeobuf_path'],
        html_output_path=config['output']['html_map_path']
    )
    visualizer.generate_3d_map()
    

if __name__ == "__main__":
    main()