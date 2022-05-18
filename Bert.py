#!/usr/bin/env python
# coding: utf-8

# # Question Answering with a Fine-Tuned BERT
# *by Chris McCormick*

# What does it mean for BERT to achieve "human-level performance on Question Answering"? Is BERT the greatest search engine ever, able to find the answer to any question we pose it?
# 
# In **Part 1** of this post / notebook, I'll explain what it really means to apply BERT to QA, and illustrate the details.
# 
# **Part 2** contains example code--we'll be downloading a model that's *already been fine-tuned* for question answering, and try it out on our own text! 
# 
# For something like text classification, you definitely want to fine-tune BERT on your own dataset. For question answering, however, it seems like you may be able to get decent results using a model that's already been fine-tuned on the SQuAD benchmark. In this Notebook, we'll do exactly that, and see that it performs well on text that wasn't in the SQuAD dataset.
# 
# **Links**
# 
# * My [video walkthrough](https://youtu.be/l8ZYCvgGu0o) on this topic. 
# * The blog post version.
# * The [Colab Notebook](https://colab.research.google.com/drive/1uSlWtJdZmLrI3FCNIlUHFxwAJiSu2J0-).

# # Part 1: How BERT is applied to Question Answering

# ## The SQuAD v1.1 Benchmark

# When someone mentions "Question Answering" as an application of BERT, what they are really referring to is applying BERT to the Stanford Question Answering Dataset (SQuAD).
# 
# The task posed by the SQuAD benchmark is a little different than you might think. Given a question, and *a passage of text containing the answer*, BERT needs to highlight the "span" of text corresponding to the correct answer. 
# 
# The SQuAD homepage has a fantastic tool for exploring the questions and reference text for this dataset, and even shows the predictions made by top-performing models.
# 
# For example, here are some [interesting examples](https://rajpurkar.github.io/SQuAD-explorer/explore/1.1/dev/Super_Bowl_50.html?model=r-net+%20(ensemble)%20(Microsoft%20Research%20Asia)&version=1.1) on the topic of Super Bowl 50.
# 

# ## BERT Input Format

# To feed a QA task into BERT, we pack both the question and the reference text into the input.
# 

# 
# [![Input format for QA](https://drive.google.com/uc?export=view&id=1dfgTaE_SABpr2blqwTjq9PTyhYabO8_m)](https://drive.google.com/uc?export=view&id=1dfgTaE_SABpr2blqwTjq9PTyhYabO8_m)
# 

# 
# The two pieces of text are separated by the special `[SEP]` token. 
# 
# BERT also uses "Segment Embeddings" to differentiate the question from the reference text. These are simply two embeddings (for segments "A" and "B") that BERT learned, and which it adds to the token embeddings before feeding them into the input layer. 

# [![BERT eBook Display Ad](https://drive.google.com/uc?export=view&id=1d6L584QYqpREpRIwAZ55Wsq8AUs5qSk1)](https://bit.ly/3isUyCt)

# ## Start & End Token Classifiers

# BERT needs to highlight a "span" of text containing the answer--this is represented as simply predicting which token marks the start of the answer, and which token marks the end.
# 
# ![Start token classification](http://www.mccormickml.com/assets/BERT/SQuAD/start_token_classification.png)
# 
# For every token in the text, we feed its final embedding into the start token classifier. The start token classifier only has a single set of weights (represented by the blue "start" rectangle in the above illustration) which it applies to every word.
# 
# After taking the dot product between the output embeddings and the 'start' weights, we apply the softmax activation to produce a probability distribution over all of the words. Whichever word has the highest probability of being the start token is the one that we pick.
# 
# We repeat this process for the end token--we have a separate weight vector this.
# 
# ![End token classification](http://www.mccormickml.com/assets/BERT/SQuAD/end_token_classification.png)

# # Part 2: Example Code

