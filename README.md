# CHC_dh_assignment2

This repository contains the complete workflow and deliverables of a Digital Humanities project that analyzes the character-interaction network of Lin Daiyu in Chapters 10–20 of Dream of the Red Chamber.
Using Python, the project extracts co-occurrence, character mentions, dialogic relations, and sentiment tendencies, constructs a weighted character network, and visualizes it interactively with Streamlit and PyVis.

Key Components
1. Unified Character Naming (Alias Dictionary)

A comprehensive alias dictionary was constructed to normalize multiple forms of character references—
for example:

“林姑娘” → Daiyu

“宝二爷” → Baoyu

“老祖宗” → Grandmother Jia

“琏二奶奶” → Xifeng

Dozens of named characters across the Jia, Shi, Wang, and Xue families are mapped to canonical forms, ensuring accurate statistical and network analysis.

2. Data Extraction and Analytical Outputs

The project automatically generates:

✔ Co-occurrence Edge Table

daiyu_edges_cooccur.csv — weighted edges representing how often Daiyu co-occurs with each character.

✔ Sentence-Level Interaction Records

daiyu_interaction_sentences.txt — detailed annotations including:

Co-occurring characters

Directional mentions (who mentions whom)

Sentiment label (positive / negative / neutral / mixed)

Distance thresholds

Dialogue contexts

✔ Node Attribute Table

Includes centrality measures:

Strength (weighted degree)

Betweenness

Closeness

Eigenvector centrality

✔ Gephi-ready GEXF File

Can be directly imported into Gephi for further exploration or styling.

3. Network Modeling with NetworkX

Using NetworkX, the project computes:

Node centrality metrics

Network density

Core–inner–outer structural layers (based on strength quantiles)

Structural interpretation of Daiyu’s ego-network

These metrics help distinguish emotional, domestic, and political/outer-circle characters in the narrative.

4. Streamlit Interactive Web Application

This repository includes a fully functional Streamlit web app that allows users to:

Upload their own analysis files (edges / nodes / sentences)

Explore an interactive drag-and-move circular network layout

View character layers (core, inner, peripheral)

Analyze the sentiment trend across the narrative

Search sentences by keyword, sentiment, or section (co-occurrence / mentions)

Download an automatically packaged output.zip containing:

node table

edge table

GEXF file

filtered sentence sets

The app provides a clean UI designed for class presentation, replication, and further research.

requirement

streamlit>=1.29.0
pandas>=1.5.0
networkx>=3.1
pyvis>=0.3.2
matplotlib>=3.7.0
