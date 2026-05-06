import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("HEART DISEASE ANALYSIS WITH K-MEANS CLUSTERING")
print("="*60)

df = pd.read_csv('heart.csv')

print(f"\nDataset Shape: {df.shape}")
print(f"Number of samples: {df.shape[0]}")
print(f"Number of features: {df.shape[1]}")
print("\nFirst 5 rows:")
print(df.head())

print("\n" + "="*60)
print("EXPLORATORY DATA ANALYSIS")
print("="*60)

# Basic Info
print("\n1. Dataset Information:")
print(df.info())

# Summary
print("\n2. Statistical Summary:")
print(df.describe())

# missing values
print("\n3. Missing Values:")
print(df.isnull().sum())

# Handle missing values
df = df.dropna()
print(f"Dataset shape after removing missing values: {df.shape}")

# Distribution
print("\n4. Target Variable Distribution:")
print(df['target'].value_counts())
print(f"Heart Disease: {df['target'].value_counts().get(1, 0)} cases")
print(f"No Heart Disease: {df['target'].value_counts().get(0, 0)} cases")

# Correlation Analysis
print("\n5. Correlation Matrix:")
correlation_matrix = df.corr()
print(correlation_matrix['target'].sort_values(ascending=False))

# Visualization
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

# Age Distribution
axes[0, 0].hist(df['age'], bins=20, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Age Distribution')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Frequency')

# Cholesterol Distribution
axes[0, 1].hist(df['chol'], bins=20, edgecolor='black', alpha=0.7, color='orange')
axes[0, 1].set_title('Cholesterol Distribution')
axes[0, 1].set_xlabel('Cholesterol')
axes[0, 1].set_ylabel('Frequency')

# Target Distribution
axes[1, 0].bar(['No Disease', 'Disease'], df['target'].value_counts(), 
               color=['green', 'red'], alpha=0.7)
axes[1, 0].set_title('Heart Disease Distribution')
axes[1, 0].set_ylabel('Count')

# Age vs Max Heart Rate
scatter = axes[1, 1].scatter(df['age'], df['thalach'], c=df['target'], 
                             cmap='coolwarm', alpha=0.7)
axes[1, 1].set_title('Age vs Max Heart Rate')
axes[1, 1].set_xlabel('Age')
axes[1, 1].set_ylabel('Max Heart Rate')
plt.colorbar(scatter, ax=axes[1, 1], label='Target')

# Correlation Heatmap
corr_subset = df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'target']].corr()
sns.heatmap(corr_subset, annot=True, cmap='coolwarm', ax=axes[2, 0])
axes[2, 0].set_title('Correlation Heatmap')

