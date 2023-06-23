'''Base class for processes and measurement.'''

from typing import ClassVar, Type, Union, Optional
import re
from datetime import datetime

from gemd import (
    ProcessTemplate, ProcessSpec, ProcessRun,
    MeasurementTemplate, MeasurementSpec, MeasurementRun,
    Condition, Parameter, PerformedSource
)

from .base_node import BaseNode
from .typing import SpecRunLiteral, ValueOriginDict

__all__ = ['ProcessOrMeasurement']

class ProcessOrMeasurement(BaseNode):
    '''Base class for processes and measurements.'''

    _TempType: ClassVar[Type[Union[ProcessTemplate, MeasurementTemplate]]]
    _SpecType: ClassVar[Type[Union[ProcessSpec, MeasurementSpec]]]
    _RunType: ClassVar[Type[Union[ProcessRun, MeasurementRun]]]

    TEMPLATE: ClassVar[Union[ProcessTemplate, MeasurementTemplate]]

    # {'brand1': {'model1': ('id1', 'id2', etc.), etc.}, etc.}
    # e.g. {'Quantum Design': {'DynaCool': ['1', '2', '3']}}
    INSTRUMENTS: ClassVar[dict[str, dict[str, tuple]]]

    def __init__(
        self,
        name: str,
        *,
        notes: Optional[str] = None,
        conditions: Optional[list[Condition]] = None,
        parameters: Optional[list[Parameter]] = None,
        ) -> None:

        super().__init__(name, notes=notes)

        if conditions is None:
            conditions = []

        if parameters is None:
            parameters = []

        self.update_conditions(*conditions, replace_all=True, which='spec')

        self.update_parameters(*parameters, replace_all=True, which='spec')

    def get_conditions_dict(self) -> dict[str, ValueOriginDict]:
        '''Return a ``dict`` of the spec and run conditions.'''
        return self._spec_run_dict(self._spec.conditions, self._run.conditions)

    def update_conditions(
        self,
        *conditions: Condition,
        replace_all: bool = False,
        which: SpecRunLiteral = 'spec'
        ) -> None:
        '''
        Change or add conditions.

        Parameters
        ----------
        *conditions: Condition
            The conditions to change (by name) or add.
        replace_all: bool, default False
            If ``True``, remove any existing conditions before adding new ones.
        which: {'spec', 'run', 'both'}, default 'spec'
            Whether to update the spec, run, or both.

        Raises
        ------
        ValueError
            If the name of a condition is not supported.
        '''

        self._update_attributes(
            AttrType=Condition,
            attributes=conditions,
            replace_all=replace_all,
            which=which
        )

    def remove_conditions(self, *condition_names: str, which: SpecRunLiteral = 'spec') -> None:
        '''
        Remove conditions by name.

        *condition_names: str
            The names of conditions to remove.
        which: {'spec', 'run', 'both'}, default 'spec'
            Whether to remove from the spec, run, or both.

        Raises
        ------
        ValueError
            If the name of a condition is not supported.
        '''

        self._remove_attributes(AttrType=Condition, attr_names=condition_names, which=which)

    def get_parameters_dict(self) -> dict[str, ValueOriginDict]:
        '''Return a ``dict`` of the spec and run parameters.'''
        return self._spec_run_dict(self._spec.parameters, self._run.parameters)

    def update_parameters(
        self,
        *parameters: Parameter,
        replace_all: bool = False,
        which: SpecRunLiteral = 'spec'
        ) -> None:
        '''
        Change or add parameters.

        Parameters
        ----------
        *parameters: Parameter
            The parameters to change (by name) or add.
        replace_all: bool, default False
            If ``True``, remove any existing parameters before adding new ones.
        which: {'spec', 'run', 'both'}, default 'spec'
            Whether to update the spec, run, or both.

        Raises
        ------
        ValueError
            If the name of a parameter is not supported.
        '''

        self._update_attributes(
            AttrType=Parameter,
            attributes=parameters,
            replace_all=replace_all,
            which=which
        )

    def remove_parameters(self, *parameter_names: str, which: SpecRunLiteral = 'spec') -> None:
        '''
        Remove parameters by name.

        *parameter_names: str
            The names of parameters to remove.
        which: {'spec', 'run', 'both'}, default 'spec'
            Whether to remove from the spec, run, or both.

        Raises
        ------
        ValueError
            If the name of a parameter is not supported.
        '''

        self._remove_attributes(AttrType=Parameter, attr_names=parameter_names, which=which)

    def get_source(self) -> dict[str, str]:
        '''
        Get the run's source.

        Returns
        -------
        source: dict
            ``{'performed_by': '<email>', 'performed_date': '<iso_date>'}``
        '''

        run_source = self._run.source.as_dict()

        return {
            'performed_by': run_source['performed_by'],
            'performed_date': run_source['performed_date']
        }

    def set_source(self, email: str, iso_date: Optional[str] = None) -> None:
        '''
        Set the run's source with a valid email address and an optional ISO date string.

        Parameters
        ----------
        email: str
            A valid email address.
        date: str, optional
            A date string to be passed to ``datetime.fromisoformat``.

        Raises
        ------
        ValueError
            If `email` is invalid.
        '''

        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError(
                'Invalid email. Must contain a single "@" and at least one "." after the "@".'
            )

        if iso_date is not None:
            iso_date = datetime.fromisoformat(iso_date).isoformat(timespec='auto')

        self._run.source = PerformedSource(email, iso_date)

    @staticmethod
    def _spec_run_dict(
        spec_attrs: Union[list[Condition], list[Parameter]],
        run_attrs: Union[list[Condition], list[Parameter]]
        ) -> dict[str, ValueOriginDict]:
        '''
        Return a ``dict`` of spec and run conditions or parameters.

        The keys are the names of the spec and run attributes.
        Each value is a ``dict`` with the keys ``'spec'`` and ``'run'``.
        Each ``'spec'`` and ``'run'`` key corresponds to another ``dict`` containing
        a value ``dict`` and origin ``str``, or ``None`` if the attribute is only
        found under one of spec or run.

        Example output:

        {
            'Duration': {
                'spec': {
                    'value': {
                        'nominal': 60,
                        'units': 'minutes',
                        'type': 'nominal_real'
                    },
                    'origin': 'specified'
                },
                'run': {
                    'value': None,
                    'origin': None
                }
            },
            'Set temperature': {
                'spec': {
                    'value': {
                        'nominal': 105,
                        'units': 'K',
                        'type': 'nominal_real'
                    },
                    'origin': 'specified'
                },
                'run': {
                    'value': {
                        'lower_bound': 104,
                        'upper_bound': 106,
                        'units': 'K',
                        'type': 'uniform_real'
                    },
                    'origin': 'measured'
                }
            },
            'Set pressure': {
                'spec': {
                    'value': {
                        'nominal': 400,
                        'units': 'millitorr',
                        'type': 'nominal_real'
                    },
                    'origin': 'specified'
                },
                'run': {
                    'value': {
                        'mean': 399.9,
                        'std': 0.5,
                        'units': 'K',
                        'type': 'normal_real'
                    },
                    'origin': 'measured'
                }
            }
        }
        '''

        spec_dict = {
            attr.name: {'value': attr.value.as_dict(), 'origin': attr.origin}
            for attr in spec_attrs
        }
        run_dict = {
            attr.name: {'value': attr.value.as_dict(), 'origin': attr.origin}
            for attr in run_attrs
        }

        attrs = {}

        for name, value_and_origin in spec_dict.items():
            attrs[name] = {'spec': value_and_origin, 'run': None}

        for name, value_and_origin in run_dict.items():
            if name in attrs:
                attrs[name]['run'] = value_and_origin
            else:
                attrs[name] = {'spec': None, 'run': value_and_origin}

        return attrs

    def to_form(self) -> str:
        pass
