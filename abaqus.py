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

# noms des objets
MODELE_POUTRE = "Model-3D-poutre"
PIECE_1_TUYAU_VERTICAL = "Tuyau vertical"
PIECE_2_TUYAU_HORIZONTAL = "Tuyau horizontal"
PIECE_3_COUDE = "Coude"
ACIER_304 = "Acier 304"
INCONEL_600 = "Inconel 600"

PROFIL_CIRCULAIRE_CREUX = "Profil-circulaire-creux"
SECTION_CIRCULAIRE_POUTRE = "Section-circulaire-poutre"

ETAPE_ANALYSE_MODALE = "Analyse modale"
ETAPE_CALCUL_STATIQUE = "Etude statique"

# Paramètres de l'étude
RAYON_TUYAU = 500  # mm
EPAISSEUR_TUYAU = 10  # mm
# Paramètre de calcul
NOMBRE_MAX_DE_MODES = 15
# Dimensions géométriques
HAUTEUR_TIGE_VERTICALE = 1000  # mm
LONGEUR_TIGE_HORIZONTALE = 2000  # mm
RAYON_DE_COURBURE_COUDE = 500  # mm
# Constantes matériaux
DENSITE_ACIER = 7.9e-05  # kg/mm²
MODULE_YOUNG_ACIER = 2e5  # kg/mm²
POISSON_ACIER = 0.3  # s.u.



## Création du modèle
mdb.Model(modelType=STANDARD_EXPLICIT, name=MODELE_POUTRE)


## Création  de l'esquisse
# Tube vertical
def creer_piece_1():
    mdb.models[MODELE_POUTRE].ConstrainedSketch(
        name="__profile__", sheetSize=HAUTEUR_TIGE_VERTICALE + 1
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].Line(
        point1=(0.0, -HAUTEUR_TIGE_VERTICALE / 2),
        point2=(0.0, HAUTEUR_TIGE_VERTICALE / 2),
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].VerticalConstraint(
        addUndoState=False,
        entity=mdb.models[MODELE_POUTRE].sketches["__profile__"].geometry[2],
    )
    mdb.models[MODELE_POUTRE].Part(
        dimensionality=THREE_D, name=PIECE_1_TUYAU_VERTICAL, type=DEFORMABLE_BODY
    )
    mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].BaseWire(
        sketch=mdb.models[MODELE_POUTRE].sketches["__profile__"]
    )
    del mdb.models[MODELE_POUTRE].sketches["__profile__"]


creer_piece_1()


# tube horizontal
def creer_piece_2():
    mdb.models[MODELE_POUTRE].ConstrainedSketch(
        name="__profile__", sheetSize=LONGEUR_TIGE_HORIZONTALE
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].Line(
        point1=(-LONGEUR_TIGE_HORIZONTALE / 2, 0.0),
        point2=(LONGEUR_TIGE_HORIZONTALE / 2, 0.0),
    )
    mdb.models[MODELE_POUTRE].sketches["__profile__"].HorizontalConstraint(
        addUndoState=False,
        entity=mdb.models[MODELE_POUTRE].sketches["__profile__"].geometry[2],
    )
    mdb.models[MODELE_POUTRE].Part(
        dimensionality=THREE_D, name=PIECE_2_TUYAU_HORIZONTAL, type=DEFORMABLE_BODY
    )
    mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].BaseWire(
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
        point1=(-RAYON_DE_COURBURE_COUDE, 0.0),
        point2=(0.0, RAYON_DE_COURBURE_COUDE),
    )
    mdb.models[MODELE_POUTRE].Part(
        dimensionality=THREE_D, name=PIECE_3_COUDE, type=DEFORMABLE_BODY
    )
    mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE].BaseWire(
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
    density=DENSITE_ACIER,
    young_modulus=MODULE_YOUNG_ACIER,
    poisson=POISSON_ACIER,
)

## Sections
mdb.models[MODELE_POUTRE].PipeProfile(
    name=PROFIL_CIRCULAIRE_CREUX, r=RAYON_TUYAU, t=EPAISSEUR_TUYAU
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
mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE].SectionAssignment(
    offset=0.0,
    offsetField="",
    offsetType=MIDDLE_SURFACE,
    region=Region(
        edges=mdb.models[MODELE_POUTRE]
        .parts[PIECE_3_COUDE]
        .edges.getSequenceFromMask(
            mask=("[#1 ]",),
        )
    ),
    sectionName=SECTION_CIRCULAIRE_POUTRE,
    thicknessAssignment=FROM_SECTION,
)
SET_COUDE = 'Set coude'
mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE].Set(edges=
    mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE].edges.getSequenceFromMask((
    '[#1 ]', ), ), name=SET_COUDE)
mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE].sets[SET_COUDE])

# Ici

# Association tube vertical
mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].SectionAssignment(
    offset=0.0,
    offsetField="",
    offsetType=MIDDLE_SURFACE,
    region=Region(
        edges=mdb.models[MODELE_POUTRE]
        .parts[PIECE_1_TUYAU_VERTICAL]
        .edges.getSequenceFromMask(
            mask=("[#1 ]",),
        )
    ),
    sectionName=SECTION_CIRCULAIRE_POUTRE,
    thicknessAssignment=FROM_SECTION,
)
SET_TUBE_VERTICAL = 'Set tube vertical'
mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].Set(edges=
    mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].edges.getSequenceFromMask((
    '[#1 ]', ), ), name=SET_TUBE_VERTICAL)
mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].sets[SET_TUBE_VERTICAL])

# Association tube horizontal
SET_TUBE_HORIZONTALE = 'Set tube horizontal'
mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].Set(
    edges=mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].edges.getSequenceFromMask(("[#1 ]", ), ), name=SET_TUBE_HORIZONTALE)
mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].SectionAssignment(
    offset=0.0,
    offsetField="",
    offsetType=MIDDLE_SURFACE,
    region=mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].sets[SET_TUBE_HORIZONTALE],
    sectionName=SECTION_CIRCULAIRE_POUTRE,
    thicknessAssignment=FROM_SECTION,
)
mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].sets[SET_TUBE_HORIZONTALE])

## Assembly
# initier assemblage
mdb.models[MODELE_POUTRE].rootAssembly.DatumCsysByDefault(CARTESIAN)
# import des pièces
mdb.models[MODELE_POUTRE].rootAssembly.Instance(
    dependent=ON, name=PIECE_1_TUYAU_VERTICAL+"-1", part=mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL],
)
mdb.models[MODELE_POUTRE].rootAssembly.Instance(
    dependent=ON, name=PIECE_3_COUDE+"-1", part=mdb.models[MODELE_POUTRE].parts[PIECE_3_COUDE]
)
mdb.models[MODELE_POUTRE].rootAssembly.Instance(
    dependent=ON, name=PIECE_2_TUYAU_HORIZONTAL+"-1", part=mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL]
)

# déplacement des pièces
mdb.models[MODELE_POUTRE].rootAssembly.translate(
    instanceList=(PIECE_2_TUYAU_HORIZONTAL+"-1",), vector=(LONGEUR_TIGE_HORIZONTALE/2,RAYON_TUYAU,0.0)
)
mdb.models[MODELE_POUTRE].rootAssembly.translate(
    instanceList=(PIECE_1_TUYAU_VERTICAL+"-1",), vector=(-RAYON_TUYAU, -HAUTEUR_TIGE_VERTICALE/2, 0.0)
)
## Interactions
EXTREMITE_TIGE_VERTICALE= "extremité-tige-verticale"
EXTREMITE_TIGE_HORIZONTALE= "Extremité tige horizontale"
EXTREMITE_BASSE_COUDE = "extremité-basse-coude"
EXTREMITE_HAUTE_COUDE = "extremité haute coude"
mdb.models[MODELE_POUTRE].rootAssembly.Set(name=EXTREMITE_TIGE_VERTICALE, 
    vertices=
    mdb.models[MODELE_POUTRE].rootAssembly.instances[PIECE_1_TUYAU_VERTICAL+'-1'].vertices.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models[MODELE_POUTRE].rootAssembly.Set(name=EXTREMITE_BASSE_COUDE, 
    vertices=
    mdb.models[MODELE_POUTRE].rootAssembly.instances[PIECE_3_COUDE+'-1'].vertices.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models[MODELE_POUTRE].rootAssembly.Set(name=EXTREMITE_TIGE_HORIZONTALE, 
    vertices=
    mdb.models[MODELE_POUTRE].rootAssembly.instances[PIECE_2_TUYAU_HORIZONTAL+'-1'].vertices.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models[MODELE_POUTRE].rootAssembly.Set(name=EXTREMITE_HAUTE_COUDE, 
    vertices=
    mdb.models[MODELE_POUTRE].rootAssembly.instances[PIECE_3_COUDE+'-1'].vertices.getSequenceFromMask(
    ('[#2 ]', ), ))
SOUDURE_BASSE = "Soudure basse"
SOUDURE_HAUTE = "Soudure haute"
mdb.models[MODELE_POUTRE].Tie(adjust=ON, main=
    mdb.models[MODELE_POUTRE].rootAssembly.sets[EXTREMITE_TIGE_VERTICALE]
    , name=SOUDURE_BASSE, positionToleranceMethod=COMPUTED, secondary=
    mdb.models[MODELE_POUTRE].rootAssembly.sets[EXTREMITE_BASSE_COUDE], 
    thickness=ON, tieRotations=ON)
mdb.models[MODELE_POUTRE].Tie(adjust=ON, main=
    mdb.models[MODELE_POUTRE].rootAssembly.sets[EXTREMITE_TIGE_HORIZONTALE]
    , name=SOUDURE_HAUTE, positionToleranceMethod=COMPUTED, secondary=
    mdb.models[MODELE_POUTRE].rootAssembly.sets[EXTREMITE_HAUTE_COUDE], 
    thickness=ON, tieRotations=ON)

## Step
mdb.models[MODELE_POUTRE].FrequencyStep(description='Analyse modale', 
    limitSavedEigenvectorRegion=None, name=ETAPE_ANALYSE_MODALE, numEigen=NOMBRE_MAX_DE_MODES, previous=
    'Initial')

mdb.models[MODELE_POUTRE].StaticStep(
    description="Calcul des contraintes résultantes de la pression interne de 150 bar",
    name=ETAPE_CALCUL_STATIQUE,
    previous=ETAPE_ANALYSE_MODALE,
)

# Partition 
mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].PartitionEdgeByPoint(
    edge=mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].edges[0], point=
    mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].InterestingPoint(
    mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].edges[0], MIDDLE))
mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].PartitionEdgeByPoint(
    edge=mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].edges[0], 
    point=
    mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].InterestingPoint(
    mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].edges[0], MIDDLE))
# Creation set 
mdb.models[MODELE_POUTRE].rootAssembly.Set(name='milieu tige vertical', 
    vertices=
    mdb.models[MODELE_POUTRE].rootAssembly.instances[PIECE_1_TUYAU_VERTICAL+'-1'].vertices.getSequenceFromMask(
    ('[#2 ]', ), ))
## Load
mdb.models[MODELE_POUTRE].DisplacementBC(amplitude=UNSET, createStepName=
    'Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'milieu horizontal', region=Region(
    vertices=mdb.models[MODELE_POUTRE].rootAssembly.instances[PIECE_2_TUYAU_HORIZONTAL+'-1'].vertices.getSequenceFromMask(
    mask=('[#2 ]', ), )), u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=
    UNSET)
mdb.models[MODELE_POUTRE].DisplacementBC(amplitude=UNSET, createStepName=
    'Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'milieu vertical', region=
    mdb.models[MODELE_POUTRE].rootAssembly.sets['milieu tige vertical'], 
    u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models[MODELE_POUTRE].DisplacementBC(amplitude=UNSET, createStepName=
    'Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'Sol', region=Region(
    vertices=mdb.models['Model-3D-poutre'].rootAssembly.instances[PIECE_1_TUYAU_VERTICAL+'-1'].vertices.getSequenceFromMask(
    mask=('[#1 ]', ), )), u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=
    UNSET)


# mdb.models[MODELE_POUTRE].parts[PIECE_1_TUYAU_VERTICAL].generateMesh()
# mdb.models[MODELE_POUTRE].parts[PIECE_2_TUYAU_HORIZONTAL].generateMesh()
'''
## Load
# mdb.models[MODELE_POUTRE].rootAssembly.Surface(end2Edges=
#     mdb.models[MODELE_POUTRE].rootAssembly.instances['Tube_vertical-1'].edges.getSequenceFromMask(
#     mask=('[#1 ]', ), )+\
#     mdb.models[MODELE_POUTRE].rootAssembly.instances['Part-3-1'].edges.getSequenceFromMask(
#     mask=('[#1 ]', ), )+\
#     mdb.models[MODELE_POUTRE].rootAssembly.instances['Part-2-1'].edges.getSequenceFromMask(
#     mask=('[#1 ]', ), ), name='surface1')
# mdb.models[MODELE_POUTRE].Pressure(amplitude=UNSET, createStepName=
#     'Etude Statique', distributionType=UNIFORM, field='', magnitude=15.0, name=
#     'Chargement pression', region=
#     mdb.models[MODELE_POUTRE].rootAssembly.surfaces['surface1'])

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
'''