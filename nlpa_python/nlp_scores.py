import spacy
from spacy.scorer import Scorer
from spacy.tokens import Doc
from spacy.training.example import Example

examples = [
    ('Who is Talha Tayyab?',
     {(7, 19, 'PERSON')}),
    ('I like London and Berlin.',
     {(7, 13, 'LOC'), (18, 24, 'LOC')}),
     ('Agra is famous for Tajmahal, The CEO of Facebook will visit India shortly to meet Murari Mahaseth and to visit Tajmahal.',
     {(0, 4, 'LOC'), (40, 48, 'ORG'), (60, 65, 'GPE'), (82, 97, 'PERSON'), (111, 119, 'GPE')})
]

def my_evaluate(ner_model, examples):
    scorer = Scorer()
    example = []
    for input_, annotations in examples:
        pred = ner_model(input_)
        print(pred,annotations)
        temp = Example.from_dict(pred, dict.fromkeys(annotations))
        example.append(temp)
    scores = scorer.score(example)
    return scores

ner_model = spacy.load('en_core_web_sm') # for spaCy's pretrained use 'en_core_web_sm'
results = my_evaluate(ner_model, examples)
print(results)