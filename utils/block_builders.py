# Tools to build GEMD BaseNodes

### Imports ###

from utils.spec_builders import *

from tools.entity.base import Process,Material,Ingredient,Measurement
from tools.entity.base.attributes import AttrsDict
from tools.entity.base.attributes import finalize_template
from tools.block.Block import Block

from typing import ClassVar
from gemd import ProcessRun,MaterialRun,IngredientRun,MeasurementRun,PerformedSource,ProcessTemplate,MaterialTemplate,MeasurementTemplate
from tools.workflow.Workflow import Workflow

from utils.provenance import Provenance

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

    process_run = ProcessRun( # Returns a ProcessRun
        name=name,
        spec=process_spec,
        conditions=process_spec.conditions,
        parameters=process_spec.parameters,
        source= PerformedSource(prv.tag,prv.date)
    )

    material_run = MaterialRun( # Returns a MaterialRun
        name=name,
        spec=material_spec,
        process=process_run,
        sample_type='experimental'
    )

    ### Build Base Nodes ###

    class AcquisitionProcess(Process):

        TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{}}

        finalize_template(_ATTRS, TEMPLATE)

    process = AcquisitionProcess.from_spec_or_run(
                name=f'{name} Acquisition Process Base',
                run=process_run
            )

    class AcquiredMaterial(Material):

        TEMPLATE: ClassVar[MaterialTemplate] = MaterialTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'properties':{}}

        finalize_template(_ATTRS, TEMPLATE)

    material = AcquiredMaterial.from_spec_or_run(
                name=f'{name} Acquired Material Base',
                run=material_run
            )
    
    ### Build Block ###

    block = Block(
        name=f'{name} Acquisition Block',
        workflow=workflow,
        process=process,
        material=material
    )

    block.link_within

    return block