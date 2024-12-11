import subprocess
from typing import Dict
from pprint import pprint

# import requests
# import toml
# import threading
# import datetime
# import os
import json
import time

from constants import *
from states import *


def GetGenesisAccAddress():
    command = f"rollapp-wasm keys show {GENESIS_ACCOUNT_NAME} --keyring-backend test --output json"
    output = subprocess.getstatusoutput(command)[1]
    output = json.loads(output)
    return output["address"]


def GetContractAddress(codeID):
    command = f"rollapp-wasm q wasm list-contract-by-code {codeID} --output json --node {NODE}"
    result = subprocess.getstatusoutput(command)
    if result[0] != 0:
        print(f"error in fetching last contract code: {result[1]}")
        exit(result[0])
    resp = json.loads(result[1])
    return resp["contracts"][0]


def GetLastContractCodeID():
    command = f"rollapp-wasm q wasm list-code --output json --node {NODE}"
    result = subprocess.getstatusoutput(command)
    if result[0] != 0:
        print(f"error in fetching last contract code: {result[1]}")
        exit(result[0])
    resp = json.loads(result[1])
    return int(resp["code_infos"][-1]["code_id"])


def StoreAndIntantiateWasmContract():
    print("Storing & Instantiating code")
    contractAddresses = {}
    for _, contractData in enumerate(WASM_CONTRACTS):
        print(f"\nStoring {contractData['name']} ....")
        time.sleep(6)
        command = f"rollapp-wasm tx wasm store {contractData['contractPath']} --from {GENESIS_ACCOUNT_NAME} --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test --node {NODE} -y  --output json --fees {FEE} "
        output = subprocess.getstatusoutput(command)
        output = json.loads(output[1])
        if int(output["code"]) != 0:
            print(output)
            exit(f"error in adding {contractData['name']}")
        print(f"{contractData['name']} added successfully ✔️")

        for keys in contractData["formatKeys"]:
            contractData["initator"][keys] = contractAddresses[keys]

        time.sleep(6)
        currentCodeID = GetLastContractCodeID()
        command = f"""rollapp-wasm tx wasm instantiate {currentCodeID} '{json.dumps(contractData['initator'])}' --label "Instantiate {contractData['name']}" --no-admin --from {GENESIS_ACCOUNT_NAME} --chain-id {CHAIN_ID} --node {NODE} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test -y  --output json --fees {FEE} """
        output = subprocess.getstatusoutput(command)
        if int(output[0]) != 0:
            print(output)
            exit(f"error in instantiating {contractData['name']}")
        output = subprocess.getstatusoutput(command)[1]
        output = json.loads(output)
        if int(output["code"]) != 0:
            print(output)
            exit(f"error in instantiating {contractData['name']}")
        print(f"{contractData['name']} instantiated successfully ✔️")
        time.sleep(6)
        contractAddresses[contractData["contractAddressKey"]] = GetContractAddress(
            currentCodeID
        )
    print("all contract added and instantiated successfully ✔️")
    return contractAddresses


def WhitelistGamesInBank(contractAddresses: Dict[str, str]):
    print("Whitelisting Games in Bank")
    bank_contract = contractAddresses["bank_addr"]

    for contractAddressKey, contractAddress in contractAddresses.items():
        if (
            contractAddressKey.startswith("random")
            or contractAddressKey.startswith("callback")
            or contractAddressKey.startswith("bank")
        ):
            continue
        print(f"\nRegistering {contractAddressKey}")

        EXECUTEMSG = {
            "whitelist_game": {
                "game_name": f"{contractAddressKey}",
                "game": f"{contractAddress}",
            }
        }
        command = f"rollapp-wasm tx wasm execute {bank_contract} '{json.dumps(EXECUTEMSG)}' --from {GENESIS_ACCOUNT_NAME}  --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test  -y  --output json --node {NODE} --fees {FEE}"
        output = subprocess.getstatusoutput(command)[1]
        output = json.loads(output)

        if int(output["code"]) != 0:
            print(output)
            exit(f"error in whitelisting {contractAddressKey}")
        print(f"{contractAddressKey} registered successfully ✔️")
    return


def RegisterCallbacks(contractsAddresses: Dict[str, str]):
    print("Registering contracts in callback")
    callback_contract = contractsAddresses["callback_contract"]

    for _, contractData in enumerate(WASM_CONTRACTS):
        if contractData["contractAddressKey"].startswith("random") or contractData[
            "contractAddressKey"
        ].startswith("callback"):
            continue
        print(f"\nRegistering {contractData['contractAddressKey']}")
        EXECUTEMSG = {
            "add_game": {
                "game_name": f"{contractData['contractAddressKey']}",
                "callback_ids": contractData["callbackIds"],
                "address": f"{contractsAddresses[contractData['contractAddressKey']]}",
            },
        }
        if contractData["contractAddressKey"] == "bank_addr":
            EXECUTEMSG["add_game"]["game_name"] = "bank"

        command = f"rollapp-wasm tx wasm execute {callback_contract} '{json.dumps(EXECUTEMSG)}' --from {GENESIS_ACCOUNT_NAME}  --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test  -y  --output json --node {NODE} --fees {FEE}"

        output = subprocess.getstatusoutput(command)[1]
        output = json.loads(output)

        if int(output["code"]) != 0:
            print(output)
            exit(f"error in registering {contractData['contractAddressKey']}")
        print(f"{contractData['contractAddressKey']} registered successfully ✔️")
        time.sleep(2)
    return


