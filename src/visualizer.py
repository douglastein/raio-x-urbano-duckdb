import os
import logging
import geopandas as gpd
from keplergl import KeplerGl

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SpatialVisualizer:
    """
    Módulo responsável por gerar o mapa 3D no Kepler.gl
    """
    def __init__(self, fgb_path: str, html_output_path: str):
        self.fgb_path = fgb_path
        self.html_output_path = html_output_path

    def generate_3d_map(self):
        logging.info(f"Carregando o ficheiro {self.fgb_path} com GeoPandas...")
        gdf = gpd.read_file(self.fgb_path)
        
        custom_config = {
            "version": "v1",
            "config": {
                "visState": {
                    "filters": [],
                    "layers": [
                        {
                            "id": "edificacoes_layer",
                            "type": "geojson",
                            "config": {
                                "dataId": "Edificacoes_Urbanas",
                                "label": "Porte das Edificações",
                                "color": [0, 212, 255],
                                "columns": {"geojson": "geometry"},
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.9,
                                    "thickness": 0.0,  # Sem contornos para limpar a visualização
                                    "strokeColor": None,
                                    "filled": True,
                                    "extruded": True,
                                    "wireframe": False,
                                    "elevationScale": 4,
                                    "sizeScale": 10
                                },
                                "colorRange": {
                                    "name": "Colors",
                                    "type": "categorical",
                                    "category": "Custom",
                                    "colors": [
                                        [0, 212, 255],    
                                        [255, 183, 3],    
                                        [6, 214, 160]     
                                    ]
                                }
                            },
                            "visualChannels": {
                                "colorField": {"name": "categoria_tamanho", "type": "string"},
                                "colorScale": "ordinal",
                                "strokeColorField": None,
                                "strokeColorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": {"name": "area_in_meters", "type": "real"},
                                "heightScale": "linear"
                            }
                        }
                    ],
                    "interactionConfig": {
                        "tooltip": {
                            "enabled": True,
                            "compare": False,
                            "coordinate": False
                        },
                        "brush": {"enabled": False},
                        "geocoder": {"enabled": False},
                        "legend": {
                            "enabled": True,   
                            "data": {}
                        }
                    },
                    "layerBlending": "normal",
                    "splitMapMode": False,
                    "mapState": {
                        "bearing": 0,
                        "dragRotate": False,
                        "latitude": -20.3155,
                        "longitude": -40.3128,
                        "pitch": 45,
                        "zoom": 12,
                        "isSplit": False
                    },
                    "mapStyle": {
                        "styleType": "dark",
                        "topLayerGroups": {},
                        "visibleLayerGroups": {
                            "label": True,
                            "road": True,
                            "border": False,
                            "building": True,
                            "water": True,
                            "land": True,
                            "land use": True,
                            "natural": True
                        },
                        "threeDBuildingColor": [9.6, 12.6, 15.9],
                        "customMapStyle": {}
                    }
                },
                "uiState": {
                    "readOnly": False,
                    "mapControls": {
                        "mapLegend": {"show": True},
                        "toggle3d": {"show": True},
                        "splitMap": {"show": False},
                        "fitBounds": {"show": True},
                        "draw": {"show": False},
                        "mapStyle": {"show": False}
                    }
                }
            }
        }

        mapa = KeplerGl(height=800, data={"Edificacoes_Urbanas": gdf}, config=custom_config)
        mapa.save_to_html(file_name=self.html_output_path)
        
        logging.info(f"Mapa 3D interativo salvo com sucesso em: {self.html_output_path}")