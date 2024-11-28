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
mdb.models.changeKey(fromName='Model-1', toName='Model-3D-poutre')
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
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].ArcByCenterEnds(center=(
    0.0, 0.0), direction=CLOCKWISE, point1=(-50.0, 0.0), point2=(0.0, 50.0))
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Part-3', type=
    DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Part-3'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
