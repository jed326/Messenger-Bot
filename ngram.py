import re, string, random, math
import pickle
from collections import deque


def tokenize(text):
    return re.findall(r"[\w]+|[" + string.punctuation + "]", text)


def ngrams(n, tokens):
    tokens = ['<START>'] * (n - 1) + tokens + ['<END>']
    return [(tuple(tokens[start:start + n - 1]), tokens[start + n - 1])
            for start in range(len(tokens) - n + 1)]


class NgramModel(object):
    def __init__(self, n):
        self._order = n
        self._counts = dict()
        self._context_counts = dict()

    def update(self, sentence):
        update = ngrams(self._order, tokenize(sentence))
        for i in update:
            self._counts[i] = self._counts.get(i, 0) + 1
            self._context_counts[i[0]] = self._context_counts.get(i[0], 0) + 1

    def prob(self, context, token):
        return float(self._counts.get(
            (context, token), 0)) / float(self._context_counts[context])

    def random_token(self, context):
        r = random.random()
        words = sorted([x[1] for x in set(self._counts) if context == x[0]])
        prob_sum = 0
        for word in words:
            prob_sum += self.prob(context, word)
            if prob_sum > r:
                return word

    def random_text(self, token_count):
        sentence = []
        context = tuple((self._order - 1) * ["<START>"])
        context_deque = deque(context)
        for _ in range(token_count):
            word = self.random_token(tuple(context_deque))
            sentence.append(word)
            if word == "<END>":
                context_deque = deque(context)
            elif self._order > 1:
                context_deque.popleft()
                context_deque.append(word)
        return " ".join(sentence).replace(" <END>", "")

    def perplexity(self, sentence):
        tokens = tokenize(sentence)
        NG = ngrams(self._order, tokens)
        log_prod = sum(
            math.log(1 / self.prob(gram[0], gram[1])) for gram in NG)

        return math.exp(log_prod)**(1 / float(len(tokens) + 1))


def create_ngram_model(n, path):
    with open(path, "r") as file:
        text = [x[:-1] for x in file.readlines()]
    m = NgramModel(n)
    for line in text:
        m.update(line)
    return m