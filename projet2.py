import streamlit as st

# Votre application Streamlit
st.title("🎥 Les Cinémas de la Creuse")
st.subheader("Trouvez votre film")

# Données des films avec affiches et descriptions
movies = [
    {
        "title": "Transformers",
        "category": "Animation",
        "year": 2023,
        "actors": ["Chris Hemsworth", "Scarlett Johansson"],
        "description": "Un préquel animé explorant les origines des Transformers.",
        "image": "https://www.premiere.fr/sites/default/files/styles/scale_crop_336x486/public/2018-04/Transformers.jpg",
        "trailer": "https://www.youtube.com/watch?v=exemple",
        "rating": 8.7,
    },
    {
        "title": "Haikyuu!! La Guerre des Poubelles",
        "category": "Animation",
        "year": 2023,
        "actors": ["Ayumu Murase", "Kaito Ishikawa"],
        "description": "Une bataille épique et hilarante sur le terrain de volley.",
        "image": "https://th.bing.com/th/id/OIP.NiU16SZkEcQkcXvXWJnUKgHaLH?rs=1&pid=ImgDetMain",
        "trailer": "https://www.youtube.com/watch?v=exemple",
        "rating": 9.0,
    },
    {
        "title": "Spider-Man: Across the Spider-Verse",
        "category": "Animation",
        "year": 2023,
        "actors": ["Shameik Moore", "Hailee Steinfeld"],
        "description": "Une aventure multidimensionnelle avec Spider-Man.",
        "image": "https://www.dolby.com/siteassets/xf-site/content-detail-pages/sv2_1280x1920_stothard_dolby_02.jpg",
        "trailer": "https://www.youtube.com/watch?v=exemple",
        "rating": 9.2,
    },
    {
        "title": "Dune: Deuxième partie",
        "category": "Fiction",
        "year": 2024,
        "actors": ["Timothée Chalamet", "Zendaya", "Oscar Isaac"],
        "description": "Suite épique de l'adaptation de Frank Herbert.",
        "image": "https://fr.web.img6.acsta.net/pictures/23/05/03/11/51/2350536.jpg",
        "trailer": "https://www.youtube.com/watch?v=exemple",
        "rating": 9.1,
    },
    {
        "title": "Rebel Moon: Partie 1 - Calice de sang",
        "category": "Fiction",
        "year": 2023,
        "actors": ["Charlie Hunnam", "Sofia Boutella", "Michiel Huisman"],
        "description": "Une bataille pour la survie d'une colonie lointaine.",
        "image": "https://image.tmdb.org/t/p/w500/uiYV2ldUZPDDhgJ6SdXKKB4HRhS.jpg",
        "trailer": "https://www.youtube.com/watch?v=exemple",
        "rating": 8.5,
    },
    # Ajout d'autres films ici...
]

# Genres (catégories spécifiques)
genres = ["Animation", "Fiction", "Documentaire", "Comédie"]
selected_genre = st.sidebar.selectbox("Filtrer par genre :", ["Tous"] + genres)

# Années (de 1960 à 2024)
years = list(range(1960, 2025))
selected_year = st.sidebar.selectbox("Filtrer par année :", ["Toutes"] + years)

# Acteurs (unique et trié)
all_actors = sorted(set(actor for movie in movies for actor in movie["actors"]))
selected_actor = st.sidebar.selectbox("Filtrer par acteur :", ["Tous"] + all_actors)

# Filtrage des films
filtered_movies = movies
if selected_genre != "Tous":
    filtered_movies = [movie for movie in filtered_movies if movie["category"] == selected_genre]

if selected_year != "Toutes":
    filtered_movies = [movie for movie in filtered_movies if movie["year"] == selected_year]

if selected_actor != "Tous":
    filtered_movies = [movie for movie in filtered_movies if selected_actor in movie["actors"]]

# Affichage des films filtrés
st.write("### Films disponibles :")
for movie in filtered_movies:
    st.image(movie["image"], caption=movie["title"], use_column_width=True)
    st.write(f"**{movie['title']}** ({movie['year']})")
    st.write(f"*Catégorie* : {movie['category']}")
    st.write(f"*Description* : {movie['description']}")
    st.write(f"⭐ **Note** : {movie['rating']}")
    st.markdown(f"[🎬 Voir la bande-annonce]({movie['trailer']})")

