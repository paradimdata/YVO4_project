'''Base class for materials.'''

from typing import ClassVar, Optional

from gemd import MaterialTemplate, MaterialSpec, MaterialRun, PropertyAndConditions
from gemd.entity.util import make_instance
from gemd.enumeration import SampleType

from .base_node import BaseNode
from .typing import ProcessDict, PropsAndCondsDict
from .process import Process

__all__ = ['Material']

class Material(BaseNode):
    '''
    Base class for materials.

    TODO: instructions for subclassing
    '''

    _TempType = MaterialTemplate
    _SpecType = MaterialSpec
    _RunType = MaterialRun

    TEMPLATE: ClassVar[MaterialTemplate]

    def __init__(
        self,
        name: str,
        *,
        notes: Optional[str] = None,
        process: Optional[Process] = None,
        properties: Optional[list[PropertyAndConditions]] = None,
        sample_type: Optional[SampleType] = None
        ) -> None:

        super().__init__(name, notes=notes)

        self.set_process(process)

        if properties is None:
            properties = []

        self.update_properties_and_conditions(*properties, replace_all=True)

        self.set_sample_type(sample_type)

    @property
    def spec(self) -> MaterialSpec:
        '''The underlying material spec.'''
        return self._spec

    @property
    def run(self) -> MaterialRun:
        '''The underlying material run.'''
        return self._run

    @classmethod
    def from_spec_or_run(
        cls,
        name: str,
        *,
        notes: Optional[str] = None,
        spec: MaterialSpec = None,
        run: MaterialRun = None
        ) -> 'Material':
        '''
        Instantiate a `Material` from a spec or run with appropriate validation.

        Note that the spec's template will be set to the class template,
        and the run's spec will be set to this spec.
        '''

        if spec is None and run is None:
            raise ValueError('At least one of spec or run must be given.')

        material = cls(name, notes=notes)

        if spec is not None:

            if not isinstance(spec, MaterialSpec):
                raise TypeError('spec must be a MaterialSpec.')

            material._spec = spec

            material.spec.name = name
            material.spec.notes = notes
            material.spec.template = cls.TEMPLATE

            material.update_properties_and_conditions()

        if run is not None:

            if not isinstance(run, MaterialRun):
                raise TypeError('run must be a MaterialRun.')

            material._run = run
            material.run.name = name
            material.run.notes = notes

            material.run.spec = material.spec
        
        else:
            material.run = make_instance(material.spec)

        return material

    def get_process_dict(self) -> ProcessDict:
        '''Get the names of the spec's and run's process.'''

        return {'spec': self._spec.process.name, 'run': self._run.process.name}

    def set_process(self, process: Optional[Process]) -> None:
        '''
        Set the process that produces this material.

        Parameters
        ----------
        process: {Process, None}
            Process instance whose spec and run will be set as the process for the material's
            spec and run, respectively. If ``None``, the material's spec and run process will be
            ``None``.
        '''

        if process is not None:
            self._spec.process = process.spec
            self._run.process = process.run
        else:
            self._spec.process = None
            self._run.process = None

    def get_properties_and_conditions_dict(self) -> dict[str, PropsAndCondsDict]:
        '''
        Return a ``dict`` of material spec properties and conditions.

        The keys are the names of the properties.
        Each value is a ``dict`` with the keys ``'property'`` and ``'conditions'``.
        Each ``'property'`` key corresponds to another ``dict`` containing a value
        ``dict`` and origin ``str``.
        Each ``'condition'`` key corresponds to a ``dict`` in which the keys are
        the names of the conditions associated with a particular property and the
        values are value/origin ``dict``s.

        Example output:

        {
            'Composition': {
                'property': {
                    'value': {'formula': 'Na', 'type': 'empirical_formula'},
                    'origin': 'specified'
                },
                'conditions': {}
            },
            'Purity': {
                'property': {
                    'value': {'nominal': 0.999, 'units': '', 'type': 'nominal_real'},
                    'origin': 'specified'
                },
                'conditions': {
                    'atmosphere': {
                        'value': {'category': 'argon', 'type': 'nominal_categorical'},
                        'origin': 'specified'
                    },
                    'pressure': {
                        'value': {'nominal': 1, 'units': 'bar', 'type': 'nominal_real'},
                        'origin': 'specified'
                    }
                }
            },
        }
        '''

        return self._prop_cond_dict(self._spec.properties)

    def update_properties_and_conditions(
        self,
        *properties: PropertyAndConditions,
        replace_all: bool = False
        ) -> None:
        '''
        Change or add expected properties (with conditions) of the material spec.

        Parameters
        ----------
        *properties: PropertyAndConditions
            The properties (with conditions) to change (by name) or add.
        replace_all: bool, default False
            If ``True``, remove any existing properties before adding new ones.

        Raises
        ------
        ValueError
            If the name of a property is not supported.
        '''

        self._update_attributes(
            AttrType=PropertyAndConditions,
            attributes=properties,
            replace_all=replace_all,
            which='spec'
        )

    def remove_properties(self, *property_names: str) -> None:
        '''
        Remove expected properties from the material spec by name.

        *property_names: str
            The names of properties to remove.

        Raises
        ------
        ValueError
            If the name of a property is not supported.
        '''

        self._remove_attributes(
            AttrType=PropertyAndConditions,
            attr_names=property_names,
            which='spec'
        )

    def get_sample_type(self) -> SampleType:
        '''
        Get the sample type of the material run.

        Returns
        -------
        sample_type: SampleType
        '''

        return self._run.sample_type

    def set_sample_type(self, sample_type: Optional[SampleType]) -> None:
        '''
        Set the sample type of the material run.

        Parameters
        ----------
        sample_type: SampleType
        '''

        self._run.sample_type = sample_type

    @staticmethod
    def _prop_cond_dict(spec_prop_conds:list[PropertyAndConditions]) -> dict[str,PropsAndCondsDict]:
        '''Return a ``dict`` of material spec properties and conditions.'''

        prop_cond_dict = {
            prop_cond.property.name: {
                'property': {
                    'value': prop_cond.property.value.as_dict(),
                    'origin': prop_cond.property.origin
                },
                'conditions': {
                    cond.name: {
                        'value': cond.value.as_dict(),
                        'origin': cond.origin
                    }
                    for cond in prop_cond.conditions
                }
            }
            for prop_cond in spec_prop_conds
        }

        return prop_cond_dict

    def to_form(self) -> str:
        pass
