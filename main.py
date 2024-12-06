import subprocess
import requests
import toml
import threading
import datetime
import os
import json
import time

from constants import *
from states import *


def GetGenesisAccAddress():
    command = f"rollapp-wasm keys show {GENESIS_ACCOUNT_NAME} --keyring-backend test --output json"
    output = subprocess.getstatusoutput(command)[1]
    output = json.loads(output)
    return output["address"]


def StoreAndIntantiateWasmContract():
    contractAddresses = {}
    for index, contractData in enumerate(WASM_CONTRACTS):
        print(f"fetching test {contractData['name']} ....")
        time.sleep(6)
        command = f"rollapp-wasm tx wasm store {contractData['contractPath']} --from {GENESIS_ACCOUNT_NAME}  --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test  -y  --output json"
        output = subprocess.getstatusoutput(command)[1]
        output = json.loads(output)
        if int(output["code"]) != 0:
            print(output)
            exit(f"error in adding {contractData['name']}")
        print(f"\n{contractData['name']} added successfully ✔️")

        for keys in contractData['formatKeys']:
            contractData['initator'][keys] = contractAddresses[keys]

        time.sleep(6)
        currentCodeID = GetLastContractCodeID()
        command = f"""rollapp-wasm tx wasm instantiate {currentCodeID} '{json.dumps(contractData['initator'])}' --label "Instantiate {contractData['name']}" --no-admin --from {GENESIS_ACCOUNT_NAME} --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test -y  --output json"""
        output = subprocess.getstatusoutput(command)[1]
        output = json.loads(output)
        if int(output["code"]) != 0:
            print(output)
            exit(f"error in instantiating {contractData['name']}")
        print(f"{contractData['name']} instantiated successfully ✔️")
        time.sleep(6)
        contractAddresses[contractData['contractAddressKey']] = GetContractAddress(currentCodeID)
    print(contractAddresses)
    print("all contract added and instantiaded successfully ✔️")
    return contractAddresses


def CreateState():

    contractAddresses = StoreAndIntantiateWasmContract()
    print(contractAddresses)

def main():
    CreateState()

main()