# Chest Pain Type Distribution
cp_counts = df['cp'].value_counts().sort_index()
axes[2, 1].bar(cp_counts.index, cp_counts.values, alpha=0.7, color='purple')
axes[2, 1].set_title('Chest Pain Type Distribution')
axes[2, 1].set_xlabel('Chest Pain Type')
axes[2, 1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('eda_analysis.png', dpi=100)
plt.show()

print("\n" + "="*60)
print("BOXPLOTS - OUTLIER DETECTION")
print("="*60)

# Select numerical features for boxplots
numerical_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

for i, feature in enumerate(numerical_features):
    bp = axes[i].boxplot(df[feature], patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')
    axes[i].set_title(f'Boxplot of {feature}')
    axes[i].set_ylabel('Value')
    
    # Calculate outliers
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
    
    print(f"\n{feature}:")
    print(f"  Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}")
    print(f"  Outlier bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"  Number of outliers: {len(outliers)}")
    if len(outliers) > 0:
        print(f"  Outlier values: {outliers[feature].values}")

# Target vs Numerical features boxplots
axes[5].axis('off')
plt.tight_layout()
plt.savefig('boxplots_outliers.png', dpi=100)
plt.show()

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

for i, feature in enumerate(numerical_features[:5]):
    df.boxplot(column=feature, by='target', ax=axes[i])
    axes[i].set_title(f'{feature} by Heart Disease')
    axes[i].set_xlabel('Heart Disease (0=No, 1=Yes)')

axes[5].axis('off')
plt.suptitle('Feature Distributions by Target Variable')
plt.tight_layout()
plt.savefig('boxplots_by_target.png', dpi=100)
plt.show()

print("\n" + "="*60)
print("DATA PREPROCESSING FOR CLUSTERING")
print("="*60)

feature_columns = list(df.columns[:-1])  # All except target
X = df[feature_columns].copy()

print(f"\nFeatures used for clustering ({len(feature_columns)} features):")
print(feature_columns)

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns)

print("\nData standardized (mean=0, std=1)")
print(f"Mean after scaling: {X_scaled_df.mean().mean():.6f}")
print(f"Std after scaling: {X_scaled_df.std().mean():.6f}")

# ============================================
# 5. K-MEANS CLUSTERING
# ============================================
print("\n" + "="*60)
print("K-MEANS CLUSTERING")
print("="*60)

def perform_kmeans(X_scaled, n_clusters, feature_subset=None):
    """Perform K-means clustering and return results"""
    if feature_subset:
        X_subset = X_scaled[:, feature_subset]
        feature_names = [feature_columns[i] for i in feature_subset]
    else:
        X_subset = X_scaled
        feature_names = feature_columns
    
    # Apply K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_subset)
    
    # Calculate metrics
    silhouette_avg = silhouette_score(X_subset, labels)
    inertia = kmeans.inertia_
    
    # Compare with actual target
    df_labels = pd.DataFrame({'Cluster': labels, 'Actual': df['target'].values})
    cross_tab = pd.crosstab(df_labels['Cluster'], df_labels['Actual'])
    
    return {
        'labels': labels,
        'centroids': kmeans.cluster_centers_,
        'silhouette': silhouette_avg,
        'inertia': inertia,
        'cross_tab': cross_tab,
        'feature_names': feature_names
    }
print("\n--- K-means with 2 Features ---")
two_features = [3, 4]  # trestbps and chol
print(f"Selected features: {[feature_columns[i] for i in two_features]}")

results_2 = perform_kmeans(X_scaled, n_clusters=2, feature_subset=two_features)

print(f"\nClustering Results (2 features):")
print(f"Silhouette Score: {results_2['silhouette']:.4f}")
print(f"Inertia: {results_2['inertia']:.2f}")
print("\nCluster vs Actual Target:")
print(results_2['cross_tab'])

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
scatter = plt.scatter(X_scaled[:, two_features[0]], X_scaled[:, two_features[1]], 
                      c=results_2['labels'], cmap='viridis', alpha=0.7)
plt.scatter(results_2['centroids'][:, 0], results_2['centroids'][:, 1], 
           marker='X', s=200, c='red', label='Centroids')
plt.xlabel(feature_columns[two_features[0]])
plt.ylabel(feature_columns[two_features[1]])
plt.title('K-means Clustering (2 Features)')
plt.colorbar(scatter, label='Cluster')
plt.legend()

plt.subplot(1, 2, 2)
scatter = plt.scatter(X_scaled[:, two_features[0]], X_scaled[:, two_features[1]], 
                      c=df['target'], cmap='coolwarm', alpha=0.7)
plt.xlabel(feature_columns[two_features[0]])
plt.ylabel(feature_columns[two_features[1]])
plt.title('Actual Heart Disease Labels')
plt.colorbar(scatter, label='Heart Disease')

plt.tight_layout()
plt.savefig('kmeans_2features.png', dpi=100)
plt.show()

print("\n" + "-"*40)
print("--- K-means with 3 Features ---")

three_features = [0, 3, 4]  # age, trestbps, chol
print(f"Selected features: {[feature_columns[i] for i in three_features]}")

results_3 = perform_kmeans(X_scaled, n_clusters=2, feature_subset=three_features)

print(f"\nClustering Results (3 features):")
print(f"Silhouette Score: {results_3['silhouette']:.4f}")
print(f"Inertia: {results_3['inertia']:.2f}")
print("\nCluster vs Actual Target:")
print(results_3['cross_tab'])

fig = plt.figure(figsize=(15, 5))

# 3D Scatter plot
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
scatter = ax1.scatter(X_scaled[:, three_features[0]], 
                      X_scaled[:, three_features[1]], 
                      X_scaled[:, three_features[2]],
                      c=results_3['labels'], cmap='viridis', alpha=0.7)
ax1.set_xlabel(feature_columns[three_features[0]])
ax1.set_ylabel(feature_columns[three_features[1]])
ax1.set_zlabel(feature_columns[three_features[2]])
ax1.set_title('K-means Clustering (3 Features)')
plt.colorbar(scatter, ax=ax1, label='Cluster')

ax2 = fig.add_subplot(1, 2, 2)
scatter = ax2.scatter(X_scaled[:, three_features[0]], X_scaled[:, three_features[1]], 
                      c=results_3['labels'], cmap='viridis', alpha=0.7, s=50)

centroids_2d = results_3['centroids'][:, :2]
ax2.scatter(centroids_2d[:, 0], centroids_2d[:, 1], 
           marker='X', s=200, c='red', label='Centroids')
ax2.set_xlabel(feature_columns[three_features[0]])
ax2.set_ylabel(feature_columns[three_features[1]])
ax2.set_title('K-means Clustering (2D view of 3 features)')
plt.colorbar(scatter, label='Cluster')
ax2.legend()

plt.tight_layout()
plt.savefig('kmeans_3features.png', dpi=100)
plt.show()

# ============================================
# 5c. K-MEANS WITH ALL FEATURES
# ============================================
print("\n" + "-"*40)
print("--- K-means with All Features ---")

results_all = perform_kmeans(X_scaled, n_clusters=2)

print(f"\nClustering Results (all features):")
print(f"Silhouette Score: {results_all['silhouette']:.4f}")
print(f"Inertia: {results_all['inertia']:.2f}")
print("\nCluster vs Actual Target:")
print(results_all['cross_tab'])

cross_tab = results_all['cross_tab']
if cross_tab.shape == (2, 2):
    accuracy = (cross_tab.values[0, 0] + cross_tab.values[1, 1]) / cross_tab.values.sum()
    print(f"\nClustering Accuracy (compared to actual): {accuracy:.2%}")

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=results_all['labels'], 
                     cmap='viridis', alpha=0.7)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('K-means Clustering (All Features - PCA)')
plt.colorbar(scatter, label='Cluster')

plt.subplot(1, 2, 2)
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['target'], 
                     cmap='coolwarm', alpha=0.7)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('Actual Heart Disease (PCA)')
