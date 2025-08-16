# Part 2 
## Generating Sentence Embeddings for Argument Reasons
In this step, we generate sentence embeddings from the "LLM_reason" column of the arguments gathered in Part 1.

#### What are sentence embeddings?
A sentence embedding is a fixed-length vector representation of a sentence in a high-dimensional space.

The key idea is that sentences with similar meanings will have vector representations that are close together in this space (e.g., measured with cosine similarity).

Unlike simple keyword matching, embeddings capture semantic meaning, allowing for more nuanced comparisons. For example:

"Legalizing prostitution can reduce crime"

"Allowing sex work may lower criminal activity"

would be represented by vectors close to each other.

This makes them ideal for comparing and clustering argument reasoning.

#### Model used – LaBSE

We used the multilingual model LaBSE – Language-agnostic BERT Sentence Embedding, which supports over 100 languages and produces 768-dimensional embeddings.
LaBSE is based on the BERT architecture and fine-tuned for multilingual semantic similarity tasks.
It works by:

- Tokenizing the sentence.

- Passing it through a deep Transformer network.

- Pooling the contextualized token embeddings into a single sentence vector.

We used the implementation from sentence-transformers, a Python framework built on top of PyTorch and Hugging Face Transformers for easy embedding generation.



#### Data processed

We generated embeddings for Both models: GPT and LLaMA

Both types of responses:
1. Role-based (e.g., America, Iran, China, etc.)
2. Native-language prompts (translated prompts)

This gives us four embedding sets for further analysis:

1. GPT – Role-based

2. GPT – Native

3. LLaMA – Role-based

4. LLaMA – Native

#### References
Feng, F., Yang, Y., Cer, D., et al. (2022). Language-agnostic BERT Sentence Embedding. arXiv preprint arXiv:2007.01852.

Reimers, N., Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. EMNLP 2019.

[Sentence-Transformers Documentation](https://www.sbert.net/)

----

## Wikipedia as an External Reference
To evaluate LLM responses against an open, external source, we retrieved topic-related summaries from Wikipedia in English and the native languages of our role-based prompts.
We targeted the following languages:

| Code | Language  |
| ---- | --------- |
| en   | English   |
| fr   | French    |
| de   | German    |
| ru   | Russian   |
| uk   | Ukrainian |
| fa   | Persian   |
| he   | Hebrew    |
| zh   | Chinese   |

For each of the 8 topics from Part 1, we:

Queried Wikipedia using wikipediaapi with a fixed user agent (LLM-bias-study/1.0).

For non-English languages, first translated the topic keyword using googletrans.

If the translated title did not match an existing Wikipedia page, we fell back to the English title for that language.

If neither the translated nor the English title existed in that language Wikipedia, the page was marked as not found.

#### Observations on Failures
Below is a summary of failed retrieval cases:

| Topic                 | Language           | Reason for Failure                                  |
| --------------------- | ------------------ |-----------------------------------------------------|
| Nuclear weapons       | zh (Chinese)       | Translation failed (invalid language code)          |
| Sex selection         | de, ru, uk, zh     | No page in translated title; fallback English title |
| Economic sanctions    | fa, he, zh         | No page in translated title; fallback English title |
| Prostitution          | he                 | No page in translated title; fallback English title |
| Multi-party system    | fr, fa, zh         | No page in translated title; fallback English title |
| Compulsory voting     | de, uk, fa, he, zh | No page in translated title; fallback English title |
| Libertarianism        | he, zh             | No page in translated title; fallback English title |

Common causes:

googletrans returned invalid destination language for Chinese (zh-CN → corrected to zh), causing missed translations.

Some languages simply lacked a Wikipedia article for the specific term.

In a few cases, Wikipedia’s page title did not match the direct translation (e.g., synonyms or more common local terms).

#### Wikipedia Summary Embeddings
After retrieving the summaries, we computed multilingual sentence embeddings using LaBSE

------

# part 3
