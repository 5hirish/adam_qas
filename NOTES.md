## SQUAD 2.0

SQuAD2.0 combines the 100,000 questions in SQuAD1.1 with over 50,000 new, unanswerable questions written adversarially 
by crowdworkers to look similar to answerable ones.

Implementing: [U-Net: Machine Reading Comprehension with Unanswerable Questions, Fudan University & Liulishuo Lab](
https://arxiv.org/pdf/1810.06638.pdf)

This paper decomposes the problem of Machine Reading Comprehension with unanswerable questions into three sub-tasks:
 answer pointer, no-answer pointer, and answer verifier. 

1) an answer pointer to predict a canidate answer span for a question; 
2) a no-answer pointer to avoid selecting any text span when a question has no answer; and 
3) an answer verifier to determine the probability of the "unanswerability" of a question with candidate answer information.

Introduce a universal node and process the question and its context passage as a single contiguous sequence of tokens,
 which greatly improves the conciseness of UNet.

Represent the MRC problem as: given a set of tuples *(Q, P, A)*, 
where *Q = (q<sub>1</sub>, q<sub>2</sub>, · · · , q<sub>m</sub>)* is the question with *m* words, 
*P = (p<sub>1</sub>, p<sub>2</sub>, · · · , p<sub>n</sub>)* is the context passage with *n* words, 
and *A = p<sub>r<sub>s</sub>:r<sub>e</sub></sub>* is the answer with *r<sub>s</sub>* and *r<sub>e</sub>* indicating 
the start and end points, the task is to estimate the conditional probability *P(A|Q, P)*.

#### 1) Unified Encoding

**Embedding**: Embed both the question and the passage with Glove embedding and Elmo embedding.
Use POS embedding, NER embedding, and a feature embedding that
includes the exact match, lower-case match, lemma match,
and a TF-IDF feature. Get the question representation *Q = q<sup>m</sup><sub>i=1</sub>* and
the passage representation *P = p<sup>n</sup><sub>i=1</sub>*, where each word is represented as a d-dim 
embedding by combining the features/embedding described above.

**Universal Node**: We create a universal node *u*, to learn universal information from
both passage and question. This universal node is added and
connects the passage and question at the phase of embedding,
and then goes along with the whole representation, so
it is a key factor in information representation.

We concatenated question representation,
universal node representation, passage representation
together as:

*V = [Q, u, P] = [q<sub>1</sub>, q<sub>2</sub> . . . q<sub>m</sub>, u, p<sub>1</sub>, p<sub>2</sub>, · · · , p<sub>n</sub>]*

**Word-level Fusion**: Then we first use two-layer bidirectional
LSTM (BiLSTM) to fuse the joint representation of question, universal
node, and passage.

*H<sup>l</sup> = BiLSTM(V)*

*H<sup>h</sup> = BiLSTM(H<sup>l</sup>)*

*H<sup>f</sup> = BiLSTM([H<sup>l</sup>;H<sup>h</sup>])*

Thus, *H = [H<sup>l</sup>; H<sup>h</sup>; H<sup>f</sup>]* represents the deep fusion information
of the question and passage on word-level. When
a BiLSTM is applied to encode representations, it learns
the semantic information bi-directionally. Since the universal
node *u* is between the question and passage, its hidden
states h<sub>m+1</sub> can learn both question and passage information.

#### 2) Multi-Level Attention

First divide *H* into two representations: attached passage
*H<sub>q</sub>* and attached question *H<sub>p</sub>*, and let the universal node
representation h<sub>m+1</sub> attached to both the passage and question,

*H<sub>q</sub> = [h<sub>1</sub>, h<sub>2</sub>, · · · , h<sub>m+1</sub>]*

*H<sub>p</sub> = [h<sub>m+1</sub>, h<sub>m+2</sub>, · · · , h<sub>m+n+1</sub>]*

