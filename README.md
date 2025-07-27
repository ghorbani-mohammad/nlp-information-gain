# NLP Information Gain Project

A comprehensive Natural Language Processing project focused on text classification using information gain feature selection and various language models (unigram, bigram) for Persian text classification.

## 📋 Project Overview

This project implements text classification algorithms for Persian news articles using different approaches:
- **Information Gain Feature Selection**: Calculates the most informative words for classification
- **Unigram Model**: Basic word-based classification without feature selection
- **Unigram with Feature Selection**: Enhanced classification using top 200 most informative words
- **Bigram Model**: Word pair-based classification for better context understanding

## 🎯 Features

- **Multi-class Classification**: Supports multiple document categories (politics, sports, economy, social, arts)
- **Information Gain Calculation**: Identifies the most discriminative words for classification
- **Stop Word Removal**: Preprocesses text by removing common stop words
- **Multiple Smoothing Parameters**: Tests different delta values (0.1, 0.3, 0.5) for model optimization
- **Confusion Matrix Generation**: Provides detailed performance metrics
- **Persian Text Support**: Specifically designed for Persian language processing

## 📁 File Structure

```
nlp-information-gain/
├── calculate_information_gain.py    # Information gain calculation
├── unigram.py                       # Basic unigram classification
├── unigram_with_feature_selection.py # Unigram with feature selection
├── bigram.py                        # Bigram classification model
├── removeStopWords.py               # Stop word removal preprocessing
├── get200MaxInformation.python.py   # Extract top 200 informative words
├── HAM-Train.txt                    # Training dataset
├── HAM-Test.txt                     # Test dataset
├── puredInput.txt                   # Preprocessed training data
├── Stop_words.txt                   # Persian stop words list
├── information_gain_calculated.txt  # Calculated information gain scores
└── Probably not matter/             # Additional output files
```

## 🚀 Usage

### Prerequisites

Install required Python packages:
```bash
pip install nltk hazm numpy
```

### Data Format

The input files should follow this format:
```
category@@@@@@@@@@ document_text
```

Example:
```
سیاسی@@@@@@@@@@ متن خبر سیاسی
ورزش@@@@@@@@@@ متن خبر ورزشی
```

### Running the Models

1. **Preprocess Data** (Remove stop words):
```bash
python removeStopWords.py
```

2. **Calculate Information Gain**:
```bash
python calculate_information_gain.py
```

3. **Run Unigram Classification**:
```bash
python unigram.py
```

4. **Run Unigram with Feature Selection**:
```bash
python unigram_with_feature_selection.py
```

5. **Run Bigram Classification**:
```bash
python bigram.py
```

6. **Extract Top 200 Words** (Optional):
```bash
python get200MaxInformation.python.py
```

## 📊 Model Details

### Information Gain Calculation
- Calculates entropy-based information gain for each word
- Identifies words that best distinguish between document categories
- Outputs sorted list of words by information gain score

### Unigram Model
- Uses individual word frequencies for classification
- Implements Laplace smoothing with configurable delta values
- Calculates log-likelihood scores for each document category

### Bigram Model
- Uses word pair frequencies for better context understanding
- Implements background probability smoothing
- Considers word sequence patterns in classification

### Feature Selection
- Selects top 200 words with highest information gain
- Reduces feature space for improved performance
- Maintains classification accuracy with fewer features

## 📈 Performance Metrics

The models generate confusion matrices and calculate:
- True Positives (TP)
- False Positives (FP)
- False Negatives (FN)
- Overall accuracy for each delta value

## 🔧 Configuration

### Smoothing Parameters
- Delta values: [0.1, 0.3, 0.5]
- Adjustable in each model file
- Affects model performance and generalization

### Feature Selection
- Number of top words: 200 (configurable)
- Based on information gain scores
- Can be modified in `get200MaxInformation.python.py`

## 📝 Output Files

- `information_gain_calculated.txt`: Word scores sorted by information gain
- `puredInput.txt`: Preprocessed training data without stop words
- Various confusion matrix and performance files in `Probably not matter/` directory

## 🛠️ Technical Implementation

### Libraries Used
- **NLTK**: Natural language processing and tokenization
- **Hazm**: Persian text processing
- **NumPy**: Numerical computations
- **Collections**: Data structures for frequency counting

### Algorithm Details
- **Entropy Calculation**: Uses log base 2 for information gain
- **Smoothing**: Laplace smoothing with configurable parameters
- **Tokenization**: NLTK word tokenization for Persian text
- **Matrix Operations**: Efficient frequency counting using defaultdict

## 📚 Academic Context

This project appears to be an academic assignment (HW1) focused on:
- Information theory in NLP
- Feature selection methods
- Text classification algorithms
- Persian language processing

## 🤝 Contributing

This is an academic project, but suggestions and improvements are welcome. Please ensure any modifications maintain the project's educational value and Persian language support.

## 📄 License

This project is for educational purposes. Please respect academic integrity guidelines when using this code.
