from mtgsdk import Card

testCard = Card.where(name="Attrition").all()[0]
# print(dict(vars(testCard)))

card = dict(vars(testCard))

print(card)