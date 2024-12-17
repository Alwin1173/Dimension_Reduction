import os
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

# Streamlit App Initialization
st.title("PCA and LDA Visualization")

# Function to apply PCA
def apply_pca(data, n_components=2):
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(data)
    return principal_components

# Function to apply LDA
def apply_lda(X, y, n_components=2):
    lda = LDA(n_components=n_components)
    lda_components = lda.fit_transform(X, y)
    return lda_components

# File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.dataframe(df.head())

    if df.shape[1] < 3:  # PCA and LDA require enough features
        st.error("Dataset must have at least 2 features and 1 target column")
    else:
        # Splitting features and target
        X = df.iloc[:, :-1]  # Features
        y = df.iloc[:, -1]   # Target column

        # Encode labels if necessary
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply PCA and LDA
        pca_result = apply_pca(X_scaled, n_components=2)
        lda_result = None
        if len(np.unique(y_encoded)) > 1:  # LDA requires multiple classes
            lda_result = apply_lda(X_scaled, y_encoded, n_components=2)

        # Plot the results
        st.write("### Visualization Results")
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Original Data (First 2 features)
        axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], c=y_encoded, cmap='viridis', s=10)
        axes[0].set_title("Original Data (First 2 Features)")
        axes[0].set_xlabel("Feature 1")
        axes[0].set_ylabel("Feature 2")

        # PCA Reduced
        axes[1].scatter(pca_result[:, 0], pca_result[:, 1], c=y_encoded, cmap='viridis', s=10)
        axes[1].set_title("PCA Reduced Data")
        axes[1].set_xlabel("Principal Component 1")
        axes[1].set_ylabel("Principal Component 2")

        # LDA Reduced (if applicable)
        if lda_result is not None:
            axes[2].scatter(lda_result[:, 0], lda_result[:, 1], c=y_encoded, cmap='viridis', s=10)
            axes[2].set_title("LDA Reduced Data")
            axes[2].set_xlabel("LDA Component 1")
            axes[2].set_ylabel("LDA Component 2")
        else:
            axes[2].text(0.5, 0.5, "LDA requires multiple classes", horizontalalignment='center', fontsize=12)
            axes[2].axis('off')
            axes[2].set_title("LDA Not Applicable")

        st.pyplot(fig)
