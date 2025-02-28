from typing import Optional
from datetime import datetime, timedelta


def linear_vesting(
    full_amount: int,
    start_date: datetime,
    full_vesting_time: timedelta,
    retrieval_date: datetime,
    interval: Optional[timedelta],
) -> int:
    if interval:
        raise NotImplementedError(
            "Linear Vesting with custom interval haven't been implemted yet."
        )

    full_vesting_time_in_seconds: float = full_vesting_time.total_seconds()
    seconds_passed_since_start: float = (retrieval_date - start_date).total_seconds()

    vested_portion: float = min(
        1, seconds_passed_since_start / full_vesting_time_in_seconds
    )

    return int(full_amount * vested_portion)
