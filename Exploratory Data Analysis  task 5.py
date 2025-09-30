import pandas as pd
# Load datasets
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
gender_submission = pd.read_csv("gender_submission.csv")

# Basic info
print(train.info())

# Statistical summary
print(train.describe(include="all"))

# Value counts for categorical variables
for col in ['Sex', 'Embarked', 'Pclass']:
    print(f"\nValue counts for {col}:\n", train[col].value_counts())


import matplotlib.pyplot as plt
# Plot histograms for numeric features
train.hist(figsize=(12, 8), bins=20, edgecolor="black")
plt.suptitle("Histograms of Titanic Features", fontsize=16)
plt.tight_layout()
plt.show()

import seaborn as sns
plt.figure(figsize=(12, 6))
sns.boxplot(data=train[['Age', 'Fare']])
plt.title("Boxplot of Age and Fare")
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x="Age", y="Fare", hue="Survived", data=train, alpha=0.7)
plt.title("Scatterplot of Age vs Fare by Survival")
plt.show()

sns.pairplot(
    train.dropna(subset=["Age"]), 
    vars=["Age", "Fare", "SibSp", "Parch"], 
    hue="Survived", 
    diag_kind="hist"
)
plt.suptitle("Pairplot of Key Features by Survival", y=1.02)
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(train.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

print("""
Observations:
1. Females had a much higher survival rate.
2. Wealthier passengers (higher Fare, 1st Class) survived more often.
3. Children had better chances of survival compared to adults.
4. Small families (1–2 members) survived more than large families or people traveling alone.
5. 'Cabin' has too many missing values and might need to be dropped or processed.
""")



