import gensim
import re
import spacy
from collections import Counter, OrderedDict
from pprint import pprint


def query2vec(query, dictionary):

    corpus = dictionary.doc2bow(query)

    return corpus


def doc2vec(documents):
    with open('corpus/stop_words.txt', 'r', newline='') as stp_fp:
        stop_list = (stp_fp.read()).lower().split("\n")
    texts = [[word for word in doc.text.lower().split() if word not in stop_list]for doc in documents]

    frequency = Counter()
    for sent in texts:
        for token in sent:
            frequency[token] += 1

    texts = [[token for token in snipp if frequency[token] > 1]for snipp in texts]

    dictionary = gensim.corpora.Dictionary(texts)
    # print(dictionary)
    # print(dictionary.token2id)

    corpus = [dictionary.doc2bow(snipp) for snipp in texts]

    return corpus, dictionary


def transform_vec(corpus, query_corpus):
    lsidf = gensim.models.LsiModel(corpus)

    corpus_lsidf = lsidf[corpus]
    query_lsidf = lsidf[query_corpus]

    return corpus_lsidf, query_lsidf


def similariy(corpus_lsidf, query_lsidf):
    index = gensim.similarities.SparseMatrixSimilarity(corpus_lsidf, num_features=100000)

    simi = index[query_lsidf]

    simi_sorted = sorted(enumerate(simi), key=lambda item: -item[1])
    # print("Rank:")
    # pprint(simi_sorted)
    return simi_sorted


def combine(sub_keys, keywords_splits, lb, mb, ub):
    whitespace = ' '
    while mb != ub:
        keywords_splits.append(whitespace.join(sub_keys[lb: mb]))
        keywords_splits.append(whitespace.join(sub_keys[mb: ub]))
        mb += 1
    del sub_keys[0]
    if len(sub_keys) > 2:
        combine(sub_keys, keywords_splits, 0, 1, len(sub_keys))


def keywords_splitter(keywords, keywords_splits):

    for key in keywords:
        sub_keys = key.split()

        if len(sub_keys) > 2:
            combine(sub_keys, keywords_splits, 0, 1, len(sub_keys))


def pre_query(keywords):
    keywords = [keywords[feat].lower() for feat in range(0, len(keywords) - 1)]
    whitespace = ' '
    keywords_splits = whitespace.join(keywords).split()

    keywords_splitter(keywords, keywords_splits)
    keywords_splits = list(set(keywords_splits + keywords))

    return keywords_splits

keywords_ip = ['stage', 'color Johnny Cash', 'wears']
document = "From 1969 to 1971, Cash starred in his own television show, The Johnny Cash Show, on the ABC network. The Statler Brothers opened up for him in every episode; the Carter Family and rockabilly legend Carl Perkins were also part of the regular show entourage. Cash also enjoyed booking mainstream performers as guests; including Neil Young, Louis Armstrong, Neil Diamond, Kenny Rogers and The First Edition (who appeared four times), James Taylor, Ray Charles, Roger Miller, Roy Orbison, Derek and the Dominos, and Bob Dylan. During the same period, he contributed the title song and other songs to the film Little Fauss and Big Halsey, which starred Robert Redford, Michael J. Pollard, and Lauren Hutton. The title song, The Ballad of Little Fauss and Big Halsey, written by Carl Perkins, was nominated for a Golden Globe award. Cash had met with Dylan in the mid-1960s and became closer friends when they were neighbors in the late 1960s in Woodstock, New York. Cash was enthusiastic about reintroducing the reclusive Dylan to his audience. Cash sang a duet with Dylan on Dylan's country album Nashville Skyline and also wrote the album's Grammy-winning liner notes. Another artist who received a major career boost from The Johnny Cash Show was Kris Kristofferson, who was beginning to make a name for himself as a singer-songwriter. During a live performance of Kristofferson's Sunday Mornin' Comin' Down, Cash refused to change the lyrics to suit network executives, singing the song with its references to marijuana intact: On a Sunday morning sidewalk I'm wishin', Lord, that I was stoned. By the early 1970s, he had crystallized his public image as The Man in Black. He regularly performed dressed all in black, wearing a long black knee-length coat. This outfit stood in contrast to the costumes worn by most of the major country acts in his day: rhinestone suits and cowboy boots. In 1971, Cash wrote the song Man in Black, to help explain his dress code: We're doing mighty fine I do suppose In our streak of lightning cars and fancy clothes But just so we're reminded of the ones who are held back He wore 'black' on behalf of the poor and hungry, on behalf of the prisoner who has long paid for his crime, and on behalf of those who have been betrayed by age or drugs. And, Cash added, with the Vietnam War as painful in my mind as it was in most other Americans, I wore it 'in mournin' for the lives that could have been' ... Apart from the Vietnam War being over, I don't see much reason to change my position ... The old are still neglected, the poor are still poor, the young are still dying before their time, and we're not making many moves to make things right. There's still plenty of darkness to carry off. He and his band had initially worn black shirts because that was the only matching color they had among their various outfits. He wore other colors on stage early in his career, but he claimed to like wearing black both on and off stage. He stated that political reasons aside, he simply liked black as his on-stage color.e needed] The outdated US Navy's winter blue uniform used to be referred to by sailors as Johnny Cashes, as the uniform's shirt, tie, and trousers are solid black. In the mid-1970s, Cash's popularity and number of hit songs began to decline. He made commercials for Amoco and STP, an unpopular enterprise at the time of the 1970s energy crisis. In 1976 he made commercials for Lionel Trains, for which he also wrote the music. However, his first autobiography, Man in Black, was published in 1975 and sold 1.3 million copies. A second, Cash: The Autobiography, appeared in 1997. His friendship with Billy Graham  led to the production of a film about the life of Jesus, The Gospel Road, which Cash co-wrote and narrated. Cash and June Carter Cash appeared several times on the Billy Graham Crusade TV specials, and Cash continued to include gospel and religious songs on many of his albums, though Columbia declined to release A Believer Sings the Truth, a gospel double-LP Cash recorded in 1979 and which ended up being released on an independent label even with Cash still under contract to Columbia. On November 22, 1974, CBS ran his one-hour TV special entitled Riding The Rails, a musical history of trains."

ranked_pages = [(0, 0.22592135), (3, 0.21375993), (2, 0.14056443)]

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + document)

keywords_query = pre_query(keywords_ip)
print(keywords_query)

sentences = list(en_doc.sents)

corpus, dictionary = doc2vec(sentences)

query_corpus = query2vec(keywords_query, dictionary)



corpus_lsidf, query_lsidf = transform_vec(corpus, query_corpus)

simi_sorted = similariy(corpus_lsidf, query_lsidf)

simi_sorted = simi_sorted[0:10]

for sent in simi_sorted:
    sent_id = sent[0]
    print(sent_id, sentences[sent_id])