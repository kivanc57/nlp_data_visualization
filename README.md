# NLP Analysis Tools 

## Overview 🌈 

Welcome to the **NLP Data Visualization** project! This repository contains a collection of Python scripts designed to help you analyze and visualize text data in various ways. Each script focuses on a specific type of analysis or visualization, providing a comprehensive toolkit for text data exploration.

This project utilizes a range of powerful Python libraries such as matplotlib, seaborn, wordcloud, spacy, and textblob to perform tasks like frequency analysis, sentiment analysis, and parts of speech tagging. The resulting visualizations, including bar plots, histograms, pie charts, treemaps, violin plots, and word clouds, offer clear and insightful representations of the underlying data.


This project includes:
* 🌍 **Well-known Data Science libraries** 🌍
  * Some them are: `matplotlib`, `seaborn`, `wordcloud`, `spacy`, `textblob`

* 💐 **Colorful visualizations** 💐
  * Each graph is crafted by inspiration from its own document and its function is left open to configure freely. The graphs are: `bar plots`, `histograms`, `pie charts`, `treemaps`, `violin plots`, `word clouds`

* ✨ **Creative file handlings (writings+readings), tailored for large datasets** ✨
  * These are: `txt`, `xml`, `json`, `xlsx`, `csv`, `sgm`

