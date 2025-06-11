# ai_logic.py

import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample industry classification data
data = {
    "Description": [
        "A SaaS company specializing in AI-driven analytics.",
        "A healthcare startup using machine learning for diagnostics.",
        "Fintech platform focused on blockchain-based payments.",
        "Retail automation company leveraging big data.",
        "Autonomous vehicle sensor startup."
    ],
    "Industry": ["SaaS", "Healthcare", "Fintech", "Retail", "Automotive"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['Description'])
y = df['Industry']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression Model for industry classification
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Industry Classification Accuracy: {accuracy * 100:.2f}%")

# Lead scoring function based on keywords
def lead_scoring(description: str):
    """Score lead based on the presence of relevant keywords"""
    keywords = {
        "SaaS": 0.8,
        "Healthcare": 0.7,
        "Fintech": 0.9,
        "Retail": 0.6,
        "Automotive": 0.7
    }
    
    score = 0
    for keyword, weight in keywords.items():
        if keyword.lower() in description.lower():
            score += weight
    
    return round(score, 2)

# Test lead scoring
test_description = "A new SaaS company providing AI-based solutions for businesses."
score = lead_scoring(test_description)
print(f"Lead Score for '{test_description}': {score}")
