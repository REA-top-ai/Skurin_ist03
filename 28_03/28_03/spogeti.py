client1 = 'Alice'
client_1_balance = 1000

client2 = 'Bob'
client_2_balance = 500

amount = 200
client_1_balance += amount
print(f"Client {client1} add {amount}. Balance is {client_1_balance}")

amount = 300
client_2_balance += amount
print(f"Client {client2} add {amount}. Balance is {client_2_balance}")

amount = 200
if client_2_balance >= amount:
    client_2_balance -= amount
    print(f"Client {client2} pay {amount}. Balance is {client_2_balance}")
else:
    print(f"Not enough money. Balance is {client_2_balance}")

amount = 300
if client_1_balance >= amount:
    client_1_balance -= amount
    print(f"Client {client1} pay {amount}. Balance is {client_1_balance}")
else:
    print(f"Not enough money. Balance is {client_1_balance}")