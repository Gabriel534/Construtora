from abc import ABC, abstractmethod
import doctest as d
import unittest as u


class Pai(ABC, metaclass=type):
    @abstractmethod
    def __init__(self):
        print("Iniciado")

    def A(self) -> None:
        print("A")

    def retornaPai(self):
        return super()


class Filho(Pai):
    def __init__(self):
        """
        >>> 1+1
        2

        >>> 2+3
        6
        """
        super().__init__()
        pai = super().retornaPai()
        print(pai)


class Teste(u.TestCase):
    def test_tendas(self):
        a = Filho()
        a.A()

    def test_listasNãoSãoIguais(self):
        lista1 = [1, 2, 3, 4, 5]
        lista2 = [1, 2, 3, 4, 5]
        dicio = {a: lista2[lista1.index(a)] for a in lista1}
        for entrada, saida in dicio.items():
            with self.subTest(entrada=entrada, saida=saida):
                assert (entrada == saida), "a"


# d.testmod(verbose=True)
u.main(verbosity=True)