def WhitelistAssetInBank(contractAddress: str, assetData: Dict[str, str]):
    print(f"\nWhitelisting {assetData['denom']} in bank")
    EXECUTEMSG = {
        "whitelist_asset": {
            "asset": {
                "id": assetData["id"],
                "denom": assetData["denom"],
                "decimals": assetData["decimals"],
            },
        },
    }
    command = f"rollapp-wasm tx wasm execute {contractAddress} '{json.dumps(EXECUTEMSG)}' --from {GENESIS_ACCOUNT_NAME}  --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test  -y  --output json --node {NODE} --fees {FEE}"

    output = subprocess.getstatusoutput(command)
    if output[0] != 0:
        print(output)
        exit(f"error in whitelisting {assetData['denom']}")
    output = output[1]
    output = json.loads(output)

    if int(output["code"]) != 0:
        print(output)
        exit(f"error in whitelisting {assetData['denom']}")
    print(f"{assetData['denom']} whitelisted successfully ✔️")
    return


def SetMinBetInContracts(contractAddresses: Dict[str, str], assetData: Dict[str, str]):
    for contractAddressKey, contractAddress in contractAddresses.items():
        if contractAddressKey.startswith("random") or contractAddressKey.startswith("callback") or contractAddressKey.startswith("bank"):
            continue
        print(f"\nSetting Min bet for {assetData['denom']} in {contractAddressKey}")
        EXECUTEMSG = {
            "update_min_bet": {
                "denom": f"{assetData['denom']}",
                "amount": f"{assetData['min_bet']}",
            },
        }
        command = f"rollapp-wasm tx wasm execute {contractAddress} '{json.dumps(EXECUTEMSG)}' --from {GENESIS_ACCOUNT_NAME}  --chain-id {CHAIN_ID} --gas 5000000 --gas-adjustment 1.3 --keyring-backend test  -y  --output json --node {NODE} --fees {FEE}"

        output = subprocess.getstatusoutput(command)
        if output[0] != 0:
            print(output)
            exit(f"error in setting min bet in {contractAddressKey}")

        output = output[1]
        output = json.loads(output)
        if int(output["code"]) != 0:
            print(output)
            exit(f"error in whitelisting {assetData['denom']}")
        print(f"{contractAddressKey} Min Bet updated successfully ✔️")
    return


def WhitelistAssetAndSetMinBet(contractAddresses: Dict[str, str]):
    bank_contract = contractAddresses["bank_addr"]
    for _, assetData in enumerate(WHITELIST_ASSET):
        WhitelistAssetInBank(bank_contract, assetData)
        SetMinBetInContracts(contractAddresses, assetData)
        time.sleep(2)
    return


def main():
    CreateState()
    return


def CreateState():
    contractAddresses = StoreAndIntantiateWasmContract()
    pprint(contractAddresses)
    RegisterCallbacks(contractAddresses)
    WhitelistGamesInBank(contractAddresses)
    RegisterCallbacks(contractAddresses)
    WhitelistGamesInBank(contractAddresses)
    WhitelistAssetAndSetMinBet(contractAddresses)
    return


def manual_labour():
    contractAddresses = {
        "random_addr": "allin1wr6vc3g4caz9aclgjacxewr0pjlre9wl2uhq73rp8mawwmqaczsql3t5kj",
        "callback_contract": "allin1ul4msjc3mmaxsscdgdtjds85rg50qrepvrczp0ldgma5mm9xv8yqg8uqzl",
        "bank_addr": "allin1nqrmxvqep7pg47aln823h75txe856kln37ghpkkvhjyx3qw2prysplq9k9",
        "andarbahar": "allin1j30wx6kjfsessdx5mlp32hqwklj48ufvtve50ymzg7dc6870sw3s7tzqjj",
        "baccarat": "allin1utve8x4s2jq8wua78mtagwusyu0u64ldlx9sc8pff00077rhqwdsy3pp7c",
        "classicdice": "allin12xk7d7lksh6z94vvt4qqur765trqdcn7w86mfak62qjz63zvmhvshzpmvq",
        "coinflip": "allin1nyuryl5u5z04dx4zsqgvsuw7fe8gl2f77yufynauuhklnnmnjncqn7q6vh",
        "dragontiger": "allin1wfa20sv00kpgnj38j3akds2m64pvk7yrhylgyj7587lyl8mtc8xsahyw3n",
        "hashdice": "allin1xc3n6fauf3gaug26jh5qtfuv256x6why6tcsfyztwh59gm85j30qcatnd6",
        "roulette": "allin1pg4dxed60q3w5a6dy8ca84q7wa7d9qm0amxw5j7zmwcpvgefg6xsulr87g",
        "sevenupsevendown": "allin13gmz4njttq7f5tahn8077n4waljjfucsuatd28h9zrxr9g4lg2tsf4vt6f",
        "slots": "allin105ml67ymwlznz8twk2nyxu5xaqnsp2h24t50995ucp8ffu5wut7qpc7z4s",
    }
    # RegisterCallbacks(contractAddresses)
    # WhitelistGamesInBank(contractAddresses)
    WhitelistAssetAndSetMinBet(contractAddresses)
    return


manual_labour()
# main()
