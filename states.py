from constants import *

WASM_CONTRACTS = [
    {
        "name": "Vesting Contract",
        "contractAddressKey": "vesting_contract",
        "contractPath": f"./token_vesting.wasm",
        "initator": {},
        "formatKeys": []
    },
    {
        "name": "Locking Contract",
        "contractAddressKey": "locking_contract",
        "contractPath": f"./locking_contract.wasm",
        "initator": {
            "t1": {"period": 500, "weight": "0.25"},
            "t2": {"period": 1000, "weight": "0.50"},
            "voting_period": 122500,
            "vesting_contract": "",
            "foundation_addr": ["aallin1rljg3wwgv6qezu3p05vxny9pwk3mdwl0ja407z"],
            "foundation_percentage": "0.2",
            "surplus_asset_id": 3,
            "emission": {
                "app_id": 1,
                "total_rewards": "10000000000000",
                "rewards_pending": "10000000000000",
                "emission_rate": "0.01",
                "distributed_rewards": "0",
            },
            "min_lock_amount" : "4",
            "admin":"aallin1663kc7kwlqxg5s35wuq4nleuqvy5j2tstlkeg2"
        },
        "formatKeys": ['vesting_contract']
    },
    {
        "name": "Governance Contract",
        "contractAddressKey": "governance_contract",
        "contractPath": f"./governance.wasm",
        "initator": {
            "threshold": {"threshold_quorum": {"threshold": "0.50", "quorum": "0.33"}},
            "target": "0.0.0.0:9090",
            "locking_contract": "",
        },
        "formatKeys": ['locking_contract']
    },
]