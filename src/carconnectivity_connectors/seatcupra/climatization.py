"""
Module for charging for Seat/Cupra vehicles.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from carconnectivity.climatization import Climatization
from carconnectivity.objects import GenericObject
from carconnectivity.vehicle import GenericVehicle
from carconnectivity.attributes import BooleanAttribute, StringAttribute

if TYPE_CHECKING:
    from typing import Optional


class SeatCupraClimatization(Climatization):  # pylint: disable=too-many-instance-attributes
    """
    SeatCupraClimatization class for handling Seat/Cupra vehicle climatization information.

    This class extends the Climatization class and includes an enumeration of various
    climatization states specific to Volkswagen vehicles.
    """
    def __init__(self, vehicle: GenericVehicle | None = None, origin: Optional[Climatization] = None) -> None:
        if origin is not None:
            super().__init__(vehicle=vehicle, origin=origin)
            if not isinstance(self.settings, SeatCupraClimatization.Settings):
                self.settings: Climatization.Settings = SeatCupraClimatization.Settings(parent=self, origin=origin.settings)
        else:
            super().__init__(vehicle=vehicle)
            self.settings: Climatization.Settings = SeatCupraClimatization.Settings(parent=self, origin=self.settings)
        # Ensure explicit default UNKNOWN state to avoid empty payloads downstream
        try:
            if getattr(self, 'state', None) is not None and getattr(self.state, 'value', None) is None:
                self.state._set_value(Climatization.ClimatizationState.UNKNOWN)  # pylint: disable=protected-access
        except Exception:
            pass

    class Settings(Climatization.Settings):
        """
        This class represents the settings for a skoda car climatiation.
        """
        def __init__(self, parent: Optional[GenericObject] = None, origin: Optional[Climatization.Settings] = None) -> None:
            if origin is not None:
                super().__init__(parent=parent, origin=origin)
            else:
                super().__init__(parent=parent)
            self.climatization_at_unlock: BooleanAttribute = BooleanAttribute(name="climatization_at_unlock", parent=self, tags={'connector_custom'})
            self.window_heating_enabled: BooleanAttribute = BooleanAttribute(name="window_heating_enabled", parent=self, tags={'connector_custom'})
            self.unit_in_car: StringAttribute = StringAttribute(name="unit_in_car", parent=self, tags={'connector_custom'})

            if origin is not None:
                if hasattr(origin, 'climatization_at_unlock') and getattr(origin.climatization_at_unlock, 'value', None) is not None:
                    self.climatization_at_unlock._set_value(origin.climatization_at_unlock.value)  # pylint: disable=protected-access
                if hasattr(origin, 'window_heating_enabled') and getattr(origin.window_heating_enabled, 'value', None) is not None:
                    self.window_heating_enabled._set_value(origin.window_heating_enabled.value)  # pylint: disable=protected-access
                if hasattr(origin, 'unit_in_car') and getattr(origin.unit_in_car, 'value', None) is not None:
                    self.unit_in_car._set_value(origin.unit_in_car.value)  # pylint: disable=protected-access