# In the example code below, we'll be downloading a model that's *already been fine-tuned* for question answering, and try it out on our own text.
# 
# If you do want to fine-tune on your own dataset, it is possible to fine-tune BERT for question answering yourself. See [run_squad.py](https://github.com/huggingface/transformers/blob/master/examples/run_squad.py) in the `transformers` library. However,you may find that the below "fine-tuned-on-squad" model already does a good job, even if your text is from a different domain. 
# 
# > Note: The example code in this Notebook is a commented and expanded version of the short example provided in the `transformers` documentation [here](https://huggingface.co/transformers/model_doc/bert.html?highlight=bertforquestionanswering#transformers.BertForQuestionAnswering).

# ## 1. Install huggingface transformers library

# This example uses the `transformers` [library](https://github.com/huggingface/transformers/) by huggingface. We'll start by installing the package.

# In[1]:


# get_ipython().system('pip install transformers')


# In[2]:



import torch

# ## 2. Load Fine-Tuned BERT-large

# For Question Answering we use the `BertForQuestionAnswering` class from the `transformers` library.
# 
# This class supports fine-tuning, but for this example we will keep things simpler and load a BERT model that has already been fine-tuned for the SQuAD benchmark.
# 
# The `transformers` library has a large collection of pre-trained models which you can reference by name and load easily. The full list is in their documentation [here](https://huggingface.co/transformers/pretrained_models.html).
# 
# For Question Answering, they have a version of BERT-large that has already been fine-tuned for the SQuAD benchmark. 
# 
# BERT-large is really big... it has 24-layers and an embedding size of 1,024, for a total of 340M parameters! Altogether it is 1.34GB, so expect it to take a couple minutes to download to your Colab instance. 
# 
# (Note that this download is not using your own network bandwidth--it's between the Google instance and wherever the model is stored on the web).
# 
# Note: I believe this model was trained on version 1 of SQuAD, since it's not outputting whether the question is "impossible" to answer from the text (which is part of the task in v2 of SQuAD).
# 

# In[3]:


from transformers import BertForQuestionAnswering

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Load the tokenizer as well.
# 
# Side note: Apparently the vocabulary of this model is identicaly to the one in bert-base-uncased. You can load the tokenizer from `bert-base-uncased` and that works just as well.

# In[4]:


from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# ## 3. Ask a Question

# Now we're ready to feed in an example!
# 
# A QA example consists of a question and a passage of text containing the answer to that question.
# 
# Let's try an example using the text in this tutorial!

# In[5]:


question = "How many parameters does BERT-large have?"
answer_text = "BERT-large is really big... it has 24-layers and an embedding size of 1,024, for a total of 340M parameters! Altogether it is 1.34GB, so expect it to take a couple minutes to download to your Colab instance."

# We'll need to run the BERT tokenizer against both the `question` and the `answer_text`. To feed these into BERT, we actually concatenate them together and place the special [SEP] token in between.
# 

# In[6]:


# Apply the tokenizer to the input text, treating them as a text-pair.
input_ids = tokenizer.encode(question, answer_text)

print('The input has a total of {:} tokens.'.format(len(input_ids)))

# Just to see exactly what the tokenizer is doing, let's print out the tokens with their IDs.

# In[7]:


# BERT only needs the token IDs, but for the purpose of inspecting the 
# tokenizer's behavior, let's also get the token strings and display them.
tokens = tokenizer.convert_ids_to_tokens(input_ids)

# For each token and its id...
for token, id in zip(tokens, input_ids):


    # If this is the [SEP] token, add some space around it to make it stand out.
    if id == tokenizer.sep_token_id:
        print('')

    # Print the token string and its ID in two columns.
    print('{:<12} {:>6,}'.format(token, id))

    if id == tokenizer.sep_token_id:
        print('')

