from nltk import CFG
grammar=    CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

print(grammar)
print(grammar.start())
print(grammar.productions())
print(grammar.productions(rhs='elephant'))

