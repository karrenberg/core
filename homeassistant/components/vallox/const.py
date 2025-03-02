"""Constants for the Vallox integration."""

from datetime import timedelta
from typing import Final

from vallox_websocket_api import (
    Profile,
    CellState,
    SupplyHeatingAdjustMode,
    DefrostMode,
)

DOMAIN = "vallox"
DEFAULT_NAME = "Vallox"

STATE_SCAN_INTERVAL = timedelta(seconds=60)

# Common metric keys and (default) values.
METRIC_KEY_MODE = "A_CYC_MODE"
METRIC_KEY_PROFILE_FAN_SPEED_HOME = "A_CYC_HOME_SPEED_SETTING"
METRIC_KEY_PROFILE_FAN_SPEED_AWAY = "A_CYC_AWAY_SPEED_SETTING"
METRIC_KEY_PROFILE_FAN_SPEED_BOOST = "A_CYC_BOOST_SPEED_SETTING"

MODE_ON = 0
MODE_OFF = 5

DEFAULT_FAN_SPEED_HOME = 50
DEFAULT_FAN_SPEED_AWAY = 25
DEFAULT_FAN_SPEED_BOOST = 65

I18N_KEY_TO_VALLOX_PROFILE: Final = {
    "home": Profile.HOME,
    "away": Profile.AWAY,
    "boost": Profile.BOOST,
    "fireplace": Profile.FIREPLACE,
    "extra": Profile.EXTRA,
}

VALLOX_PROFILE_TO_PRESET_MODE: Final = {
    Profile.HOME: "Home",
    Profile.AWAY: "Away",
    Profile.BOOST: "Boost",
    Profile.FIREPLACE: "Fireplace",
    Profile.EXTRA: "Extra",
}

PRESET_MODE_TO_VALLOX_PROFILE: Final = {
    value: key for (key, value) in VALLOX_PROFILE_TO_PRESET_MODE.items()
}

VALLOX_CELL_STATE_TO_STR: Final = {
    CellState.HEAT_RECOVERY: "HeatReco", # C_CYC_CELL_STATE_HEATRECO
    CellState.COOL_RECOVERY: "CoolReco", # C_CYC_CELL_STATE_COOLRECO
    CellState.BYPASS:        "Bypass",   # C_CYC_CELL_STATE_BYPASS
    CellState.DEFROST:       "Defrost",  # C_CYC_CELL_STATE_DEFROST
}

VALLOX_DEFROST_MODE_TO_STR: Final = {
    DefrostMode.BYPASS:   "Bypass",  # C_CYC_BYPASS_MODE
    DefrostMode.FAN_STOP: "Fanstop", # C_CYC_FAN_STOP_MODE
}

VALLOX_DEFROST_MODE_FROM_STR = {v: k for k, v in VALLOX_DEFROST_MODE_TO_STR.items()}

VALLOX_SUPPLY_HEATING_ADJUST_MODE_TO_STR: Final = {
    SupplyHeatingAdjustMode.SUPPLY: "Supply",   # C_CYC_HEATING_SUPPLY
    SupplyHeatingAdjustMode.EXTRACT: "Extract", # C_CYC_HEATING_HEATING
    SupplyHeatingAdjustMode.COOLING: "Cooling", # C_CYC_HEATING_COOLING
}

VALLOX_SUPPLY_HEATING_ADJUST_MODE_FROM_STR = {v: k for k, v in VALLOX_SUPPLY_HEATING_ADJUST_MODE_TO_STR.items()}