Note *h<sub>m+1</sub>* is shared by *H<sub>q</sub>* and *H<sub>p</sub>*. Here the universal node
works as a special information carrier, and both passage and
question can focus attention information on this node so that
the connection between them is closer than a traditional biattention
interaction.

We first compute the affine matrix of *H<sup>l</sup><sub>q</sub>* and *H<sup>l</sup><sub>p</sub>* by

*S = (ReLU(W<sub>1</sub>H<sup>l</sup><sub>q</sub>))<sup>T</sup>ReLU(W<sub>2</sub>H<sup>l</sup><sub>p</sub>)*

Where, *W<sub>1</sub>* and *W<sub>2</sub>* are learnable parameters.
Next, a bi-directional attention is used to compute the
interacted representation *<sup>^</sup>H<sup>l</sup><sub>q</sub>*
and *<sup>^</sup>H<sup>l</sup><sub>p</sub>*.

*<sup>^</sup>H<sup>l</sup><sub>q</sub> = H<sup>l</sup><sub>p</sub> × softmax(S<sup>T</sup>)*

*<sup>^</sup>H<sup>l</sup><sub>p</sub> = H<sup>l</sup><sub>q</sub> × softmax(S)*

where *softmax(·)* is column-wise normalized function. We use the same attention layer to model the interactions
for all the three levels, and get the final fused representation
*<sup>^</sup>H<sup>l</sup><sub>q</sub>, <sup>^</sup>H<sup>h</sup><sub>q</sub>, <sup>^</sup>H<sup>f</sup><sub>q</sub>* for the question and passage respectively

#### 3) Final Fusion

We concatenate all the history information: we first concatenate the
encoded representation *H* and the representation after attention *<sup>^</sup>H*. We pass the concatenated representation H through
a BiLSTM to get HA.

*H<sup>A</sup> = BiLSTM[H<sup>l</sup>; H<sup>h</sup>; H<sup>f</sup>; <sup>^</sup>H<sup>l</sup>; <sup>^</sup>H<sup>h</sup>; <sup>^</sup>H<sup>f</sup>]*

where the representation *H<sup>A</sup>* is a fusion of information from
different levels. Then we concatenate the original embedded representation
*V* and *H<sup>A</sup>* for better representation of the fused information
of passage, universal node, and question.

*A = [V;H<sup>A</sup>]*

Finally, we use a self-attention layer to get the attention
information within the fused information. The self-attention
layer is constructed the same way as:

*<sup>^</sup>A = A × softmax(A<sup>T</sup>A)*

where *<sup>^</sup>A* is the representation after self-attention of the fused
information *A*. Next we concatenated representation *H<sup>A</sup>*
and *<sup>^</sup>A* and pass them through another BiLSTM layer:

*O = BiLSTM[H<sup>A</sup>; <sup>^</sup>A]*

Now *O* is the final fused representation of all the information.
At this point, we divide *O* into two parts: *OP* , *OQ*,
representing the fused information of the question and passage
respectively.

*O<sup>P</sup> = [o<sup>1</sup>, o<sup>2</sup>, · · · , o<sup>m</sup>]*

*O<sup>Q</sup> = [o<sup>m+1</sup>, o<sup>m+2</sup>, · · · , o<sup>m+n+1</sup>]*

Note for the final representation, we attach the universal
node only in the passage representation *O<sup>P</sup>* . This is because
we need the universal node as a focus for the pointer when
the question is unanswerable. 

#### 4) Prediction

The prediction layer receives fused information of passage
*O<sup>P</sup>* and question *O<sup>Q</sup>*, and tackles three prediction tasks: 
1) answer pointer, 
2) no-answer pointer and 
3) answer verifier

First, we summarize the
question information *O<sup>Q</sup>* into a fixed-dim representation *c<sub>q</sub>*.


