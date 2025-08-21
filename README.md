# Thesis Project: Bias and Ideological Tendencies in Large Language Models  

This project investigates potential biases and ideological tendencies in Large Language Models (LLMs), focusing on whether models display different stances when prompted under various roles (e.g., specific countries) and languages. The research explores agreement ratios on controversial topics and measures the similarity of reasoning patterns across roles, languages, and assistant responses. The workflow is divided into two main parts: agreement ratio analysis and embedding similarity analysis.  

---

## Project Structure  

### [Part 1: Agreement Ratio Analysis](part_1_readme.md)  
**Notebooks:**  
- `Thesis_part1.ipynb`  
- `Thesis_part1_5.ipynb`  

This section covers:  
- Dataset preparation and topic modeling.  
- Selection of key topics relevant to the research.  
- Collecting model responses (both GPT and LLaMA) under **role-based** and **language-based** conditions.  
- Introducing the **Agreement Ratio** metric.  
- Measuring agreement ratios across roles, languages, and topics.  
- Visualizing results with plots for comparison.  

---

### [Part 2: Embedding Similarity Analysis](part_2_readme.md)  
**Notebooks:**  
- `Thesis_part2_generate_embeddings.ipynb`  
- `Thesis_part_3_Similarities_GPTmodel.ipynb`
- `Thesis_part_3_Similarities_LlamaModel.ipynb`  

This section covers:  
- Generating **sentence embeddings** for argument reasons across both models, for role-based and language-based prompts.  
- (Experimental, not included in thesis results) Generating topic summaries from Wikipedia as external references and embedding them. Due to poor coverage and frequent errors, this part is considered **future work**.  
- Performing **embedding similarity comparisons** (cosine similarity) for:  
  - Role-based vs Assistant  
  - Role-based vs Native  
  - Native vs Assistant  
- Presenting results and interpretations of embedding similarities across all topics and roles.  

---

## How to Navigate the Repository  

- Each part has its own detailed README (`part_1_readme.md`, `part_2_readme.md`).  
- Jupyter notebooks contain the implementation, while plots and results are saved for reference.  
- The main findings are divided into **Agreement Ratio Analysis** (Part 1) and **Embedding Similarity Analysis** (Part 2).  

---

## Future Work  

- Improving the integration of external references (e.g., Wikipedia embeddings) by handling multilingual coverage and data quality issues.  
- Extending the methodology to additional LLMs or future model generations.  
- Refining similarity measures to capture more nuanced ideological biases.  
