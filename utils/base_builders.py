# Helpers to build GEMD BaseNodes

### Imports ###

from utils.spec_builders import *
from utils.provenance import Provenance

from tools.entity.base import Process,Material,Ingredient,Measurement
from tools.entity.base.attributes import AttrsDict
from tools.entity.base.attributes import finalize_template,define_attribute
from tools.workflow.Workflow import Workflow

from typing import ClassVar

from gemd import ProcessTemplate,MaterialTemplate,MeasurementTemplate,PropertyTemplate,ParameterTemplate,ConditionTemplate
from gemd import ProcessSpec,MaterialSpec,MeasurementSpec,IngredientSpec
from gemd import ProcessRun,MaterialRun,MeasurementRun,IngredientRun
from gemd import PerformedSource, CategoricalBounds

from utils.templates.attribute_templates import ATTR_TEMPL

### Process BaseNodes ###

def build_grinding_process_base(name:str,location:str,equipment:str,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for grinding a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    process_spec = build_grinding_material_proc_spec(
        name=name,
        location=location,
        equipment=equipment,
        notes=notes
    )

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    class GrindingProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Equipment Used', bounds=ATTR_TEMPL['Equipment Used'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ConditionTemplate(
                name='Location', bounds=ATTR_TEMPL['Location'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    process = GrindingProcess.from_spec_or_run(
                name=f'{name} Grinding Process',
                run=process_run,
                spec=process_spec
            )

    return process

def build_heating_process_base(name:str,steps:int,location:str,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for heating a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    process_spec = build_heating_material_proc_spec(
        name=name,
        steps=steps,
        location=location,
        notes=notes
    )

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    class HeatingProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='StepsNum', bounds=ATTR_TEMPL['StepsNum'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Step', bounds=ATTR_TEMPL['Step'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ConditionTemplate(
                name='Location', bounds=ATTR_TEMPL['Location'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    process = HeatingProcess.from_spec_or_run(
                name=f'{name} Heating Process',
                run=process_run,
                spec=process_spec
            )

    return process

def build_dissolving_process_base(name:str,location:str,equipment:str,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for dissolving a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    process_spec = build_dissolving_material_proc_spec(
        name=name,
        location=location,
        equipment=equipment,
        notes=notes
    )

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    class DissolvingProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Equipment Used', bounds=ATTR_TEMPL['Equipment Used'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ConditionTemplate(
                name='Location', bounds=ATTR_TEMPL['Location'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    process = DissolvingProcess.from_spec_or_run(
                name=f'{name} Dissolving Process',
                run=process_run,
                spec=process_spec
            )

    return process

def build_pressing_process_base(name:str,location:str,equipment:str,pressure:float,duration:float,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for pressing a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    process_spec = build_pressing_material_proc_spec(
        name=name,
        location=location,
        pressure=pressure,
        duration=duration,
        equipment=equipment,
        notes=notes
    )

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    class PressingProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Equipment Used', bounds=ATTR_TEMPL['Equipment Used'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Duration', bounds=ATTR_TEMPL['Duration'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Pressure', bounds=ATTR_TEMPL['Pressure'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ConditionTemplate(
                name='Location', bounds=ATTR_TEMPL['Location'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    process = PressingProcess.from_spec_or_run(
                name=f'{name} Pressing Process',
                run=process_run,
                spec=process_spec
            )

    return process

def build_filtering_process_base(name:str,location:str,equipment:str,solvent:str,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for dissolving a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    process_spec = build_filtering_material_proc_spec(
        name=name,
        location=location,
        equipment=equipment,
        solvent=solvent,
        notes=notes
    )

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    class FilteringProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Equipment Used', bounds=ATTR_TEMPL['Equipment Used'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Solvent', bounds=ATTR_TEMPL['Solvent'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ConditionTemplate(
                name='Location', bounds=ATTR_TEMPL['Location'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    process = FilteringProcess.from_spec_or_run(
                name=f'{name} Filtering Process',
                run=process_run,
                spec=process_spec
            )

    return process

### Material BaseNodes ###

def build_ground_material_base(name:str,process_spec:ProcessSpec,process_run:ProcessRun,form:str='Powder',notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for a ground material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    material_spec = build_ground_material_mat_spec( 
        name=name,
        form=form,
        process_spec=process_spec,
        notes=notes,
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    class GroundMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name='Form', bounds=ATTR_TEMPL['Form'].bounds
            )
        )

        finalize_template(_ATTRS, TEMPLATE)

    material = GroundMaterial.from_spec_or_run(
                name=f'{name} Ground Material',
                run=material_run,
                spec=material_spec
            )
    
    return material

def build_heated_material_base(name:str,process_spec:ProcessSpec,process_run:ProcessRun,form:str,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for a ground material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    material_spec = build_heated_material_mat_spec( 
        name=name,
        form=form,
        process=process_spec,
        notes=notes
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    class HeatedMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name='Form', bounds=ATTR_TEMPL['Form'].bounds
            )
        )

        finalize_template(_ATTRS, TEMPLATE)

    material = HeatedMaterial.from_spec_or_run(
                name=f'{name} Heated Material',
                run=material_run,
                spec=material_spec
            )
    
    return material

def build_dissolved_material_base(name:str,process_spec:ProcessSpec,process_run:ProcessRun,form:str='Solution',notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for a solution material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    material_spec = build_dissolved_material_mat_spec( 
        name=name,
        form=form,
        process=process_spec,
        notes=notes
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    class DissolvedMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name='Form', bounds=ATTR_TEMPL['Form'].bounds
            )
        )

        finalize_template(_ATTRS, TEMPLATE)

    material = DissolvedMaterial.from_spec_or_run(
                name=f'{name} Dissolved Material',
                run=material_run,
                spec=material_spec
            )
    
    return material

def build_filtered_material_base(name:str,process_spec:ProcessSpec,process_run:ProcessRun,form:str,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for a solution material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    material_spec = build_filtered_material_mat_spec( 
        name=name,
        form=form,
        process=process_spec,
        notes=notes
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    class FilteredMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name='Form', bounds=ATTR_TEMPL['Form'].bounds
            )
        )

        finalize_template(_ATTRS, TEMPLATE)

    material = FilteredMaterial.from_spec_or_run(
                name=f'{name} Filtered Material',
                run=material_run,
                spec=material_spec
            )
    
    return material

def build_pressed_material_base(name:str,process_spec:ProcessSpec,process_run:ProcessRun,form:str='Pellet',notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a basenode for a pressed material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    material_spec = build_pressed_material_mat_spec( 
        name=name,
        form=form,
        process=process_spec,
        notes=notes
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    class PressedMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name='Form', bounds=ATTR_TEMPL['Form'].bounds
            )
        )

        finalize_template(_ATTRS, TEMPLATE)

    material = PressedMaterial.from_spec_or_run(
                name=f'{name} Pressed Material',
                run=material_run,
                spec=material_spec
            )
    
    return material

### Ingredient BaseNode ###

def build_ingredient_base(name:str,material_spec:MaterialSpec,material_run:MaterialRun,quantity_spec,quantity_run,process_spec:ProcessSpec,process_run:ProcessRun,notes:str=None):

    '''
    Returns an ingredient BaseNode.
    '''

    spec = build_ingredient_spec(
        name=name,
        process=process_spec,
        material=material_spec,
        quantity=quantity_spec,
        notes=notes
    )

    run = IngredientRun(
        material = material_run,
        process=process_run,
        absolute_quantity=quantity_run,
        spec=spec,
        notes=notes
    )

    ingredient = Ingredient.from_spec_or_run(
        name=f'{name} Ingredient',
        spec=spec,
        run=run,
        notes=notes
    )

    return ingredient

### Measurement BaseNodes ###

def build_xrd_measurement_base(name:str,duration:float,range:str,adhesive:str,material:MaterialRun,location:str='X-Ray Diffraction Panel',file=None,notes:str=None,prv:Provenance=None):

    '''
    Returns an XRD measurement BaseNode.
    '''

    measurement_spec = build_xrd_meas_spec(
        name=name,
        duration=duration,
        range=range,
        adhesive=adhesive,
        location=location,
        file=None
    )

    measurement_run = MeasurementRun(
        name=name,
        spec=measurement_spec,
        material=material,
        parameters=measurement_spec.parameters,
        conditions=measurement_spec.conditions,
        notes=notes,
        file_links=file,
        source=PerformedSource(prv.email,prv.date)
    )

    class XRDMeasurement(Measurement):

        TEMPLATE: ClassVar[MeasurementTemplate] = MeasurementTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Duration', bounds=ATTR_TEMPL['Duration'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='XRD Range', bounds=ATTR_TEMPL['XRD Range'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='XRD Adhesive', bounds=ATTR_TEMPL['XRD Adhesive'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ConditionTemplate(
                name='Location', bounds=ATTR_TEMPL['Location'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    measurement = XRDMeasurement.from_spec_or_run(
                name=f'{name} XRD Measurement',
                run=measurement_run,
                spec=measurement_spec
            )

    return measurement