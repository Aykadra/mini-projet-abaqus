# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqusConstants import *
from noms import (
    ACIER_304,
    MODELE_POUTRE,
    PIECE_1,
    PIECE_2,
    PIECE_3,
    PROFIL_CIRCULAIRE_CREUX,
    SECTION_CIRCULAIRE_POUTRE,
)
import variables as v

## Création du modèle
mdb.Model(modelType=STANDARD_EXPLICIT, name=MODELE_POUTRE)


## Création  de l'esquisse
# Tube vertical
def creer_piece_1():
    mdb.models[MODELE_POUTRE].ConstrainedSketch(
        name="__profile__", sheetSize=v.HAUTEUR_TIGE_VERTICALE + 1
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].Line(
        point1=(0.0, -v.HAUTEUR_TIGE_VERTICALE / 2),
        point2=(0.0, v.HAUTEUR_TIGE_VERTICALE / 2),
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].VerticalConstraint(
        addUndoState=False,
        entity=mdb.models[MODELE_POUTRE].sketches["__profile__"].geometry[2],
    )
    mdb.models[MODELE_POUTRE].Part(
        dimensionality=THREE_D, name=PIECE_1, type=DEFORMABLE_BODY
    )
    mdb.models[MODELE_POUTRE].parts[PIECE_1].BaseWire(
        sketch=mdb.models[MODELE_POUTRE].sketches["__profile__"]
    )
    del mdb.models[MODELE_POUTRE].sketches["__profile__"]


creer_piece_1()


# tube horizontal
def creer_piece_2():
    mdb.models[MODELE_POUTRE].ConstrainedSketch(
        name="__profile__", sheetSize=v.LONGEUR_TIGE_HORIZONTALE
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].Line(
        point1=(-v.LONGEUR_TIGE_HORIZONTALE / 2, 0.0),
        point2=(v.LONGEUR_TIGE_HORIZONTALE / 2, 0.0),
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].HorizontalConstraint(
        addUndoState=False,
        entity=mdb.models[MODELE_POUTRE].sketches["__profile__"].geometry[2],
    )
    mdb.models[MODELE_POUTRE].Part(
        dimensionality=THREE_D, name=PIECE_2, type=DEFORMABLE_BODY
    )
    mdb.models[MODELE_POUTRE].parts[PIECE_2].BaseWire(
        sketch=mdb.models[MODELE_POUTRE].sketches["__profile__"]
    )
    del mdb.models[MODELE_POUTRE].sketches["__profile__"]


creer_piece_2()


# coude
def creer_piece_3():
    mdb.models[MODELE_POUTRE].ConstrainedSketch(name="__profile__", sheetSize=200.0)
    mdb.models[MODELE_POUTRE].sketches["__profile__"].ArcByCenterEnds(
        center=(0.0, 0.0),
        direction=CLOCKWISE,
        point1=(-v.RAYON_DE_COURBURE_COUDE, 0.0),
        point2=(0.0, v.RAYON_DE_COURBURE_COUDE),
    )
    mdb.models[MODELE_POUTRE].Part(
        dimensionality=THREE_D, name=PIECE_3, type=DEFORMABLE_BODY
    )
    mdb.models[MODELE_POUTRE].parts[PIECE_3].BaseWire(
        sketch=mdb.models[MODELE_POUTRE].sketches["__profile__"]
    )
    del mdb.models[MODELE_POUTRE].sketches["__profile__"]


creer_piece_3()


## Matériaux
def creer_materiau_elastique(
    name: str, density: float, young_modulus: float, poisson: float
):
    mdb.models[MODELE_POUTRE].Material(name=name)
    mdb.models[MODELE_POUTRE].materials[name].Density(table=((density,),))
    mdb.models[MODELE_POUTRE].materials[name].Elastic(table=((young_modulus, poisson),))


creer_materiau_elastique(
    name=ACIER_304,
    density=v.DENSITE_ACIER,
    young_modulus=v.MODULE_YOUNG_ACIER,
    poisson=v.POISSON_ACIER,
)

## Sections
mdb.models[MODELE_POUTRE].PipeProfile(
    name=PROFIL_CIRCULAIRE_CREUX, r=v.RAYON_TUYAU, t=v.EPAISSEUR_TUYAU
)
mdb.models[MODELE_POUTRE].BeamSection(
    beamSectionOffset=(0.0, 0.0),
    consistentMassMatrix=False,
    integration=DURING_ANALYSIS,
    material=ACIER_304,
    name=SECTION_CIRCULAIRE_POUTRE,
    poissonRatio=0.0,
    profile=PROFIL_CIRCULAIRE_CREUX,
    temperatureVar=LINEAR,
)
# Association coude
mdb.models[MODELE_POUTRE].parts[PIECE_3].SectionAssignment(
    offset=0.0,
    offsetField="",
    offsetType=MIDDLE_SURFACE,
    region=Region(
        edges=mdb.models[MODELE_POUTRE]
        .parts["Part-3"]
        .edges.getSequenceFromMask(
            mask=("[#1 ]",),
        )
    ),
    sectionName=SECTION_CIRCULAIRE_POUTRE,
    thicknessAssignment=FROM_SECTION,
)


