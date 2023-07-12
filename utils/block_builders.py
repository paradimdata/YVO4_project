# Tools to build GEMD BaseNodes

### Imports ###

from utils.spec_builders import *
from utils.provenance import Provenance

from tools.entity.base import Process,Material,Ingredient,Measurement
from tools.entity.base.attributes import AttrsDict
from tools.entity.base.attributes import finalize_template,define_attribute
from tools.block.Block import Block
from tools.workflow.Workflow import Workflow

from typing import ClassVar

from gemd import ProcessTemplate,MaterialTemplate,MeasurementTemplate,PropertyTemplate,ParameterTemplate,ConditionTemplate
from gemd import ProcessSpec,MaterialSpec,MeasurementSpec,IngredientSpec
from gemd import ProcessRun,MaterialRun,MeasurementRun,IngredientRun
from gemd import CategoricalBounds,RealBounds,IntegerBounds
from gemd import PerformedSource
from gemd.entity.util import make_instance

from utils.templates.attribute_templates import ATTR_TEMPL

def make_ingredient_dict(name,quantity,measured,unc,units):
    return {
        'name':name,
        'quantity':NominalReal(quantity,units),
        'measured':UniformReal(measured-unc,measured+unc,units)
    }

def build_acquiring_material_block(name:str,manufacturer:str,lot_id:str,cas_rn:str,form:str,purity:float,notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a Block for acquiring a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Manufacturer: The manufacturer from which the material was purchased
        ex: 'Thermo Scientific'
    Lot ID: Lot ID of the purchased material
        ex: '2134WX'
    CAS RN: CAS registry number of the purchased material
        ex: '123-45-678'
    Form: Physical form of the ingredient
        ex: 'Powder', 'Rod'
    Purity: Purity of the material as a percent
        ex: 99.996
    Workflow: Workflow to which the Block belongs 
        ex: Workflow()
    Provenance: Provenance object describing the personnel involved
        ex: Provenance()
    """

    process_spec = build_acquire_raw_material_proc_spec( 
        name=name,
        manufacturer=manufacturer,
        lot_id=lot_id,
        cas_rn=cas_rn,
        notes=notes
    )

    material_spec = build_raw_material_mat_spec( 
        name=name,
        form=form,
        purity=purity,
    )

    ### Convert Ingredient, Process, Material, & Measurement Specs into Runs ###

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    ### Build Base Nodes ###

    class AcquisitionProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Manufacturer', bounds=ATTR_TEMPL['Manufacturer'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='Lot ID', bounds=ATTR_TEMPL['Lot ID'].bounds
            )      
        )

        define_attribute(
            _ATTRS,
            template=ParameterTemplate(
                name='CAS RN', bounds=ATTR_TEMPL['CAS RN'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    process = AcquisitionProcess.from_spec_or_run(
                name=f'{name} Acquisition Process',
                run=process_run,
                spec=process_spec
            )

    class AcquiredMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name='Form', bounds=ATTR_TEMPL['Form'].bounds
            )
        )

        define_attribute(
            _ATTRS,
            template=PropertyTemplate(
                name="Purity", bounds=ATTR_TEMPL['Purity Percentage'].bounds
            ),
        )

        finalize_template(_ATTRS, TEMPLATE)

    material = AcquiredMaterial.from_spec_or_run(
                name=f'{name} Acquired Material Base',
                run=material_run,
                spec=material_spec
            )
    
    ### Build Block ###

    block = Block(
        name=f'{name} Acquisition Block',
        workflow=workflow,
        process=process,
        material=material
    )

    block.link_within()

    return block

def build_grinding_material_block(name:str,location:str,form:str='Powder',equipment:str='Mortar and Pestle',ingredient_dict:dict={},notes:str=None,workflow:Workflow=None,prv:Provenance=None):
    """
    Builds a Block for grinding a material.

    ### Parameters:

    Name: Name of the material being acquired
        ex: 'YVO4'
    Location: Location where a process was performed
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'
    Equipment: Equipment used to perform an action. Default is mortar and pestle.
        ex: 'Mortar and Pestle'
    Ingredient Dicts: A list of dictionaries with ingredient names and quantities
        ex: INGREDIENTS = [
        {
        'name':'Y2O3',
        'quantity':NominalReal(123.3,'mg'),
        'measured':NominalReal(123.1,'mg')
        }
        ]
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

    material_spec = build_ground_material_mat_spec( 
        name=name,
        form=form,
        notes=notes
    )

    ingredient_spec = []

    for i in ingredient_dict:
        ingredient_spec.append(
            IngredientSpec(
            name=i['name'],
            process=process_spec,
            absolute_quantity=i['quantity'],
            notes=notes
            )
        )


    ### Convert Ingredient, Process, Material, & Measurement Specs into Runs ###

    process_run = ProcessRun( 
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.email,prv.date),
        notes=notes
    )

    material_run = MaterialRun( 
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental',
        notes=notes
    )

    ingredient_run = []

    for i in range(len(ingredient_spec)):
        ingredient_run.append(
            IngredientRun(
            process=process_run,
            spec=ingredient_spec[i],
            absolute_quantity=ingredient_dict[i]['measured']
            )
        )

    ### Build Base Nodes ###

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
    
    ingredients = []

    for i in range(len(ingredient_run)):

        ingredients.append(
            Ingredient.from_spec_or_run(
            name=ingredient_spec[i].name,
            spec=ingredient_spec[i],
            run=ingredient_run[i]
            )
        )       

    
    ### Build Block ###

    block = Block(
        name=f'{name} Grinding',
        workflow=workflow,
        process=process,
        material=material,
        ingredients=ingredients
    )

    return block