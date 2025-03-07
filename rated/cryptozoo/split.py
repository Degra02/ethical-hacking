
zoo = b'pet=BillTheRock|Kb\xca0\x8bB\x19l\xb7\x87\xef\x0e\xa0\xc9\x17\xb4pet=rubberduck|Ay\xaaS(J\xfc\x11Ii\xb7\xb7\xfd\xb0\x82\xd2\x0c|pet=Ferris|heprill'


pets = zoo.split(b"|")
print(pets)

found_pets = []
for pet in pets:
    pieces = pet.split(b"=")
    if pieces[0] == b"pet":
        found_pets.append(pieces[1])

print(found_pets)
