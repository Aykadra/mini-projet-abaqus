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
## Création du modèle
mdb.Model(modelType=STANDARD_EXPLICIT, name='Model-3D-poutre')
## Création  de l'esquisse
# Tube vertical
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].Line(point1=(0.0, -50.0), 
    point2=(0.0, 50.0))
mdb.models['Model-3D-poutre'].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-3D-poutre'].sketches['__profile__'].geometry[2])
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Tube_vertical'
    , type=DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
# tube horizontal
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].Line(point1=(-100.0, 0.0)
    , point2=(100.0, 0.0))
mdb.models['Model-3D-poutre'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-3D-poutre'].sketches['__profile__'].geometry[2])
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Part-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Part-2'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
# coude
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].ArcByCenterEnds(center=(
    0.0, 0.0), direction=CLOCKWISE, point1=(-50.0, 0.0), point2=(0.0, 50.0))
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Part-3', type=
    DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Part-3'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
## Matériaux
mdb.models['Model-3D-poutre'].Material(name='Acier 304')
mdb.models['Model-3D-poutre'].materials['Acier 304'].Density(table=((7.9e-05, 
    ), ))
mdb.models['Model-3D-poutre'].materials['Acier 304'].Elastic(table=((200000.0, 
    0.3), ))
## Sections
mdb.models['Model-3D-poutre'].PipeProfile(name='Profil-circulaire-creux', r=
    50.0, t=10.0)
mdb.models['Model-3D-poutre'].BeamSection(beamSectionOffset=(0.0, 0.0), 
    consistentMassMatrix=False, integration=DURING_ANALYSIS, material=
    'Acier 304', name='Section-circulaire-poutre', poissonRatio=0.0, profile=
    'Profil-circulaire-creux', temperatureVar=LINEAR)
# Association coude
 mdb.models['Model-3D-poutre'].parts['Part-3'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    edges=mdb.models['Model-3D-poutre'].parts['Part-3'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='Section-circulaire-poutre', 
    thicknessAssignment=FROM_SECTION)
# Association tube vertical
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].SectionAssignment(offset=
    0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    edges=mdb.models['Model-3D-poutre'].parts['Tube_vertical'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='Section-circulaire-poutre', 
    thicknessAssignment=FROM_SECTION)
# Association tube horizontal
mdb.models['Model-3D-poutre'].parts['Part-2'].Set(edges=
    mdb.models['Model-3D-poutre'].parts['Part-2'].edges.getSequenceFromMask((
    '[#1 ]', ), ), name='tige horizontale')
mdb.models['Model-3D-poutre'].parts['Part-2'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-3D-poutre'].parts['Part-2'].sets['tige horizontale'], 
    sectionName='Section-circulaire-poutre', thicknessAssignment=FROM_SECTION)

## Assembly
# initier assemblage
mdb.models['Model-3D-poutre'].rootAssembly.DatumCsysByDefault(CARTESIAN)
# import des pièces
mdb.models['Model-3D-poutre'].rootAssembly.Instance(dependent=ON, name=
    'Tube_vertical-1', part=
    mdb.models['Model-3D-poutre'].parts['Tube_vertical'])
mdb.models['Model-3D-poutre'].rootAssembly.Instance(dependent=ON, name=
    'Part-3-1', part=mdb.models['Model-3D-poutre'].parts['Part-3'])
mdb.models['Model-3D-poutre'].rootAssembly.Instance(dependent=ON, name=
    'Part-2-1', part=mdb.models['Model-3D-poutre'].parts['Part-2'])
# déplacement des pièces
mdb.models['Model-3D-poutre'].rootAssembly.translate(instanceList=('Part-3-1', 
    ), vector=(50.0, 50.0, 0.0))
mdb.models['Model-3D-poutre'].rootAssembly.translate(instanceList=('Part-2-1', 
    ), vector=(150.0, 100.0, 0.0))

## Step
mdb.models['Model-3D-poutre'].StaticStep(description=
    'Calcul des contraintes résultantes de la pression interne de 150 bar', 
    name='Etude Statique', previous='Initial')

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

mdb.models['Model-3D-poutre'].rootAssembly.Set(edges=
    mdb.models['Model-3D-poutre'].rootAssembly.instances['Tube_vertical-1'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )+\
    mdb.models['Model-3D-poutre'].rootAssembly.instances['Part-3-1'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )+\
    mdb.models['Model-3D-poutre'].rootAssembly.instances['Part-2-1'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), ), name='tuyau complet')
mdb.models['Model-3D-poutre'].PipePressure(amplitude=UNSET, createStepName=
    'Etude Statique', diameter=40.0, distributionType=UNIFORM, field='', 
    magnitude=15.0, name='Load-2', region=
    mdb.models['Model-3D-poutre'].rootAssembly.sets['tuyau complet'], side=
    INTERNAL)

## Mesh
mdb.models['Model-3D-poutre'].parts['Part-2'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=10.0)
mdb.models['Model-3D-poutre'].parts['Part-2'].setElementType(elemTypes=(
    ElemType(elemCode=B31, elemLibrary=STANDARD), ), regions=(
    mdb.models['Model-3D-poutre'].parts['Part-2'].edges.getSequenceFromMask((
    '[#1 ]', ), ), ))
mdb.models['Model-3D-poutre'].parts['Part-2'].generateMesh()

mdb.models['Model-3D-poutre'].parts['Part-3'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=3.0)
mdb.models['Model-3D-poutre'].parts['Part-3'].setElementType(elemTypes=(
    ElemType(elemCode=B31, elemLibrary=STANDARD), ), regions=(
    mdb.models['Model-3D-poutre'].parts['Part-3'].edges.getSequenceFromMask((
    '[#1 ]', ), ), ))
mdb.models['Model-3D-poutre'].parts['Part-3'].generateMesh()

mdb.models['Model-3D-poutre'].parts['Tube_vertical'].seedPart(deviationFactor=
    0.1, minSizeFactor=0.1, size=10.0)
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].setElementType(elemTypes=(
    ElemType(elemCode=B31, elemLibrary=STANDARD), ), regions=(
    mdb.models['Model-3D-poutre'].parts['Tube_vertical'].edges.getSequenceFromMask(
    ('[#1 ]', ), ), ))
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].generateMesh()

## Beam orientation
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].Set(edges=
    mdb.models['Model-3D-poutre'].parts['Tube_vertical'].edges.getSequenceFromMask(
    ('[#1 ]', ), ), name='tige verticale')
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models['Model-3D-poutre'].parts['Tube_vertical'].sets['tige verticale'])
mdb.models['Model-3D-poutre'].parts['Part-3'].Set(edges=
    mdb.models['Model-3D-poutre'].parts['Part-3'].edges.getSequenceFromMask((
    '[#1 ]', ), ), name='Set-3')
mdb.models['Model-3D-poutre'].parts['Part-3'].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models['Model-3D-poutre'].parts['Part-3'].sets['Set-3'])
mdb.models['Model-3D-poutre'].parts['Part-2'].Set(edges=
    mdb.models['Model-3D-poutre'].parts['Part-2'].edges.getSequenceFromMask((
    '[#1 ]', ), ), name='Set-4')
mdb.models['Model-3D-poutre'].parts['Part-2'].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models['Model-3D-poutre'].parts['Part-2'].sets['Set-4'])

## Job
mdb.models['Model-3D-poutre'].rootAssembly.regenerate()
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-3D-poutre', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='First_try', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, numThreadsPerMpiProcess=1, queue=None, resultsFormat=
    ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, 
    waitMinutes=0)
mdb.jobs['First_try'].submit(consistencyChecking=OFF)