# We've concatenated the `question` and `answer_text` together, but BERT still needs a way to distinguish them. BERT has two special "Segment" embeddings, one for segment "A" and one for segment "B". Before the word embeddings go into the BERT layers, the segment A embedding needs to be added to the `question` tokens, and the segment B embedding needs to be added to each of the `answer_text` tokens. 
# 
# These additions are handled for us by the `transformer` library, and all we need to do is specify a '0' or '1' for each token. 
# 
# Note: In the `transformers` library, huggingface likes to call these `token_type_ids`, but I'm going with `segment_ids` since this seems clearer, and is consistent with the BERT paper.

# In[8]:


# Search the input_ids for the first instance of the `[SEP]` token.
sep_index = input_ids.index(tokenizer.sep_token_id)

# The number of segment A tokens includes the [SEP] token istelf.
num_seg_a = sep_index + 1

# The remainder are segment B.
num_seg_b = len(input_ids) - num_seg_a

# Construct the list of 0s and 1s.
segment_ids = [0] * num_seg_a + [1] * num_seg_b

# There should be a segment_id for every input token.
assert len(segment_ids) == len(input_ids)

# >*Side Note: Where's the padding?*
# >
# > The original [example code](https://huggingface.co/transformers/model_doc/bert.html?highlight=bertforquestionanswering#transformers.BertForQuestionAnswering) does not perform any padding. I suspect that this is because we are only feeding in a *single example*. If we instead fed in a batch of examples, then we would need to pad or truncate all of the samples in the batch to a single length, and supply an attention mask to tell BERT to ignore the padding tokens. 

# We're ready to feed our example into the model!
# 
# Note: The result object is of type [QuestionAnsweringModelOutput](https://huggingface.co/transformers/main_classes/output.html#transformers.modeling_outputs.QuestionAnsweringModelOutput)
# 
# 

# In[9]:


# Run our example through the model.
outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                token_type_ids=torch.tensor([segment_ids]),
                # The segment IDs to differentiate question from answer_text
                return_dict=True)

start_scores = outputs.start_logits
end_scores = outputs.end_logits

# Now we can highlight the answer just by looking at the most probable start and end words.

# In[10]:


# Find the tokens with the highest `start` and `end` scores.
answer_start = torch.argmax(start_scores)
answer_end = torch.argmax(end_scores)

# Combine the tokens in the answer and print it out.
answer = ' '.join(tokens[answer_start:answer_end + 1])

print('Answer: "' + answer + '"')

# It got it right! Awesome :)

# > *Side Note: It's a little naive to pick the highest scores for start and end--what if it predicts an end word that's before the start word?! The correct implementation is to pick the highest total score for which end >= start.*

# With a little more effort, we can reconstruct any words that got broken down into subwords.

# In[11]:


# Start with the first token.
answer = tokens[answer_start]

# Select the remaining answer tokens and join them with whitespace.
for i in range(answer_start + 1, answer_end + 1):

    # If it's a subword token, then recombine it with the previous token.
    if tokens[i][0:2] == '##':
        answer += tokens[i][2:]

    # Otherwise, add a space then the token.
    else:
        answer += ' ' + tokens[i]

print('Answer: "' + answer + '"')

# ## 4. Visualizing Scores

# I was curious to see what the scores were for all of the words. The following cells generate bar plots showing the start and end scores for every word in the input.

# In[12]:


import matplotlib.pyplot as plt
import seaborn as sns

# Use plot styling from seaborn.
sns.set(style='darkgrid')

# Increase the plot size and font size.
# sns.set(font_scale=1.5)
plt.rcParams["figure.figsize"] = (16, 8)

# Retrieve all of the start and end scores, and use all of the tokens as x-axis labels.

# In[13]:


# Pull the scores out of PyTorch Tensors and convert them to 1D numpy arrays.
s_scores = start_scores.detach().numpy().flatten()
e_scores = end_scores.detach().numpy().flatten()

# We'll use the tokens as the x-axis labels. In order to do that, they all need
# to be unique, so we'll add the token index to the end of each one.
token_labels = []
for (i, token) in enumerate(tokens):
    token_labels.append('{:} - {:>2}'.format(token, i))

