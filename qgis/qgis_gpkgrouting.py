# Example configuration
FILENAME = '/home/alejnp/Projects/UGR/TFG/gpkgrouting' \
           '/gpkgrouting/output/TopologyHandler' \
           '/granada-latest-highways.gpkg'
SOURCE_NODE, TARGET_NODE = 33400024, 330186722

# Imports
import geopandas as gpd
import networkx as nx
import qgis.core as qgs
import shapely.ops as ops

# From GeoPackage, load as GeoPandas dataframe
nodes = gpd.read_file(FILENAME, layer='network_nodes')
links = gpd.read_file(FILENAME, layer='network_links')

# From Dataframes, create NetworkX graph 
graph = nx.from_pandas_edgelist(links, 
  edge_attr=True, create_using=nx.DiGraph)

# Perform pathfinding within the network
path_nodes = nx.dijkstra_path(graph, 
  source=SOURCE_NODE, target=TARGET_NODE,
  weight=lambda _u, _v, e: e['geometry'].length)

# Create a LineString with the path found
linestring = ops.linemerge(graph.edges[u,v]['geometry'] 
  for u, v in zip(path_nodes, path_nodes[1:])
)

# Create a new QGIS LineString layer
layer = qgs.QgsVectorLayer('LineString?crs=epsg:4326',
 f'Shortest Path from {SOURCE_NODE} to {TARGET_NODE}', 
 'memory')

# Create QGIS geometry from path LineString
geometry = qgs.QgsLineString()
geometry.fromWkt(linestring.to_wkt())

# Create new QGIS feature to add onto layer, 
# from previous geometry
feature = qgs.QgsFeature()
feature.setGeometry(geometry)

# Retrieve data provider of the layer and add feature
prov = layer.dataProvider()
prov.addFeature(feature)

# Add layer to current project instance, displaying it
qgs.QgsProject.instance().addMapLayer(layer)