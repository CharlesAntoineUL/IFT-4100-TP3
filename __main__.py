from web3 import Web3
from getpass import getpass
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open('./build/contracts/CarRental.json', 'r') as file:
    contract_data  = json.load(file)
abi = contract_data['abi']
contract_address = Web3.to_checksum_address('0x73417e58d378f5fa36399d83100d9f5fd2cdb68a') # Pas trouvé comment incrire cette info dynamiquement

contract = web3.eth.contract(address=contract_address, abi=abi)
print("Login to your account. ")
account = input("Enter your account address : ")
password = input("Enter your private key : ")

def get_car(car_id):
    car = contract.functions.getCar(car_id).call()
    print("Car ID:", car[0])
    print("Owner:", car[1])
    print("Brand:", car[2])
    print("Model:", car[3])
    print("Year of Construction:", car[4])
    print("Rental Price per Day:", car[5])
    print("Is Rented:", car[6])

def add_car(brand, model, year_of_construction, rental_price):
    transaction = contract.functions.addCar(brand, model, year_of_construction, rental_price).build_transaction({
        'from': account,
        'nonce' : web3.eth.get_transaction_count(account),
        'gas': 3000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=password)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Transaction sent. Hash:", web3.to_hex(tx_hash))

def rent_car(car_id, num_days, value):
    transaction = contract.functions.rentCar(car_id, num_days).build_transaction({
        'from': account,
        'nonce' : web3.eth.get_transaction_count(account),
        'value': web3.to_wei(value, 'ether'),
        'gas': 3000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=password)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Transaction sent. Hash:", web3.to_hex(tx_hash))

def return_car(car_id):
    transaction = contract.functions.returnCar(car_id).build_transaction({
        'from': account,
        'nonce' : web3.eth.get_transaction_count(account),
        'gas': 3000000, 
        'gasPrice': web3.to_wei('50', 'gwei') 
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=password)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Transaction sent. Hash:", web3.to_hex(tx_hash))

def remove_car(car_id):
    transaction = contract.functions.removeCar(car_id).build_transaction({
        'from': account,
        'nonce' : web3.eth.get_transaction_count(account),
        'gas': 3000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=password)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Transaction sent. Hash:", web3.to_hex(tx_hash))

while True:
    print("\n1. Rent a car")
    print("2. Return a car")
    print("3. Add a car")
    print("4. Get car information")
    print("5. Remove a car")
    print("0. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        car_id = int(input("Enter car ID: "))
        num_days = int(input("Enter number of days to rent: "))
        value = float(input("Enter rental value in Ether: "))
        rent_car(car_id, num_days, value)
    elif choice == '2':
        car_id = int(input("Enter car ID: "))
        return_car(car_id)
    elif choice == '3':
        brand = input("Enter car brand: ")
        model = input("Enter car model: ")
        year_of_construction = input("Enter year of construction: ")
        rental_price = int(input("Enter rental price per day in Wei: "))
        add_car(brand, model, year_of_construction, rental_price)
    elif choice == '4':
        car_id = int(input("Enter car ID: "))
        get_car(car_id)
    elif choice == '5':
        car_id = int(input("Enter car ID: "))
        remove_car(car_id)
    elif choice == '0':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