# Ici

# Association tube vertical
mdb.models[MODELE_POUTRE].parts["Tube_vertical"].SectionAssignment(
    offset=0.0,
    offsetField="",
    offsetType=MIDDLE_SURFACE,
    region=Region(
        edges=mdb.models[MODELE_POUTRE]
        .parts["Tube_vertical"]
        .edges.getSequenceFromMask(
            mask=("[#1 ]",),
        )
    ),
    sectionName="Section-circulaire-poutre",
    thicknessAssignment=FROM_SECTION,
)
# Association tube horizontal
mdb.models[MODELE_POUTRE].parts["Part-2"].Set(
    edges=mdb.models[MODELE_POUTRE]
    .parts["Part-2"]
    .edges.getSequenceFromMask(
        ("[#1 ]",),
    ),
    name="tige horizontale",
)
mdb.models[MODELE_POUTRE].parts["Part-2"].SectionAssignment(
    offset=0.0,
    offsetField="",
    offsetType=MIDDLE_SURFACE,
    region=mdb.models[MODELE_POUTRE].parts["Part-2"].sets["tige horizontale"],
    sectionName="Section-circulaire-poutre",
    thicknessAssignment=FROM_SECTION,
)

## Assembly
# initier assemblage
mdb.models[MODELE_POUTRE].rootAssembly.DatumCsysByDefault(CARTESIAN)
# import des pièces
mdb.models[MODELE_POUTRE].rootAssembly.Instance(
    dependent=ON,
    name="Tube_vertical-1",
    part=mdb.models[MODELE_POUTRE].parts["Tube_vertical"],
)
mdb.models[MODELE_POUTRE].rootAssembly.Instance(
    dependent=ON, name="Part-3-1", part=mdb.models[MODELE_POUTRE].parts["Part-3"]
)
mdb.models[MODELE_POUTRE].rootAssembly.Instance(
    dependent=ON, name="Part-2-1", part=mdb.models[MODELE_POUTRE].parts["Part-2"]
)
# déplacement des pièces
mdb.models[MODELE_POUTRE].rootAssembly.translate(
    instanceList=("Part-3-1",), vector=(50.0, 50.0, 0.0)
)
mdb.models[MODELE_POUTRE].rootAssembly.translate(
    instanceList=("Part-2-1",), vector=(150.0, 100.0, 0.0)
)

## Step
mdb.models[MODELE_POUTRE].StaticStep(
    description="Calcul des contraintes résultantes de la pression interne de 150 bar",
    name="Etude Statique",
    previous="Initial",
)

## Load
# mdb.models['Model-3D-poutre'].rootAssembly.Surface(end2Edges=
#     mdb.models['Model-3D-poutre'].rootAssembly.instances['Tube_vertical-1'].edges.getSequenceFromMask(
#     mask=('[#1 ]', ), )+\
#     mdb.models['Model-3D-poutre'].rootAssembly.instances['Part-3-1'].edges.getSequenceFromMask(
#     mask=('[#1 ]', ), )+\
#     mdb.models['Model-3D-poutre'].rootAssembly.instances['Part-2-1'].edges.getSequenceFromMask(
#     mask=('[#1 ]', ), ), name='surface1')
# mdb.models['Model-3D-poutre'].Pressure(amplitude=UNSET, createStepName=
#     'Etude Statique', distributionType=UNIFORM, field='', magnitude=15.0, name=
#     'Chargement pression', region=
#     mdb.models['Model-3D-poutre'].rootAssembly.surfaces['surface1'])

mdb.models[MODELE_POUTRE].rootAssembly.Set(
    edges=mdb.models[MODELE_POUTRE]
    .rootAssembly.instances["Tube_vertical-1"]
    .edges.getSequenceFromMask(
        mask=("[#1 ]",),
    )
    + mdb.models[MODELE_POUTRE]
    .rootAssembly.instances["Part-3-1"]
    .edges.getSequenceFromMask(
        mask=("[#1 ]",),
    )
    + mdb.models[MODELE_POUTRE]
    .rootAssembly.instances["Part-2-1"]
    .edges.getSequenceFromMask(
        mask=("[#1 ]",),
    ),
    name="tuyau complet",
)
mdb.models[MODELE_POUTRE].PipePressure(
    amplitude=UNSET,
    createStepName="Etude Statique",
    diameter=40.0,
    distributionType=UNIFORM,
    field="",
    magnitude=15.0,
    name="Load-2",
    region=mdb.models[MODELE_POUTRE].rootAssembly.sets["tuyau complet"],
    side=INTERNAL,
)

