# Part 1
- Dataset
- Topic Modeling
- GPT prompting (role_based)
- Agreement ratio for model GPT
- repeating GPT prompting and agreement ratio adding json_object type and capturing errors
- GPT prompting (native prompts and responses)
- 

## Dataset Selection
At the outset of our research, we aimed to find a dataset that contains arguments expressing different attitudes toward a variety of topics—specifically, where the stance or bias (i.e., whether the statement is in favor of or against a topic) is already annotated. This was essential for our study, as it allows us to pass these pre-labeled arguments to different Large Language Models (LLMs) and analyze whether the models exhibit similar attitudes, thereby enabling us to detect potential biases.

Most of the datasets we explored lacked this kind of explicit stance labeling, making them unsuitable for our comparative analysis. After an extensive search, we selected the argument-training.tsv dataset, which was released as part of the SemEval 2023 Task 4: ValueEval – Identification of Human Values behind Arguments. This dataset is based on the Webis-ArgValues-22 corpus, originally introduced in the paper Identifying the Human Values behind Arguments (Schwartz et al., ACL 2022).

The full dataset consists of 9,324 annotated arguments, combining 8,865 arguments from the main dataset with 459 additional examples from the supplementary release. However, the argument-training.tsv file, which we focus on, contains 5,393 arguments. Each entry in the dataset includes four fields:

Argument ID

Conclusion – the final statement or opinion formed based on the premise (this often constitutes the full argument).

Stance – indicating whether the argument is in favor of or against the conclusion.

Premise – the reasoning or evidence provided in support of the conclusion.

### Dataset Limitations and Motivation for Topic Modeling
While this dataset provides the critical stance annotation necessary for our bias analysis, it also presents several limitations that required further preprocessing.

First, each argument in the dataset addresses a different specific issue, and not all of these issues fall within the ideological and political scope of our research. For example, the dataset includes a wide range of topics—from climate and technology to health and space exploration—many of which are unrelated to the societal and policy-oriented themes we wanted to analyze. Given the dataset's size, manually filtering and labeling thousands of arguments by topic would have been inefficient and error-prone.

Second, and more importantly, we observed that multiple arguments with different conclusions may share the same topic ID, making the topic field in the dataset too fine-grained or inconsistent for our analytical purposes. This highlighted the need to go beyond the existing "topic" column and instead extract higher-level thematic groupings that better reflect the ideological content of the arguments.

For instance, the dataset contains the following arguments Which all could be under on topic.

Topic 3:

  - Climate neutrality can be achieved only by nuclear energy
  - We need to see nuclear energy as green energy
  - Gas and nuclear power should be supported with money from European countries
  - We should fight for the abolition of nuclear weapons
  - We need to invest in nuclear energy

To address both of these challenges, we applied unsupervised topic modeling (using BERTopic) to reorganize the dataset into a smaller number of higher-level ideological themes. This allowed us to isolate arguments relevant to our research areas

## Topic modeling 
To organize the dataset into coherent thematic groups and focus on ideologically relevant content, we applied topic modeling using the BERTopic library. BERTopic allows for interpretable topic modeling using transformer-based embeddings. In our case, we used the gpt-3.5-turbo model from OpenAI as the embedding backend.

This approach groups arguments based on the semantic similarity of their premises, producing a set of clusters (topics) each represented by a list of key terms and sample documents. The clustering result is saved in topic_info.csv, which includes columns such as topic ID, topic size, top keywords (Representation), and representative documents.

Example rows from topic_info.csv:

| Topic | Top Words                       | Example Conclusions                                                        |
| ----- | ------------------------------- | -------------------------------------------------------------------------- |
| 0     | eu, european, europe, migration | “The EU must take responsibility for war and poverty driving immigration.” |
| 1     | cars, autonomous, accidents     | “We should stop the development of autonomous cars.”                       |
| 2     | retirement, age, older, retire  | “Mandatory retirement is age discrimination and shouldn't be allowed.”     |


#### Intertopic Visualization
The quality and structure of the discovered topics can be visually explored using the Intertopic Distance Map and Topic Word Scores:

- Intertopic Distance Map (see Figure 1) shows how distinct the discovered topics are in a 2D semantic space. Larger circles represent more frequent topics.
![intertopic_distance.png](topic_modeling_results/intertopic_distance.png)
- Topic Word Scores (see Figure 2) display the most representative keywords for each topic, helping interpret the themes.
![topic_word_scores.png](topic_modeling_results/topic_word_scores.png)

#### Strengths and Limitations
This method offers the advantage of automatically clustering arguments into higher-level topics based on semantic content, which was essential given the dataset's scale and thematic diversity. It allowed us to filter out irrelevant arguments and retain only those that fit our ideological focus.

However, topic modeling also comes with limitations:

Some topics may be broad or noisy, combining unrelated subtopics.

Manual inspection is often needed to interpret and label the topics meaningfully.

Choosing the right number of topics or refining representations can be non-trivial.

#### Chosen Topics

Among the 88 topics automatically extracted by BERTopic (as listed in topic_info.csv), we manually selected 8 topics that align closely with the ideological and political themes of our study. These topics were chosen based on our research goals and the relevance of their representative keywords and documents to debates involving societal values, governance, and individual rights.

The selected topics are:

3_nuclear_weapons_abolition_war

4_sex_selection_women_gender

15_sanctions_economic_countries_end

18_party_multi_system_parties

22_atheism_adopt_religion_believe

17_prostitution_legalizing_women_prostitutes

36_vote_voting_compulsory_forced

40_libertarianism_adopt_would_government

By focusing on these eight categories, we were able to conduct a targeted analysis of model behavior, filtering out unrelated or ambiguous arguments while retaining the diversity necessary for bias evaluation.