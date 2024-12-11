from constants import *

OWNER = "allin1fjagp95gq64etyvh450gzah8zlh9w7k0h5rd6z"  # IMPORTANT
BONUS = (
    "allin1dzrkwqyvs6xe5um9pt56m35kw26075fxv0u930"  # COLLECTED WAGER FEE IS SENT HERE
)
ALLIN = ""  # MINT/BURN

# Note on callbackIds:
# - 2 is resolve_bet
# - 3 is new_multiplayer_setup
# - 4 is resolve_multiplayer_bet

WASM_CONTRACTS = [
    {
        "name": "Random Contract",
        "contractAddressKey": "random_addr",
        "contractPath": f"../random-new/artifacts/random_new.wasm",
        "initator": {},
        "formatKeys": [],
    },
    {
        "name": "Callback Contract",
        "contractAddressKey": "callback_contract",
        "contractPath": f"../casino/artifacts/callback_contract.wasm",
        "initator": {
            "admin": f"{OWNER}",
        },
        "formatKeys": [],
    },
    {
        "name": "Bank Contract",
        "contractAddressKey": "bank_addr",
        "contractPath": f"../casino/artifacts/bank.wasm",
        "initator": {
            "admin": f"{OWNER}",
            "vault_info": {
                "cooloff_period": 1800,
                "max_wager_fee": "0.1",
                "wager_fee": "0.01",
                "is_payout_enabled": True,
                "is_deposit_enabled": True,
                "is_withdraw_enabled": True,
                "bonus_address": f"{BONUS}",
                "primary_token": f"{ALLIN}",
                "redemption_token": "",
                "primary_token_max_wager_fee": "0.1",
                "primary_token_wager_fee": "0.01",
            },
            "lp_limit": 4000,
        },
        "formatKeys": [],
        "callbackIds": [2],
    },
    {
        "name": "Andar Bahar",
        "contractAddressKey": "andarbahar",
        "contractPath": f"../casino/artifacts/andar_bahar.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    {
        "name": "Baccarat",
        "contractAddressKey": "baccarat",
        "contractPath": f"../casino/artifacts/baccarat.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2, 3, 4],
    },
    {
        "name": "Classic Dice",
        "contractAddressKey": "classicdice",
        "contractPath": f"../casino/artifacts/classic_dice.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    {
        "name": "Coin Flip",
        "contractAddressKey": "coinflip",
        "contractPath": f"../casino/artifacts/coin_flip.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    {
        "name": "Dragon Tiger",
        "contractAddressKey": "dragontiger",
        "contractPath": f"../casino/artifacts/dragon_tiger.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    {
        "name": "Hash Dice",
        "contractAddressKey": "hashdice",
        "contractPath": f"../casino/artifacts/hash_dice.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    {
        "name": "Roulette",
        "contractAddressKey": "roulette",
        "contractPath": f"../casino/artifacts/roulette.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2, 3, 4],
    },
    {
        "name": "Seven up Seven down",
        "contractAddressKey": "sevenupsevendown",
        "contractPath": f"../casino/artifacts/sevenupsevendown.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bank_addr": "",
            "random_addr": "",
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    {
        "name": "Slots",
        "contractAddressKey": "slots",
        "contractPath": f"../casino/artifacts/slots.wasm",
        "initator": {
            "owner": f"{OWNER}",
            "bet_reel": 3,
            "bank_addr": "",
            "random_addr": "",
            "payouts": [
                "Dollar - Dollar - Dollar",
                "Cherry - Cherry - Cherry",
                "Lemon - Lemon - Lemon",
                "Lemon - Lemon - Cherry",
                "Spade - Spade - Spade",
                "Spade - Spade - Cherry",
                "Leaf - Leaf - Leaf",
                "Leaf - Leaf - Cherry",
                "Bell - Bell - Bell",
                "Bell - Bell - -",
                "Bell - - - -",
            ],
            "multiplier": [
                "100",
                "45",
                "20",
                "20",
                "12",
                "12",
                "10",
                "10",
                "5",
                "3",
                "2",
            ],
            "reel_config": [
                "Leaf",
                "Bell",
                "Spade",
                "Cherry",
                "Bell",
                "Leaf",
                "Lemon",
                "Leaf",
                "Spade",
                "Lemon",
                "Spade",
                "Bell",
                "Spade",
                "Coin",
                "Bell",
                "Dollar",
                "Lemon",
                "Cherry",
                "Leaf",
                "Bell",
            ],
        },
        "formatKeys": ["bank_addr", "random_addr"],
        "callbackIds": [2],
    },
    # {
    #     "name": "Limbo",
    #     "contractAddressKey": "limbo",
    #     "contractPath": f"../casino/artifacts/limbo.wasm",
    #     "initator": {
    #         "owner": f"{OWNER}",
    #         "bank_addr": "",
    #         "random_addr": "",
    #         "max_multiplier": "99",
    #     },
    #     "formatKeys": ["bank_addr", "random_addr"],
    #     "callbackIds": [3,4],
    # },
    # {
    #     "name": "Yolo",
    #     "contractAddressKey": "yolo",
    #     "contractPath": f"../casino/artifacts/yolo.wasm",
    #     "initator": {
    #         "owner": f"{OWNER}",
    #         "bank_addr": "",
    #         "random_addr": "",
    #         "asset": "", #denom used for betting, only single denom allowed.
    #         "multiplayer_config": {
    #             "bet_window_size": 50, # 0 - 255
    #             "resolve_window_size": 50, # 0 - 255
    #             "post_bet_window_size": 0, # 0 - 255
    #         },
    #         "commission": "100", # 100 = 1%, 10000 = 100%
    #     },
    #     "formatKeys": ["bank_addr", "random_addr"],
    #   "callbackIds": [3,4],
    # },
]

# Note:
# id & denom need be unique.

#     = 1xxx|||xxx|||xxx||| - 18
DEC18 = 1000000000000000000
DEC15 = 1000000000000000
DEC12 = 1000000000000
DEC6 = 1000000

WHITELIST_ASSET = [
    {
        "id": 0,
        "denom": "adym",
        "decimals": DEC18,
        "min_bet": DEC18,
    }
]
