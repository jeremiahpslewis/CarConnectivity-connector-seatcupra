"""Module for vehicle classes."""
from __future__ import annotations
from typing import TYPE_CHECKING

from carconnectivity.vehicle import GenericVehicle, ElectricVehicle, CombustionVehicle, HybridVehicle
from carconnectivity.attributes import BooleanAttribute
from carconnectivity.commands import Commands
from carconnectivity.command_impl import ClimatizationStartStopCommand, ChargingStartStopCommand

from carconnectivity_connectors.seatcupra.capability import Capabilities
from carconnectivity_connectors.seatcupra.climatization import SeatCupraClimatization
from carconnectivity_connectors.seatcupra.charging import SeatCupraCharging

SUPPORT_IMAGES = False
try:
    from PIL import Image
    SUPPORT_IMAGES = True
except ImportError:
    pass

if TYPE_CHECKING:
    from typing import Optional, Dict
    from carconnectivity.garage import Garage
    from carconnectivity.charging import Charging

    from carconnectivity_connectors.base.connector import BaseConnector


class SeatCupraVehicle(GenericVehicle):  # pylint: disable=too-many-instance-attributes
    """
    A class to represent a generic Seat/Cupra vehicle.

    Attributes:
    -----------
    vin : StringAttribute
        The vehicle identification number (VIN) of the vehicle.
    license_plate : StringAttribute
        The license plate of the vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SeatCupraVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
            self.capabilities: Capabilities = origin.capabilities
            self.capabilities.parent = self
            self.is_active: BooleanAttribute = origin.is_active
            self.is_active.parent = self
            if SUPPORT_IMAGES:
                self._car_images = origin._car_images
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)
            self.climatization = SeatCupraClimatization(vehicle=self, origin=self.climatization)
            self.capabilities: Capabilities = Capabilities(vehicle=self)
            self.is_active: BooleanAttribute = BooleanAttribute(name='is_active', parent=self, tags={'connector_custom'})
            if SUPPORT_IMAGES:
                self._car_images: Dict[str, Image.Image] = {}
        self._ensure_base_commands()

    def _ensure_base_commands(self) -> None:
        """
        Ensure climatization commands container exists with a start/stop command so downstream
        integrations can rely on it even before the connector adds hooks.
        """
        if self.climatization is not None:
            if getattr(self.climatization, 'commands', None) is None:
                self.climatization.commands = Commands(parent=self.climatization)
            commands = self.climatization.commands
            if commands is not None:
                if not commands.contains_command('start-stop'):
                    command = ClimatizationStartStopCommand(parent=commands)
                    command.enabled = True
                    commands.add_command(command)
                else:
                    command = commands.commands.get('start-stop')
                    if command is not None and not command.enabled:
                        command.enabled = True
                if not commands.enabled:
                    commands.enabled = True


class SeatCupraElectricVehicle(ElectricVehicle, SeatCupraVehicle):
    """
    Represents a Seat/Cupra electric vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SeatCupraVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
            if isinstance(origin, ElectricVehicle):
                self.charging: Charging = SeatCupraCharging(vehicle=self, origin=origin.charging)
            else:
                self.charging: Charging = SeatCupraCharging(vehicle=self, origin=self.charging)
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)
            self.charging: Charging = SeatCupraCharging(vehicle=self, origin=self.charging)
        self._ensure_charging_commands()

    def _ensure_charging_commands(self) -> None:
        if getattr(self, 'charging', None) is not None:
            if getattr(self.charging, 'commands', None) is None:
                self.charging.commands = Commands(parent=self.charging)
            if self.charging.commands is not None and not self.charging.commands.contains_command('start-stop'):
                command = ChargingStartStopCommand(parent=self.charging.commands)
                command.enabled = True
                self.charging.commands.add_command(command)


class SeatCupraCombustionVehicle(CombustionVehicle, SeatCupraVehicle):
    """
    Represents a Seat/Cupra combustion vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SeatCupraVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)


class SeatCupraHybridVehicle(HybridVehicle, SeatCupraVehicle):
    """
    Represents a Seat/Cupra hybrid vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SeatCupraVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)
