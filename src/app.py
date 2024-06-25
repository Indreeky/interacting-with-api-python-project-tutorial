from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt

# Cargar variables de entorno desde el archivo .env en el mismo directorio que el script
env_path = './src/credenciales.env'
load_dotenv(dotenv_path=env_path)

# Obtener CLIENT_ID y CLIENT_SECRET 
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Imprimir las credenciales para verificar
print(f"CLIENT_ID: {client_id}")
print(f"CLIENT_SECRET: {client_secret}")

# Verificar si las variables de entorno se han cargado correctamente
if not client_id or not client_secret:
    raise ValueError("No se encontraron CLIENT_ID o CLIENT_SECRET en las variables de entorno.")

# Configurar el gestor de autenticación de Spotipy
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ID del artista obtenido de la URL
artist_id = '23fqKkggKUBHNkbKtXEls4' 

# Obtener las 10 canciones más populares del artista
results = sp.artist_top_tracks(artist_id)
top_tracks = results['tracks']

# Procesar los datos
songs_data = [
    {
        'nombre': track['name'],
        'popularidad': track['popularity'],
        'duración_minutos': track['duration_ms'] / 60000
    }
    for track in top_tracks
]

# Convertir a DataFrame y ordenar
df = pd.DataFrame(songs_data)
df_sorted = df.sort_values(by='popularidad', ascending=True)
print(df_sorted.head(3))

# Graficar scatter plot con colores personalizados
plt.figure(figsize=(8, 5))
plt.scatter(df['duración_minutos'], df['popularidad'], color='crimson', alpha=0.6, edgecolors='w', linewidth=0.5, s=100)
plt.xlabel('Duración (minutos)')
plt.ylabel('Popularidad')
plt.title('Popularidad vs Duración de las Canciones Principales')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Guardar la imagen del gráfico
plt.savefig('popularidad_vs_duracion.png', dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.show()

#Argumento
#No parece que la duración de una canción influya mucho en su popularidad. Tanto las canciones cortas como las largas pueden ser populares. Al final del día, lo que más importa es que la canción sea buena y le guste a la gente.
