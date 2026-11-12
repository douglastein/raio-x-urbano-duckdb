import os
import logging
from src.database import DuckDBManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SpatialPipeline:
    """
    Pipeline de engenharia de dados espacial para consultar o GeoParquet no S3,
    aplicar filtros espaciais e classificar o porte das edificações via DuckDB.
    """
    def __init__(self, db_manager: DuckDBManager, config: dict):
        self.db = db_manager
        self.config = config

    def extract_and_filter(self):
        s3_url = f"{self.config['s3_prefix']}/by_country_s2/country_iso={self.config['country_iso']}/*.parquet"
        bbox = self.config['bbox']
        
        logging.info("Iniciando consulta espacial streaming do S3 e classificação urbana via DuckDB...")
        
        query = f"""
            CREATE OR REPLACE TABLE brasil_buildings_filtered AS
            SELECT 
                boundary_id,
                bf_source,
                confidence,
                area_in_meters,
                CASE 
                    WHEN area_in_meters < 50 THEN '1. Compacta (< 50m²)'
                    WHEN area_in_meters BETWEEN 50 AND 200 THEN '2. Média (50-200m²)'
                    ELSE '3. Grande/Industrial (> 200m²)'
                END AS categoria_tamanho,
                geometry
            FROM parquet_scan('{s3_url}')
            WHERE bbox.xmin >= {bbox['xmin']} AND bbox.xmax <= {bbox['xmax']}
              AND bbox.ymin >= {bbox['ymin']} AND bbox.ymax <= {bbox['ymax']};
        """
        self.db.execute(query)
        
        count = self.db.execute("SELECT COUNT(*) FROM brasil_buildings_filtered").fetchone()[0]
        return count

    def export_to_flatgeobuf(self):
        output_file = self.config['output']['flatgeobuf_path']
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        logging.info(f"Exportando resultados para formato FlatGeobuf em '{output_file}'...")
        self.db.execute("SET geometry_always_xy = true;")
        
        export_query = f"""
            COPY (
                SELECT boundary_id, bf_source, confidence, area_in_meters, categoria_tamanho, geometry 
                FROM brasil_buildings_filtered
            ) TO '{output_file}' WITH (FORMAT GDAL, DRIVER 'FlatGeobuf');
        """
        self.db.execute(export_query)
        logging.info("Exportação finalizada com sucesso!")