import sys
import logging
from enum import Enum
from datetime import datetime, timedelta, UTC

from eth_typing import Address

from models import (
    Treasury,
    SolverBond,
    StakingContract,
    VestingSchedule,
    Token,
)
from vesting import linear_vesting

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def _addr(hex_str: str) -> Address:
    return Address(bytes.fromhex(hex_str[2:]))


# add all different chains for token here
class TOKENS(Enum):
    COW_MAINNET = Token(
        rpc_url_env_var="ETH_RPC_URL",
        token_contract=_addr("0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"),
        # Mainnet is the canonical source of total supply: COW on Gnosis
        # Chain is a bridged representation of the same supply and must not
        # be double-counted.
        include_in_max_supply=True,
    )
    COW_GNOSIS = Token(
        rpc_url_env_var="GNOSIS_RPC_URL",
        token_contract=_addr("0x177127622c4A00F3d409B75571e12cB3c8973d3c"),
        include_in_max_supply=False,
    )


# add all treasuries here
class TREASURIES(Enum):
    COW_DAO_TREASURY_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0xcA771eda0c70aA7d053aB1B25004559B918FE662"),
    )
    COW_DAO_TREASURY_SAFE_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669"),
    )
    COW_DAO_TREASURY_BUYBACK_RECEPIENT_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0xA2BFc70e63a48BDfc3F8013a44B04b6c33fb8200"),
    )
    COW_DAO_TREASURY_TWAP_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0x523732d31B4432BcDD4BaaD108f7EBE54AD478b0"),
    )
    COW_DAO_TREASURY_FUNDING_MODULE_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0x324E12107EC7a89e94dD1c07B7d8781406db3e1D"),
    )
    COW_DAO_TREASURY_SOLVER_REWARDS_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0xA03be496e67Ec29bC62F01a428683D7F9c204930"),
    )
    # "CoW Treasury" operational wallet for idle reserves / OTC / liquidity
    # provision, referenced as ~59M COW in the Core Team forum post but
    # currently holding ~27.7M. Funded entirely from the CoW DAO Safe and
    # Treasury Safe (verified via on-chain transfer history Apr–May 2026).
    COW_DAO_TREASURY_OPERATIONS_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET,
        treasury_addess=_addr("0x486c2B52FfbeD401b16ce39b7Ab9E2Ebf56D650f"),
    )

    # Multi-chain treasury holdings. The CoW DAO Safe and several auxiliary
    # safes are deployed at the same address on Gnosis Chain via the Safe
    # Singleton Factory; their balances must be excluded from circulating
    # supply per the Core Team methodology update.
    COW_DAO_TREASURY_GNOSIS = Treasury(
        token=TOKENS.COW_GNOSIS,
        treasury_addess=_addr("0xcA771eda0c70aA7d053aB1B25004559B918FE662"),
    )

    # Multi-chain treasury holdings. The Treasury Safe is deployed at the
    # same address on Gnosis Chain via the Safe Singleton Factory; its
    # balance must be excluded from circulating supply per the Core Team
    # methodology update. The DAO Treasury Safe is also deployed on Gnosis
    # but currently holds only dust (~1 COW) and is therefore omitted.
    COW_DAO_TREASURY_SAFE_GNOSIS = Treasury(
        token=TOKENS.COW_GNOSIS,
        treasury_addess=_addr("0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669"),
    )


# Solver bonds — wallets posting COW as bond collateral against solver
# misbehaviour. Per the Core Team methodology, these ~10M COW are excluded
# from circulating supply.
#
# Sources:
#   https://forum.cow.fi/t/cow-daos-path-to-value-distribution-core-team-view/3454
class BONDS(Enum):
    SOLVER_BOND_COW = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x5d4020b9261F01B6f8a45db929704b0Ad6F5e9E6"),
    )
    SOLVER_BOND_GNOSIS = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x7489f267C3b43dc76e4cb190F7B55ab3297706AF"),
    )
    SOLVER_BOND_RIZZOLVER = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x0deb0ae9c4399c51289adb1f3ed83557a56df657"),
    )
    SOLVER_BOND_FRACTAL = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x7719c9C0D35D460b00487A1744394E9525e8a42C"),
    )
    SOLVER_BOND_TSOLVER = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x8C77268262Cd0de611e543dfD7E9b496793ACb86"),
    )

    # Reduced bonding pools (CIP-44). Each is a Safe with only the CoW DAO
    # Solver Payouts safe (0xA03be496…4930) as signer, funded with 500K COW
    # initially and ramping to 1M COW per the bonding_pools docs. Enumerated
    # via Safe Transaction Service: every Safe owned by the Payouts safe
    # that holds 400K–1.1M COW is a reduced bonding pool.
    SOLVER_BOND_REDUCED_1 = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x3075F6aab29D92F8F062A83A0318c52c16E69a60"),
    )
    SOLVER_BOND_REDUCED_2 = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0xB6113c260aD0a8A086f1E31c5C92455252A53Fb8"),
    )
    SOLVER_BOND_REDUCED_3 = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x0A9BD5A29E49502CdC100Aa364C5de3b436e52c9"),
    )
    SOLVER_BOND_REDUCED_4 = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0xD5630C50a8aa4599dF155D155Cb960f8F2828242"),
    )
    SOLVER_BOND_REDUCED_5 = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x271ea2AA9ED4299C85C621bc7A46d90ed4d5032a"),
    )
    SOLVER_BOND_REDUCED_6 = SolverBond(
        token=TOKENS.COW_MAINNET,
        bond_address=_addr("0x2341011c8F4e49c2622Ad64ae6119EbBaf36D676"),
    )


# Staking contracts holding COW that is locked under the upcoming staking
# program. No contract has been deployed at the time of this change; the
# enum is intentionally empty so the supply pipeline picks up new entries
# automatically once an address is added.
class STAKING_CONTRACTS(Enum):
    pass


# add all vesting schedules here
VESTING_SCHEDULES: list[VestingSchedule] = [
    VestingSchedule(
        name="CoW Protocol Virtual Token ETH",
        vesting_start=datetime.fromtimestamp(1644609915, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        # https://etherscan.io/tx/0x1100cd4a50a2c224ec39f861aef7574df394edb2b5ed850705cf0bb34f6a300d
        full_amount=439952166809283833193827347,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="CoW Protocol Virtual Token GNOSIS",
        vesting_start=datetime.fromtimestamp(1644610920, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        # https://gnosisscan.io/tx/0x3cb8cf2affc63d897e9efa9882a194a1ce809e88be82a8cbc4bc63eed897550e
        full_amount=34850471096742687083022409,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="GNOSIS DAO allocation ETH",
        vesting_start=datetime.fromtimestamp(1644584715, tz=UTC),
        vesting_duration=timedelta(days=365 * 4),
        # https://etherscan.io/tx/0x0e105389f5bc8ded16723ac44e231a8e484eab28da4113a8fd3892624a364882
        full_amount=41894957000000000000000000,
        vesting_model=linear_vesting,
    ),
]
