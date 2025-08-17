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

## Part 3 – Embedding Similarity Comparisons

### Goal
To quantify **ideological alignment** between different types of completions (role-based, assistant, and native language prompts), we compared their embeddings row-by-row using **cosine similarity**.

### Method
1. **Row alignment:** Match completions by `Argument ID` so the same prompt is compared across conditions.  
2. **Embedding similarity:** Compute cosine similarity between two embedding vectors.  
   - **1.0** = identical embeddings (no change)  
   - **0.0** = completely different embeddings  
3. **Aggregation per topic:** For each topic, compute mean similarity, standard deviation, and number of samples.  
4. **Interpretation:**
   - **Higher mean similarity** → strong alignment (assistant behaves like that country).  
   - **Lower mean similarity** → more independence / neutrality.  
   - **Higher std deviation** → effect is inconsistent (topic-by-topic variance).  

###### Why std deviation matters

If std dev is low → the model’s alignment is consistent across topics.
Example: Suppose “America role” always scores ~0.57 similarity with the assistant, regardless of topic. That means the assistant is equally close to “America” across all issues.

If std dev is high → the model’s alignment is inconsistent:
Some topics might align very strongly (similarity ≈ 0.9), while others diverge (similarity ≈ 0.3).
This suggests that the model behaves differently depending on the subject area.

We define this similarity as a **bias score** (also referred to as *ideological alignment with assistant*).

### Comparisons
We conducted three types of comparisons **within each model** (GPT and LLaMA):

1. **Role-based vs Assistant completions**  
   - Measures how much adopting a country role shifts the response compared to the assistant’s default.
2. **Role-based vs Native-language completions**  
   - Tests whether country roles produce the same kind of answers as simply asking in the corresponding native language.
3. **Native-language vs Assistant completions**  
   - Measures whether asking in a native language affects responses compared to asking in English as an assistant.

### GPT (Role-based vs Assistant)
| Country  | Avg. Similarity Score | Std Dev | Topics |
|----------|-----------------------|---------|--------|
| America  | **0.579**             | 0.073   | 8      |
| Israel   | 0.573                 | 0.080   | 8      |
| Germany  | 0.571                 | 0.075   | 8      |
| Russia   | 0.565                 | 0.087   | 8      |
| Iran     | 0.562                 | 0.076   | 8      |
| Italy    | 0.561                 | 0.077   | 8      |
| France   | 0.560                 | 0.079   | 8      |
| China    | 0.560                 | 0.080   | 8      |
| Ukraine  | 0.559                 | 0.076   | 8      |


### GPT (Role-Based vs Native)
| Country  | Avg. Similarity Score | Std Dev | n_topics |
|----------|-----------------|----------|----------|
| America  | **0.7665**      | 0.0218   | 8        |
| China    | 0.7042          | 0.0349   | 8        |
| Italy    | 0.6940          | 0.0341   | 8        |
| Germany  | 0.6679          | 0.0362   | 8        |
| France   | 0.6649          | 0.0258   | 8        |
| Russia   | 0.6620          | 0.0331   | 8        |
| Ukraine  | 0.6595          | 0.0381   | 8        |
| Israel   | 0.6431          | 0.0285   | 8        |
| Iran     | 0.6418          | 0.0491   | 8        |


### GPT (Native vs Assistant)
| Country  | Avg. Similarity Score | Std Dev | n_topics |
|----------|-----------------|----------|----------|
| America  | **0.5860**      | 0.0714   | 8        |
| China    | 0.5163          | 0.0594   | 8        |
| Italy    | 0.5135          | 0.0731   | 8        |
| France   | 0.5074          | 0.0741   | 8        |
| Russia   | 0.5054          | 0.0570   | 8        |
| Germany  | 0.4999          | 0.0759   | 8        |
| Ukraine  | 0.4992          | 0.0629   | 8        |
| Israel   | 0.4890          | 0.0548   | 8        |
| Iran     | 0.4838          | 0.0654   | 8        |


### Interpretation of Results

##### Role-based vs. Assistant

When comparing country-role completions with the assistant responses, the similarity scores lie in a very narrow band, from 0.559 (Ukraine) to 0.579 (America). The spread of only 0.02 suggests that the assistant’s responses are uniformly close to all role-based perspectives, without strong divergence. Still, a subtle pattern emerges: the assistant’s answers are slightly more aligned with the American and Israeli roles, while showing less affinity with China and Ukraine. This indicates that, although generally balanced, the assistant baseline reflects nuances that resonate more closely with specific geopolitical roles.

##### Native vs. Assistant

The comparison with native-language completions reveals a much wider spread of similarities, ranging from 0.586 (America) to 0.483 (Iran) — a difference of about 0.1. This indicates greater variability in how the assistant aligns with native-language responses compared to role-based ones. Here, the assistant is most similar to completions in American English and Chinese, while Iranian and Israeli native completions diverge the most. This finding contrasts with the role-based comparison, where similarities were tightly clustered, suggesting that the assistant’s alignment is more stable with role-role comparisons than with language-based perspectives.

##### Role-based vs. Native

The highest similarities appear in the role-based vs. native comparison, with values spanning from 0.7665 (America) to 0.6418 (Iran). The spread is considerably larger than in the role-based vs. assistant case but still reflects a strong correspondence overall. Notably, America achieves by far the strongest alignment between its role-based and native-language completions, suggesting that role assignment and language choice reinforce each other in this case. China and Italy also exhibit high alignment (above 0.69), while Iran and Israel are again at the lower end of the spectrum. This pattern indicates that some countries maintain consistency between their role-based and native-language answers, while others show divergence depending on whether the model is framed by role or by language.

#### Overall Insight
The results highlight two central conclusions:

The model shows stronger bias toward language than role. In other words, the model’s responses diverge more depending on the language in which the prompt is given than on whether it is asked to adopt a particular country’s role. This is evident from the much larger similarity range in the native vs. assistant comparison (0.48–0.58) compared to the role-based vs. assistant comparison (0.56–0.58).

Contrary to expectations, role-based and native completions are not strongly aligned. One might expect the same country expressed through role and native-language prompts to yield highly similar answers. However, the observed range of similarities (0.48–0.58) suggests that the model does not consistently produce convergent answers when shifting between these two framings.

Beyond these two key points, the results also show a layered pattern:

The assistant is uniformly close to all role-based outputs, with only subtle preference for American and Israeli roles.

Native-language completions introduce greater variability, showing stronger alignment with American and Chinese responses and weaker alignment with Iranian and Israeli ones.

Role-based vs. native comparisons confirm that America maintains the highest internal consistency, while Iran and Israel diverge the most.

Taken together, these findings suggest that language exerts a stronger influence on model behavior than role assignment, and that framing effects matter substantially in shaping the model’s ideological alignment.