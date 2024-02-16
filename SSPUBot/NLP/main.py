# --encoding:utf-8--
from snownlp import SnowNLP


def main():
    goto = False
    text = open('test.txt', 'r', encoding='utf-8').read()
    keywordsNeed = open('keywordsNeed.txt', 'r', encoding='utf-8').read().split('\n')
    keywordsNotNeed = open("keywordsNotNeed.txt", 'r', encoding='utf-8').read().split('\n')
    snownlp = SnowNLP(text)
    sentences = snownlp.sentences
    sentencesBest = []
    for sentence in sentences:
        for wordNotNeed in keywordsNotNeed:
            if wordNotNeed in sentence:
                sentences.remove(sentence)
                goto = True
        if goto:
            continue
        for wordNeed in keywordsNeed:
            if wordNeed in sentence:
                sentencesBest.append(sentence)
                break
    return sentencesBest


if __name__ == '__main__':
    sentence = main()
    print(sentence)
