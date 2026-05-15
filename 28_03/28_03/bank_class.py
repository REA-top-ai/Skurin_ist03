from abc import ABC, abstractmethod

class BancAccount(ABC):
    @abstractmethod
    def add_money(self, amount):
        pass
    def payment(self, amount):
        pass

class DepositBankAccount(BancAccount):
    def __init__(self,name,bank_id):
        self.__name = name
        self.__balance = 0
        self.__id = bank_id

    def add_money(self, amount):
        self.__balance += amount
        print(f"Client {self.__name} add {amount}. Balance is {self.__balance}")

    def payment(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"Client {self.__name} pay {amount}. Balance is {self.__balance}")
        else:
            print(f"Not enough money. Balance is {self.__balance}")


class Client:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def create_account(self, bank_id):
        new_account = DepositBankAccount(self.name, bank_id)
        self.accounts.append(new_account)