# Create a bar plot showing the score for every input word being the "start" word.

# In[14]:


# Create a barplot showing the start word score for all of the tokens.
ax = sns.barplot(x=token_labels, y=s_scores, ci=None)

# Turn the xlabels vertical.
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="center")

# Turn on the vertical grid to help align words to scores.
ax.grid(True)

plt.title('Start Word Scores')

plt.show()

# Create a second bar plot showing the score for every input word being the "end" word.

# In[15]:


# Create a barplot showing the end word score for all of the tokens.
ax = sns.barplot(x=token_labels, y=e_scores, ci=None)

# Turn the xlabels vertical.
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="center")

# Turn on the vertical grid to help align words to scores.
ax.grid(True)

plt.title('End Word Scores')

plt.show()

# **Alternate View**
# 
# I also tried visualizing both the start and end scores on a single bar plot, but I think it may actually be more confusing then seeing them separately. 

# In[16]:


import pandas as pd

# Store the tokens and scores in a DataFrame. 
# Each token will have two rows, one for its start score and one for its end
# score. The "marker" column will differentiate them. A little wacky, I know.
scores = []
for (i, token_label) in enumerate(token_labels):
    # Add the token's start score as one row.
    scores.append({'token_label': token_label,
                   'score': s_scores[i],
                   'marker': 'start'})

    # Add  the token's end score as another row.
    scores.append({'token_label': token_label,
                   'score': e_scores[i],
                   'marker': 'end'})

df = pd.DataFrame(scores)

# In[17]:


# Draw a grouped barplot to show start and end scores for each word.
# The "hue" parameter is where we tell it which datapoints belong to which
# of the two series.
g = sns.catplot(x="token_label", y="score", hue="marker", data=df,
                kind="bar", height=6, aspect=4)

# Turn the xlabels vertical.
g.set_xticklabels(g.ax.get_xticklabels(), rotation=90, ha="center")

# Turn on the vertical grid to help align words to scores.
g.ax.grid(True)


# ## 5. More Examples

# Turn the QA process into a function so we can easily try out other examples.

# In[18]:


def answer_question(question, answer_text):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.
    input_ids = tokenizer.encode(question, answer_text)

    # Report how long the input sequence is.
    # print('Query has {:,} tokens.\n'.format(len(input_ids)))

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0] * num_seg_a + [1] * num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    # ======== Evaluate ========
    # Run our example through the model.
    outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                    token_type_ids=torch.tensor([segment_ids]),
                    # The segment IDs to differentiate question from answer_text
                    return_dict=True)

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):

        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]

        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]

    print('Answer: "' + answer + '"')


# As our reference text, I've taken the Abstract of the [BERT paper](https://arxiv.org/pdf/1810.04805.pdf).
# 

# In[22]:


import textwrap

# Wrap text to 80 characters.
wrapper = textwrap.TextWrapper(width=80)

bert_abstract = (
    "By default, Python source files are treated as encoded in UTF-8. In that encoding, characters of most languages in the world can be used simultaneously in string literals, identifiers and comments — although the standard library only uses ASCII characters for identifiers, a convention that any portable code should follow. To display all these characters properly, your editor must recognize that the file is UTF-8, and it must use a font that supports all the characters in the file.")

print(wrapper.fill(bert_abstract))

# -----------------------------
# Ask BERT what its name stands for (the answer is in the first sentence of the abstract).

# In[23]:


question = "Python files are treateds as what?"

answer_question(question, bert_abstract)

# ---------------------
# Ask BERT about example applications of itself :)
# 
# The answer to the question comes from this passage from the abstract: 
# 
# > "...BERT model can be finetuned with just one additional output
# layer to create state-of-the-art models for **a wide range of tasks, such as
# question answering and language inference,** without substantial taskspecific
# architecture modifications."

# In[21]:


question = "What are some example applications of BERT?"

answer_question(question, bert_abstract)

# In[ ]:
