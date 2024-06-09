from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# Example job description
job_description = """
We are looking for a skilled data scientist who is proficient in Python and machine learning.
The candidate should have experience with data analysis, data visualization, and statistical modeling.
Familiarity with libraries such as Pandas, NumPy, Scikit-Learn, and Matplotlib is required.
Strong problem-solving skills and the ability to work with large datasets are essential.
Excellent communication skills and teamwork are necessary for this role.
"""

# Preprocess the text
def preprocess_text(text):
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Convert to lowercase
    text = text.lower()
    # Split into words
    words = text.split()
    # Remove common stop words (you can expand this list)
    stop_words = set(['and', 'the', 'to', 'is', 'in', 'for', 'with', 'such', 'as', 'are', 'a','who','such',
                      'work','libraries','experience','large','role','required','strong','familiarity','necessary',
                      'ability','candidate','essential','excellent','skilled','skills','proficient','looking'])
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

processed_text = preprocess_text(job_description)

# Generate the word cloud
wordcloud = WordCloud(collocations=False).generate(processed_text)

# Display the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