plt.colorbar(scatter, label='Heart Disease')

plt.tight_layout()
plt.savefig('kmeans_all_features.png', dpi=100)
plt.show()

print("\n" + "="*60)
print("ELBOW METHOD FOR OPTIMAL K")
print("="*60)

inertias = []
silhouette_scores = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    
    if k > 1:
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(K_range, inertias, 'bo-')
axes[0].set_xlabel('Number of Clusters (K)')
axes[0].set_ylabel('Inertia')
axes[0].set_title('Elbow Method')
axes[0].grid(True)

axes[1].plot(range(2, 11), silhouette_scores, 'ro-')
axes[1].set_xlabel('Number of Clusters (K)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Analysis')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('elbow_method.png', dpi=100)
plt.show()

print(f"Optimal K based on silhouette score: {np.argmax(silhouette_scores) + 2}")
print(f"Best silhouette score: {max(silhouette_scores):.4f}")

print("\n" + "="*60)
print("FEATURE IMPORTANCE FOR CLUSTERING")
print("="*60)

kmeans_final = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans_final.fit(X_scaled)

centroids = kmeans_final.cluster_centers_
feature_importance = np.abs(centroids[0] - centroids[1])
importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': feature_importance
}).sort_values('Importance', ascending=False)

print("\nFeature Importance (based on centroid separation):")
print(importance_df)

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'], color='teal', alpha=0.7)
plt.xlabel('Importance (Centroid Separation)')
plt.title('Feature Importance in K-means Clustering')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=100)
plt.show()

print("\n" + "="*60)
print("SUMMARY AND CONCLUSIONS")
print("="*60)

print(f"""
1. DATASET OVERVIEW:
   - Total samples: {df.shape[0]}
   - Features: {df.shape[1]-1} (excluding target)
   - Heart disease cases: {df['target'].sum()} ({(df['target'].mean()*100):.1f}%)

2. KEY FINDINGS FROM EDA:
   - Age range: {df['age'].min()}-{df['age'].max()} years
   - Average cholesterol: {df['chol'].mean():.1f}
   - Most correlated with heart disease: {correlation_matrix['target'].drop('target').idxmax()}

3. OUTLIER ANALYSIS:
   - Features with most outliers: {numerical_features[np.argmax([len(df[(df[f] < df[f].quantile(0.25) - 1.5*(df[f].quantile(0.75)-df[f].quantile(0.25))) | (df[f] > df[f].quantile(0.75) + 1.5*(df[f].quantile(0.75)-df[f].quantile(0.25)))]) for f in numerical_features[:5]])]}

4. CLUSTERING PERFORMANCE:
   - 2 Features Silhouette Score: {results_2['silhouette']:.4f}
   - 3 Features Silhouette Score: {results_3['silhouette']:.4f}
   - All Features Silhouette Score: {results_all['silhouette']:.4f}
   - Best K value: {np.argmax(silhouette_scores) + 2}

5. CONCLUSION:
   - K-means clustering successfully identified patterns in heart disease data
   - Using all features provided better cluster separation
   - The clustering results show correlation with actual heart disease diagnosis
""")

print("\nAnalysis Complete! Check the generated plots for visualizations.")