where *W<sub>q</sub>* is a learnable weight matrix and *o<sup>Q</sup><sub>i</sub>*
represents the i<sup>th</sup> word in the question representation. Then we feed c<sub>q</sub>
into the answer pointer to find boundaries of answers , and the classification layer to distinguish
whether the question is answerable.

##### i) Answer Pointer
We use two trainable matrices *W<sub>s</sub>* and
*W<sub>e</sub>* to estimate the probability of the answer start and end
boundaries of the i<sup>th</sup> word in the passage, α<sub>i</sub> and β<sub>i</sub>.

*α<sub>i</sub> ∝ exp(c<sub>q</sub>W<sub>s</sub>o<sup>P</sup><sub>i</sub>)*

*β<sub>i</sub> ∝ exp(c<sub>q</sub>W<sub>e</sub>o<sup>P</sup><sub>i</sub>)*

Note here when the question is answerable, we do not
consider the universal node in answer boundary detection,
so we have *i > 0*.

The loss function for the answerable question pairs is:

*L<sub>A</sub> = −(log α<sub>a</sub> + log β<sub>b</sub>)*


where *a* and *b* are the ground-truth of the start and end
boundary of the answer

##### ii) No-Answer Pointer
We use the same pointer for questions that are not answerable

*L<sub>NA</sub> = −(log α<sub>0</sub> + log β<sub>0</sub>) − (log α<sup>\`</sup><sub>a\*</sub> + log β<sup>\`</sup><sub>b\*</sub>)*


Here *α<sub>0</sub>* and *β<sub>0</sub>* correspond to the position of the universal node,
which is at the front of the passage representation *O<sub>p</sub>*. For
this scenario, the loss is calculated for the universal node. 

Additionally, since there exits a plausible answer for each
unanswerable question in SQuAD 2.0, we introduce an auxiliary
plausible answer pointer to predict the boundaries of
the plausible answer. where *α\`* and *β\`*
are the output of the plausible answer pointer; *a<sup>∗</sup>*
and *b<sup>∗</sup>* are the start and end boundary of the unanswerable answer.

##### iii) Answer Verifier
Answer verifier applies a weighted summary layer to
summarize the passage information into a fixed-dim representation *c<sub>q</sub>*
And we use the weight matrix obtained from the answer
pointer to get two representations of the passage.

*F = [c<sub>q</sub>; o<sub>m+1</sub>; c<sub>s</sub>; c<sub>e</sub>]*

This fixed *F* includes the representation *c<sub>q</sub>* representing
the question information, and *c<sub>s</sub>* and *c<sub>e</sub>* representing the
passage information. Since these representations are highly
summarized specially for classification, we believe that this
passage-question pair contains information to distinguish
whether this question is answerable.

Finally, we pass this fixed vector *F* through a linear layer
to obtain the prediction whether the question is answerable.

*p<sup>c</sup> = σ(W<sup>T</sup><sub>f</sub> F)*

where *σ* is a sigmoid function, *W<sub>f</sub>* is a learnable weight matrix.
Here we use the cross-entropy loss in training.

*L<sub>AV</sub> = − (δ · log p<sup>c</sup> + (1 − δ) · (log (1 − p<sup>c</sup>)))*

where *δ ∈ {0, 1}* indicates whether the question has an answer
in the passage.


#### Training
We jointly train the three tasks by combining the three loss
functions. The final loss function is:

*L = δL<sub>A</sub> + (1 − δ)L<sub>NA</sub> + L<sub>AV</sub>*

where *δ ∈ {0, 1}* indicates whether the question has an answer
in the passage, *L<sub>A</sub>, L<sub>NA</sub> and L<sub>AV</sub>* are the three loss
functions of the answer pointer, no-answer pointer, and answer
verifier.

Refering:
* [Attention and Memory in Deep Learning and NLP
](http://www.wildml.com/2016/01/attention-and-memory-in-deep-learning-and-nlp/)
* Glove Vectors
* Elmo
* Loss function
* BiLSTM
* Softmax
* Affine matrix