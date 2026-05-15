client1 = 'Alice'
client_1_balance = 1000

client2 = 'Bob'
client_2_balance = 500

def add_money(amount,client, client_balance):
    client_balance += amount
    print(f"Client {client} add {amount}. Balance is {client_balance}")
    return client_balance


def payment(amount, client, client_balance):
    if client_balance >= amount:
        client_balance -= amount
        print(f"Client {client} pay {amount}. Balance is {client_balance}")
    else:
        print(f"Not enough money. Balance is {client_balance}")
    return client_balance

if __name__ == '__main__':
    client1 = 'Alice'
    client_1_balance = 1000
    client2 = 'Bob'
    client_2_balance = 500
    client_1_balance = add_money(200, client1, client_1_balance)
    client_2_balance = add_money(300, client2, client_2_balance)
    client_1_balance = payment(300, client1, client_1_balance)
    client_2_balance = payment(200, client2, client_2_balance)