* 🍄 *Each* scripts is a combination from one of these bulletpoints!

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Project Structure](#project_structure)
4. [Visualizations](#visualizations)
  * [Bar Plot](#bar_plot)
  * [Histrogram](#histogram)
  * [Pie Chart](#pie_chart)
  * [Treemap](#treemap)
  * [Violin Plot](#violin_plot)
  * [Word Cloud](#word_cloud)
5. [Data Analysis](#data_analysis)
6. [Usage](#usage)
7. [License](#license)
8. [Contact](#contact)

## 1. Introduction <a id="introduction"></a>

This repository contains Python scripts designed for text data analysis and visualization. Each script focuses on a specific type of analysis or visualization, allowing users to gain insights into text data through various methods.

## 2. Features <a id="features"></a>
🧬 **Comprehensive Text Analysis** 🧬 -> Perform sentiment analysis, frequency analysis, and more.

🔮 **Diverse Visualizations** 🔮 -> Generate bar plots, histograms, pie charts, treemaps, violin plots, and word clouds.

 🌋 **Library Utilization** 🌋 -> Utilizes powerful Python libraries such as matplotlib, seaborn, wordcloud, spacy, and textblob.

🧮 **Easy to Use** 🧮 -> Scripts are designed to be easily run from the command line.

⛓ **Configurable** ⛓ -> Input and output paths can be easily configured for different datasets.

☎️ **Logging** ☎️ -> Each script includes logging to track the execution process and capture errors.


## 3. Project Structure <a id="project_structure"></a>

```
📁 project-root
├── 📁 config
│ ├── 📄 __init__.py
│ ├── 📄 common_config.py
│ └── 📄 constants.py
│
├── 📁 scripts
│ ├── 📄 __init__.py
│ ├── 📄 entity_treemap.py
│ ├── 📄 freq_barplot.py
│ ├── 📄 len_histogram.py
│ ├── 📄 len_violin.py
│ ├── 📄 pos_cloud.py
│ └── 📄 sentiment_piechart.py
│
├── 📁 (logs)
│    ...
│
├── 📄 .gitignore
├── 📄 .gitattributes
└── 📄 main.py
```

**config/**: Contains configuration files.

* ***\_init_.py***: Imports configuration and utility functions.
* ***common_config.py***: Contains common configuration functions and logging setup.
* ***constants.py***: Defines constants used throughout the application.

**src/**: Contains source code files for the project.
* ***\_init_.py***: Initializes the source package and imports functions from individual modules.

| Script | Description | Input File | Ouput File | Graph |
| ----------- | -------|---- |-------|--------------|
| freq_barplot.py |  Generates frequency bar plots from XML data.| xml | txt | Bar Plot |
| len_histogram.py | Creates histograms of sentence lengths from text files. | txt | - | Histogram |
| sentiment_piechart.py | Generates pie charts based on sentiment analysis from text data. | sgm | - | Pie Chart |
| entity_treemap.py | Categorizes entities and build treemaps from XML data using them. | xml | json | Tree Map |
| len_violin_plot.py | Visualizes the length of email addresses using violin plots. | txt | xlsx | Violin Plot |
| pos_cloud.py | Generates word clouds based on parts of speech from text data. | sgm | csv | Word Cloud |

---

**logs**: Stores log files after every execution. If removed or not present, its created again after execution.

**.gitattributes**: Ensures consistent line endings across different operating systems in the repository.

**.gitignore**: Specifies files and directories to be ignored by Git (e.g., virtual environments, build artifacts).

**main.py**: In our case, giving the complexity of tasks, input and outputs of each task, this file is left *empty*. Please consult each script separately.

## 4. Visualizations <a id="visualizations"></a>

### Bar Plot <a id="bar_plot"></a>
The bar plot visualizes the frequency of specific entities or attributes. The script `freq_barplot.py` is used to create a bar plot of the most frequent parts of speech (verbs, subjects, and objects).

![Bar Plot](/screenshots/bar_plot.png?raw=true)
```python
def get_bar_plot(destination, frequency_dict, x_name, y_name, top_n=10, title=None, palette='viridis'):
    try:
        df = DataFrame(frequency_dict.items(), columns=[x_name, y_name])
        df_sorted = df.sort_values(by=y_name, ascending=False).head(top_n)

        plt.figure(figsize=(12, 8))
        barplot(x=x_name, y=y_name, data=df_sorted, palette=palette, hue=x_name, legend=False)
        plt.xlabel = x_name
        plt.ylabel = y_name
        if title:
            plt.title(title, fontweight = "bold")

        plt.savefig(destination)
        plt.close()
        logger.info(f"Graph created in {destination}")

    except Exception as e:
        logger.exception(f"Graph failed: {e} in {destination}")
```

### Histogram <a id="histogram"></a>
The histogram displays the distribution of numerical data. The script `len_histogram.py` generates a histogram showing the distribution of sentence lengths.

![Histogram](/screenshots/histogram.png?raw=true)

```python
def get_histogram(data, destination, color = 'red', bins=20,
                    x_label = 'Sentence Length', y_label ='Number of Sentences',
                    graph_name='histogram.png', title="Distribution of Sentence Lengths"):
    try:
        plt.hist(data, edgecolor='black', histtype='bar', bins=bins, color=color, alpha=0.7, density=1)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if title:
            plt.title("Distribution of Sentence Lengths", fontweight = "bold")
        plt.savefig(destination)
        plt.close()
        logger.info(f"Graph: {graph_name} created in {destination}")

    except Exception as e:
        logger.exception(f"Graph: {graph_name} failed: {e} in {destination}")
        return None
```

### Piechart <a id="pie_chart"></a>
The pie chart shows the proportion of different categories within a dataset. The script `sentiment_pychart.py` creates a pie chart of sentiment distribution.

![Piechart](/screenshots/pie_chart.png?raw=true)

```python
def get_pie_chart(destination, sentiments_categorized, title=None, graph_name='pie_chart.png'):
    try:
        plt.figure(figsize=(8, 8))
        plt.pie(
            sentiments_categorized.values(),
            labels=sentiments_categorized.keys(),
            autopct='%1.1f%%',
            colors=['#65d14f', '#66c2a5', '#c43737'],
            explode=(0.1, 0, 0),
            shadow=True,
            startangle=90
            )
        if title:
            plt.title(title, fontweight = "bold")
        plt.savefig(destination)
        plt.close()
        logger.info(f"Pie chart: {graph_name} created in {destination}")
    
    except Exception as e:
        logger.error(f"Pie chart: {graph_name} failed: {e} in {destination}")
        return None
```

### Treemap <a id="treemap"></a>
The treemap provides a hierarchical view of data with nested rectangles. The script `entity_treemap.py` generates a treemap visualization based on XML file content.

![Treemap](/screenshots/treemap.png?raw=true)

```python
def get_treemap(destination, entity_dict, title='Distribution of Entity Labels'):
    try:
        labels = list(entity_dict.keys())
        frequencies = list(entity_dict.values())
        squarify.plot(sizes=frequencies, label=labels, color=color_palette("Spectral", len(labels)), alpha=0.7, pad=2)

        if title:
            plt.title(title, fontweight = "bold")
        plt.savefig(destination)
        plt.close()
        logger.info(f"Treemap created in {destination}")

    except Exception as e:
        logger.exception(f"Treemap failed: {e} in {destination}")
```
### Violin Plot <a id="violin_plot"></a>
The violin plot shows data distribution across several categories. The script `len_violin.py` generates a violin plot of email lengths.

![Violin Plot](/screenshots/violin_plot.png?raw=true)

```python
def get_violin_plot(destination, data, column_name, title=None, color='Yellow'):
    try:
        data_df = DataFrame(data=data, columns=[column_name])

        plt.figure(figsize=(10, 6))
        violinplot(x=column_name, data=data_df, color=color)
        plt.xlabel(column_name)
        if title:
            plt.title(title, fontweight = "bold")
        
        plt.savefig(destination)
        plt.close()
        logger.info(f"Graph created in {destination}")

    except Exception as e:
        logger.exception(f"Graph failed: {e} in {destination}")
```
### Word Cloud <a id="word_cloud"></a>
The word cloud visualizes the frequency of words in a text. The script `pos_cloud.py` creates a word cloud of the most frequent verbs.

![Violin Plot](/screenshots/word_cloud.png?raw=true)

```python
def get_word_cloud(destination, word_counts, title=None):
    try:
        wordcloud = WordCloud(
            width=800,height=800,
            background_color='white',
            min_font_size=10
            ).generate_from_frequencies(word_counts)
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        if title:
            plt.title(title, fontweight = "bold")

        plt.savefig(destination)
        plt.close()
        logger.info(f"Graph created in {destination}")

    except Exception as e:
        logger.exception(f"Failed graph: {e} in {destination}")
```

## 5. Data Analysis <a id="data_analysis"></a>

The scripts included in this project analyze text data by performing tasks such as frequency analysis, sentiment analysis, and length distribution analysis. They generate visualizations that help in understanding the underlying patterns and characteristics of the text data.

## 6. Usage <a id="usage"></a>

1. Ensure you have Python 3.x installed.

2. Install the required libraries and instances when needed.

3. Run the scripts by executing them from the command line:
```bash
python freq_barplot.py
python len_histogram.py
python sentiment_piechart.py
python entity_treemap.py
python len_violin.py
python pos_cloud.py

```

## 7. License <a id="license"></a>

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](https://github.com/kivanc57/nlp_data_visualization/blob/main/LICENSE) file for details.

## 8. Contact <a id="contact"></a>

Let me know if there are any specific details you’d like to adjust or additional sections you want to include!
* **Email**: kivancgordu@hotmail.com
* **Version**: 1.0.0
* **Date**: 31-07-2024



