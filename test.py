from mtgsdk import Card

testCard = Card.where(name="Attrition").all()
for i in testCard:
    print(i.name)