import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Knowledge Base: Deities and their Semantic Profiles (Attributes)
# We define each deity by the 'energy' or 'domain' they occupy.
deity_data = {
    "Ganesha": "removing obstacles new beginnings wisdom success intellect clarity",
    "Hanuman": "strength courage protection devotion anxiety fear discipline",
    "Shiva": "inner peace meditation detachment destruction of ego stillness",
    "Mahalakshmi": "abundance wealth prosperity flow beauty material growth",
    "Krishna": "guidance strategy love philosophy joy karma duty",
    "Saraswati": "knowledge arts speech education creativity focus",
    "Durga": "protection power justice victory over evil feminine energy",
    "Dhanvantari": "healing health medicine recovery vitality wellness"
}

hymn_recommendations = {
    "Ganesha": "Sankata Nashana Ganesha Stotram",
    "Hanuman": "Hanuman Chalisa",
    "Shiva": "Nirvana Shatakam",
    "Mahalakshmi": "Kanakadhara Stotram",
    "Krishna": "Bhagavad Gita - Chapter 2",
    "Saraswati": "Saraswati Vandana",
    "Durga": "Argala Stotra",
    "Dhanvantari": "Dhanvantari Maha Mantra"
}

def recommend_spiritual_path(user_situation):
    # NLP Processing: Vectorization
    # We combine the user input with the deity data to create a shared vector space
    corpus = list(deity_data.values()) + [user_situation]
    
    # Using TF-IDF to capture the 'importance' of emotional keywords
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(corpus)
    
    # Linear Algebra: Cosine Similarity
    # Split the matrix back into deity vectors and the user vector
    deity_vectors = matrix[:-1]
    user_vector = matrix[-1]
    
    # Calculate similarity: dot(A, B) / (||A|| * ||B||)
    similarities = cosine_similarity(user_vector, deity_vectors).flatten()
    
    # Find the index of the highest similarity score
    best_match_idx = np.argmax(similarities)
    deity_list = list(deity_data.keys())
    recommended_deity = deity_list[best_match_idx]
    confidence_score = similarities[best_match_idx]
    
    return recommended_deity, hymn_recommendations[recommended_deity], confidence_score

# --- EXECUTION ---
print("--- Spiritual Vector Analysis ---")
situation = input("Tell me how you feel, I can guide you: ")

deity, hymn, score = recommend_spiritual_path(situation)

print(f"\n[Analysis Complete]")
print(f"Detected Emotional Vector Alignment: {deity}")
print(f"Recommended Resonance Hymn: {hymn}")
print(f"Mathematical Confidence: {score:.2f}")
