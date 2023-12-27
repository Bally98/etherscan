from web3 import Web3
from datetime import datetime, timedelta
import json

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/bcd33d492a174c4fbb9a4d321c24ebe0'))

contract_address = '0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0'
abi_file = 'abi.json'
with open(abi_file, 'r') as abi:
   contract_abi = json.load(abi)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
now = datetime.now()
start_time = int((now - timedelta(days=1)).timestamp())
end_time = int(now.timestamp())

events = contract.events.TotalDistribution.create_filter(
        fromBlock=start_time,
        toBlock=end_time
    ).get_all_entries()

print(events)
