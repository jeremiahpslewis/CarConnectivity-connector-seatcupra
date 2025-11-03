"""
Module for charging for Seat/Cupra vehicles.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from enum import Enum

from carconnectivity.charging import Charging
from carconnectivity.vehicle import ElectricVehicle
from carconnectivity.attributes import EnumAttribute, BooleanAttribute, LevelAttribute

if TYPE_CHECKING:
    from typing import Optional, Dict

    from carconnectivity.objects import GenericObject


class SeatCupraCharging(Charging):  # pylint: disable=too-many-instance-attributes
    """
    SeatCupraCharging class for handling SeatCupra vehicle charging information.

    This class extends the Charging class and includes an enumeration of various
    charging states specific to SeatCupra vehicles.
    """
    def __init__(self, vehicle: ElectricVehicle | None = None, origin: Optional[Charging] = None) -> None:
        origin_mode_value = None
        origin_preferred_mode_value = None
        if origin is not None:
            super().__init__(vehicle=vehicle, origin=origin)
            self.settings = SeatCupraCharging.Settings(parent=self, origin=origin.settings)
            if hasattr(origin, 'mode'):
                origin_mode_attribute = getattr(origin, 'mode')
                origin_mode_value = getattr(origin_mode_attribute, 'value', None)
            if hasattr(origin, 'preferred_mode'):
                origin_preferred_mode_attribute = getattr(origin, 'preferred_mode')
                origin_preferred_mode_value = getattr(origin_preferred_mode_attribute, 'value', None)
        else:
            super().__init__(vehicle=vehicle)
            self.settings = SeatCupraCharging.Settings(parent=self, origin=self.settings)

        self.mode: EnumAttribute = EnumAttribute(name="mode", parent=self, value_type=SeatCupraCharging.SeatCupraChargeMode,
                                                 tags={'connector_custom'})
        if origin_mode_value is not None:
            self.mode._set_value(origin_mode_value)  # pylint: disable=protected-access

        self.preferred_mode: EnumAttribute = EnumAttribute(name="preferred_mode", parent=self, value_type=SeatCupraCharging.SeatCupraChargeMode,
                                                           tags={'connector_custom'})
        if origin_preferred_mode_value is not None:
            self.preferred_mode._set_value(origin_preferred_mode_value)  # pylint: disable=protected-access

    class Settings(Charging.Settings):
        """
        This class represents the settings for Cupra car charging.
        """
        def __init__(self, parent: Optional[GenericObject] = None, origin: Optional[Charging.Settings] = None) -> None:
            if origin is not None:
                super().__init__(parent=parent, origin=origin)
            else:
                super().__init__(parent=parent)
            self.max_current_in_ampere: Optional[bool] = None
            self.battery_care_enabled: BooleanAttribute = BooleanAttribute(name="battery_care_enabled", parent=self, tags={'connector_custom'})
            self.battery_care_target_level: LevelAttribute = LevelAttribute(name="battery_care_target_level", parent=self, tags={'connector_custom'})
            self.battery_care_target_level.minimum = 0.0
            self.battery_care_target_level.maximum = 100.0
            self.battery_care_target_level.precision = 5.0

    class SeatCupraChargingState(Enum,):
        """
        Enum representing the various charging states for a SeatCupra vehicle.
        """
        OFF = 'off'
        READY_FOR_CHARGING = 'readyForCharging'
        NOT_READY_FOR_CHARGING = 'notReadyForCharging'
        CONSERVATION = 'conservation'
        CHARGE_PURPOSE_REACHED_NOT_CONSERVATION_CHARGING = 'chargePurposeReachedAndNotConservationCharging'
        CHARGE_PURPOSE_REACHED_CONSERVATION = 'chargePurposeReachedAndConservation'
        CHARGING = 'charging'
        ERROR = 'error'
        UNSUPPORTED = 'unsupported'
        DISCHARGING = 'discharging'
        UNKNOWN = 'unknown charging state'

    class SeatCupraChargeMode(Enum,):
        """
        Enum class representing different SeatCupra charge modes.
        """
        MANUAL = 'manual'
        INVALID = 'invalid'
        OFF = 'off'
        TIMER = 'timer'
        ONLY_OWN_CURRENT = 'onlyOwnCurrent'
        PREFERRED_CHARGING_TIMES = 'preferredChargingTimes'
        TIMER_CHARGING_WITH_CLIMATISATION = 'timerChargingWithClimatisation'
        HOME_STORAGE_CHARGING = 'homeStorageCharging'
        IMMEDIATE_DISCHARGING = 'immediateDischarging'
        UNKNOWN = 'unknown charge mode'


# Mapping of Cupra charging states to generic charging states
mapping_seatcupra_charging_state: Dict[SeatCupraCharging.SeatCupraChargingState, Charging.ChargingState] = {
    SeatCupraCharging.SeatCupraChargingState.OFF: Charging.ChargingState.OFF,
    SeatCupraCharging.SeatCupraChargingState.NOT_READY_FOR_CHARGING: Charging.ChargingState.OFF,
    SeatCupraCharging.SeatCupraChargingState.READY_FOR_CHARGING: Charging.ChargingState.READY_FOR_CHARGING,
    SeatCupraCharging.SeatCupraChargingState.CONSERVATION: Charging.ChargingState.CONSERVATION,
    SeatCupraCharging.SeatCupraChargingState.CHARGE_PURPOSE_REACHED_NOT_CONSERVATION_CHARGING: Charging.ChargingState.READY_FOR_CHARGING,
    SeatCupraCharging.SeatCupraChargingState.CHARGE_PURPOSE_REACHED_CONSERVATION: Charging.ChargingState.CONSERVATION,
    SeatCupraCharging.SeatCupraChargingState.CHARGING: Charging.ChargingState.CHARGING,
    SeatCupraCharging.SeatCupraChargingState.ERROR: Charging.ChargingState.ERROR,
    SeatCupraCharging.SeatCupraChargingState.UNSUPPORTED: Charging.ChargingState.UNSUPPORTED,
    SeatCupraCharging.SeatCupraChargingState.DISCHARGING: Charging.ChargingState.DISCHARGING,
    SeatCupraCharging.SeatCupraChargingState.UNKNOWN: Charging.ChargingState.UNKNOWN
}
