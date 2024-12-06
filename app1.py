import pandas as pd
import streamlit as st

# Charger le fichier CSV
csv_path = r"C:\Users\OTMANE\Downloads\PROJET 2\df_movie_tmdb.csv"

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"Le fichier {csv_path} est introuvable. Assurez-vous qu'il existe et que le chemin est correct.")
    st.stop()

# Vérification des colonnes nécessaires
if 'Titre' in df.columns and 'Genres' in df.columns:
    # Renommer les colonnes pour correspondre aux attentes du système
    df.rename(columns={'Titre': 'Title', 'Genres': 'Genres'}, inplace=True)
else:
    st.error("Le fichier CSV ne contient pas les colonnes nécessaires : 'Titre' et 'Genres'.")
    st.stop()

# Nettoyage des données
df['Title'] = df['Title'].str.strip().str.lower()  # Supprime les espaces et met en minuscule
df['Genres'] = df['Genres'].fillna('')            # Remplit les valeurs manquantes avec une chaîne vide

# Fonction pour obtenir des recommandations en fonction des genres
def get_movie_recommendations_by_genre(movie_title, df):
    movie_title = movie_title.strip().lower()
    
    if movie_title not in df['Title'].values:
        return pd.DataFrame()
    
    # Récupérer les genres du film demandé
    movie_genres = df.loc[df['Title'] == movie_title, 'Genres'].values[0].split(', ')
    
    # Rechercher les films correspondants pour chaque genre
    similar_movies = df[df['Genres'].apply(lambda x: any(genre in x for genre in movie_genres))]
    
    # Exclure le film demandé
    similar_movies = similar_movies[similar_movies['Title'] != movie_title]
    
    # Limiter à 3 recommandations
    recommended_movies = similar_movies[['Title', 'Genres', 'Img1', 'Acteur', 'Moyenne', 'Synopsis']].head(3)
    
    return recommended_movies

# Interface Streamlit
st.title("🎥 Recommender System de Films")
st.subheader("Trouvez votre prochain film préféré!")

# Filtres dans la sidebar
with st.sidebar:
    # Filtrer par genre
    genre_filter = st.selectbox("Choisir un genre", df['Genres'].unique())

    # Filtrer par année
    year_filter = st.slider("Choisir une année", min_value=int(df['Année'].min()), max_value=int(df['Année'].max()), value=(int(df['Année'].min()), int(df['Année'].max())))

    # Filtrer par acteur
    actor_filter = st.selectbox("Choisir un acteur", df['Acteur'].dropna().unique())

# Filtrage des données en fonction des filtres
filtered_df = df

if genre_filter:
    filtered_df = filtered_df[filtered_df['Genres'].str.contains(genre_filter, na=False)]

if year_filter:
    filtered_df = filtered_df[(filtered_df['Année'] >= year_filter[0]) & (filtered_df['Année'] <= year_filter[1])]

if actor_filter:
    filtered_df = filtered_df[filtered_df['Acteur'].str.contains(actor_filter, na=False)]

# Recherche de films basés sur le texte
movie_input = st.text_input("Entrez le titre d'un film :")

if movie_input:
    filtered_movies = filtered_df[filtered_df['Title'].str.contains(movie_input.lower(), na=False)].drop_duplicates(subset='Title')
    movie_suggestions = filtered_movies['Title'].head(10).tolist()

    if movie_suggestions:
        movie_input = st.selectbox("Sélectionnez un film", movie_suggestions)
        
        # Obtenir les recommandations basées sur le film sélectionné
        recommendations = get_movie_recommendations_by_genre(movie_input, filtered_df)
        
        if not recommendations.empty:
            st.subheader("Films recommandés :")
            for _, row in recommendations.iterrows():
                # Afficher les détails des films recommandés
                st.write(f"### **{row['Title']}**")
                
                # Vérifier si l'image existe (si Img1 contient un URL valide)
                if row['Img1'].startswith('http'):  # Si Img1 est un URL
                    st.image(row['Img1'], caption=row['Title'], use_column_width=True)  # Affiche l'image
                else:
                    st.error(f"L'image pour {row['Title']} n'est pas un URL valide.")
                
                st.write(f"**Genres**: {row['Genres']}")
                st.write(f"**Acteurs**: {row['Acteur']}")
                st.write(f"**Note moyenne**: {row['Moyenne']}")
                st.write(f"**Synopsis**: {row['Synopsis']}")
        else:
            st.write("Désolé, aucun film trouvé ou aucune recommandation disponible pour ce titre.")
    else:
        st.warning("Aucun film correspondant à votre recherche.")
