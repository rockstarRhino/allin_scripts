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
    for wasmProp in WASM_PROPOSALS:
        time.sleep(10)
        contractAddress = contractAddresses[wasmProp['contractAddressKey']]
        ProposeWasmProposal(contractAddress, wasmProp['content'], wasmProp['proposalID'])
        print(f"waiting for wasm prop {wasmProp['proposalID']}")
        if wasmProp['isProposal']:
            time.sleep(20) # waiting for proposal duration
            ExecuteWasmGovernanceProposal(contractAddress, wasmProp['proposalID'])

    chunks = [
        {
            "fromAcc" : "hotuser",
            "appID" : 2,
            "pairID" : 1,
            "direction" : "sell",
            "offerCoin" : "20000000ucmdx",
            "demandCoinDenom" : "uharbor",
            "price" : 2,
            "amount" : 10000000
        },
        {
            "fromAcc" : "cooluser",
            "appID" : 2,
            "pairID" : 1,
            "direction" : "sell",
            "offerCoin" : "20000000ucmdx",
            "demandCoinDenom" : "uharbor",
            "price" : 2,
            "amount" : 10000000
        },
        {
            "fromAcc" : "chilluser",
            "appID" : 2,
            "pairID" : 1,
            "direction" : "sell",
            "offerCoin" : "20000000ucmdx",
            "demandCoinDenom" : "uharbor",
            "price" : 2,
            "amount" : 10000000
        }
    ]
    threads = []
    for data in chunks:
        threads.append(threading.Thread(target=thread, args=(data["fromAcc"], data["appID"], data["pairID"], data["direction"], data["offerCoin"], data["demandCoinDenom"], data["price"], data["amount"])))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def main():
    CreateState()

main()