## Mesh
mdb.models[MODELE_POUTRE].parts["Part-2"].seedPart(
    deviationFactor=0.1, minSizeFactor=0.1, size=10.0
)
mdb.models[MODELE_POUTRE].parts["Part-2"].setElementType(
    elemTypes=(ElemType(elemCode=B31, elemLibrary=STANDARD),),
    regions=(
        mdb.models[MODELE_POUTRE]
        .parts["Part-2"]
        .edges.getSequenceFromMask(
            ("[#1 ]",),
        ),
    ),
)
mdb.models[MODELE_POUTRE].parts["Part-2"].generateMesh()

mdb.models[MODELE_POUTRE].parts["Part-3"].seedPart(
    deviationFactor=0.1, minSizeFactor=0.1, size=3.0
)
mdb.models[MODELE_POUTRE].parts["Part-3"].setElementType(
    elemTypes=(ElemType(elemCode=B31, elemLibrary=STANDARD),),
    regions=(
        mdb.models[MODELE_POUTRE]
        .parts["Part-3"]
        .edges.getSequenceFromMask(
            ("[#1 ]",),
        ),
    ),
)
mdb.models[MODELE_POUTRE].parts["Part-3"].generateMesh()

mdb.models[MODELE_POUTRE].parts["Tube_vertical"].seedPart(
    deviationFactor=0.1, minSizeFactor=0.1, size=10.0
)
mdb.models[MODELE_POUTRE].parts["Tube_vertical"].setElementType(
    elemTypes=(ElemType(elemCode=B31, elemLibrary=STANDARD),),
    regions=(
        mdb.models[MODELE_POUTRE]
        .parts["Tube_vertical"]
        .edges.getSequenceFromMask(
            ("[#1 ]",),
        ),
    ),
)
mdb.models[MODELE_POUTRE].parts["Tube_vertical"].generateMesh()

## Beam orientation
mdb.models[MODELE_POUTRE].parts["Tube_vertical"].Set(
    edges=mdb.models[MODELE_POUTRE]
    .parts["Tube_vertical"]
    .edges.getSequenceFromMask(
        ("[#1 ]",),
    ),
    name="tige verticale",
)
mdb.models[MODELE_POUTRE].parts["Tube_vertical"].assignBeamSectionOrientation(
    method=N1_COSINES,
    n1=(0.0, 0.0, -1.0),
    region=mdb.models[MODELE_POUTRE].parts["Tube_vertical"].sets["tige verticale"],
)
mdb.models[MODELE_POUTRE].parts["Part-3"].Set(
    edges=mdb.models[MODELE_POUTRE]
    .parts["Part-3"]
    .edges.getSequenceFromMask(
        ("[#1 ]",),
    ),
    name="Set-3",
)
mdb.models[MODELE_POUTRE].parts["Part-3"].assignBeamSectionOrientation(
    method=N1_COSINES,
    n1=(0.0, 0.0, -1.0),
    region=mdb.models[MODELE_POUTRE].parts["Part-3"].sets["Set-3"],
)
mdb.models[MODELE_POUTRE].parts["Part-2"].Set(
    edges=mdb.models[MODELE_POUTRE]
    .parts["Part-2"]
    .edges.getSequenceFromMask(
        ("[#1 ]",),
    ),
    name="Set-4",
)
mdb.models[MODELE_POUTRE].parts["Part-2"].assignBeamSectionOrientation(
    method=N1_COSINES,
    n1=(0.0, 0.0, -1.0),
    region=mdb.models[MODELE_POUTRE].parts["Part-2"].sets["Set-4"],
)

## Job
mdb.models[MODELE_POUTRE].rootAssembly.regenerate()
mdb.Job(
    atTime=None,
    contactPrint=OFF,
    description="",
    echoPrint=OFF,
    explicitPrecision=SINGLE,
    getMemoryFromAnalysis=True,
    historyPrint=OFF,
    memory=90,
    memoryUnits=PERCENTAGE,
    model=MODELE_POUTRE,
    modelPrint=OFF,
    multiprocessingMode=DEFAULT,
    name="First_try",
    nodalOutputPrecision=SINGLE,
    numCpus=1,
    numGPUs=0,
    numThreadsPerMpiProcess=1,
    queue=None,
    resultsFormat=ODB,
    scratch="",
    type=ANALYSIS,
    userSubroutine="",
    waitHours=0,
    waitMinutes=0,
)
mdb.jobs["First_try"].submit(consistencyChecking=OFF)
