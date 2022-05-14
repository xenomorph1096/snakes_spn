"""

Author: Lulof Pirée
May 2022

--------------------------------------------------------------------------------
Copyright (C) 2022 Lulof Pirée

This file is part of the snakes_spn program.

This program is free software: 
you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. 
If not, see <https://www.gnu.org/licenses/>. 

--------------------------------------------------------------------------------
File content:
Python script providing the SPN features to the SNAKES plugin interface.
"""
from __future__ import annotations
from typing import *

from snakes import ConstraintError
import snakes.plugins
from snakes.nets import Transition, Place, PetriNet, Expression, Substitution


class TransitionStatus:

    def __init__(self, is_running: bool = False, remaining_delay: float | None = None):
        self.is_running: bool = is_running
        self.remaining_delay: float | None = remaining_delay

    @property
    def is_running(self) -> bool:
        return self.is_running

    @is_running.setter
    def is_running(self, new_value: bool):
        self.is_running = new_value
        if not self.is_running:
            self.remaining_delay = None

    @property
    def remaining_delay(self) -> float | None:
        if not self.is_running:
            raise RuntimeError("TransitionStatus has no remaining delay "
                               "while not running.")
        return self.is_running

    @remaining_delay.setter
    def remaining_delay(self, new_delay: float | None):
        if isinstance(new_delay, float) and not self.is_running:
            raise RuntimeError("Cannot set delay when not running.")
        if isinstance(new_delay, None) and self.is_running:
            raise RuntimeError("While running, the delay must be a number.")
        self.remaining_delay = new_delay


@snakes.plugins.plugin("snakes.nets")
def extend(module) -> Tuple[Type[Transition], Type[Place], Type[PetriNet]]:

    return Transition, Place, PetriNet


def gen_transition_class(module) -> Type[Transition]:
    """
    Given a configured version of `snakes.net` as `module`,
    create a new subclass of `module.Transition` with SPN features.

    @param module: Python module providing a subclassable class `Transition`.
    @type module: ?
    @return: subclass of `Transition` with SPN features.
    """
    print(type(module))

    class Transition(module.Transition):

        def __init__(self, **args) -> None:
            """

            @param args: plugin arguments
            @keyword stats: initial status of the Transition 
                (defaults to `TransitionStatus(False, None)`)
            @type status: Optional[TransitionStatus]
            @keyword rate_function: expression computing the rate
                of the exponentially-distributed delay.
            @type rate_function: Expression
            """
            self._rate = args.pop("rate_function")
            assert isinstance(self._rate, Expression)
            module.Transition.__init__(**args)

            raise NotImplementedError("TODO: add initial status")
            self._status = None

        def enabled(self, binding: Substitution, **args) -> bool:
            """
            """
            