from bank_class import Client
from datetime import datetime

def create_id():
    return datetime.now().timestamp() * 1000000

def main():
    client1 = Client('Alice')
    client2 = Client('Bob')

    client1.create_account(create_id)
    client2.create_account(create_id)
    client1.accounts[0].add_money(200)


if __name__ == '__main__':
    main()