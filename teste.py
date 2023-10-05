import secrets
import pprint as p
random = secrets.SystemRandom()

lista = [{"Num": random.randint(0, 10), "Extra": random.randint(
    10, 100)} for a in range(0, 10)]
p.pprint(lista)
print()
lista2 = sorted(lista, key=lambda x: x["Num"])
p.pprint(lista2)
