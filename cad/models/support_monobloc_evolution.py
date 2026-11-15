#!/usr/bin/env python3
"""Prototype d'un support monobloc paramétrique pour EasyScanner Evolution.

IMPORTANT : dimensions génériques pour essai de fabrication, non ajustées au
smartphone de l'utilisateur. Aucun métal / vis / colle dans la pièce imprimée.
Le laser linéaire Ø12 mm reste un composant séparé inséré dans le clip.

Montage: le téléphone se glisse depuis le HAUT du cadre, écran vers +Z,
caméra arrière vers -Z. Le laser est à droite, optique dirigée vers -Z,
inclinée vers le téléphone. La ligne lumineuse doit ensuite être orientée
par rotation du module autour de son axe et vérifiée sur mire.

Dépendance: cadquery. Unités: millimètres.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import math
import cadquery as cq


@dataclass
class Dimensions:
    phone_width: float = 76.0
    phone_length: float = 160.0
    phone_thickness: float = 10.0  # téléphone + coque éventuelle
    laser_diameter: float = 12.0
    laser_tilt_deg: float = 15.0
    laser_offset: float = 42.0  # depuis le bord externe du cadre
    laser_y: float = 36.0  # axe du laser le long du téléphone
    side_clearance: float = 0.6
    thickness_clearance: float = 0.9


def bar(x0, y0, z0, dx, dy, dz):
    return cq.Solid.makeBox(dx, dy, dz, cq.Vector(x0, y0, z0))


def strut(a, b, width=11.0, depth=6.2):
    """Longeron extrudé : capsule 2D au sol avec extrémités arrondies."""
    (x0, y0), (x1, y1) = a, b
    length = math.hypot(x1 - x0, y1 - y0)
    if length < width:
        raise ValueError('Longeron trop court')
    angle = math.degrees(math.atan2(y1 - y0, x1 - x0))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return (cq.Workplane('XY')
            .center(mx, my).slot2D(length + width, width, angle)
            .extrude(depth).val())


def build(p: Dimensions):
    if not (58 <= p.phone_width <= 95 and 120 <= p.phone_length <= 200
            and 6 <= p.phone_thickness <= 16):
        raise ValueError('Dimensions téléphone hors plage prévue pour ce prototype')
    if not (9 <= p.laser_diameter <= 16 and 0 <= p.laser_tilt_deg <= 25):
        raise ValueError('Diamètre ou inclinaison laser hors plage prototype')
    if not (28 <= p.laser_offset <= 70):
        raise ValueError('Décalage laser hors plage prototype')

    hw = p.phone_width / 2 + p.side_clearance
    y0 = -p.phone_length / 2 + 6.0
    y1 = p.phone_length / 2 - 4.0
    length = y1 - y0
    floor_h = 3.4
    side_wall = 3.8
    under_phone = 4.4
    lip_inset = 1.9
    lip_height = 1.7
    cavity_top = floor_h + p.phone_thickness + p.thickness_clearance
    top_z = cavity_top + lip_height

    # Deux glissières en C, connectées au bas et au dos :
    # la caméra arrière ne doit rencontrer qu'un cadre ouvert.
    left_floor = bar(-hw-side_wall, y0, 0, side_wall+under_phone, length, floor_h)
    right_floor = bar(hw-under_phone, y0, 0, side_wall+under_phone, length, floor_h)
    left_wall = bar(-hw-side_wall, y0, floor_h, side_wall, length, top_z-floor_h)
    right_wall = bar(hw, y0, floor_h, side_wall, length, top_z-floor_h)
    left_lip = bar(-hw, y0, cavity_top, lip_inset, length, lip_height)
    right_lip = bar(hw-lip_inset, y0, cavity_top, lip_inset, length, lip_height)

    # Butée basse : empêche le téléphone de glisser par le bas.
    bottom_stop = bar(-hw-side_wall, y0-6.5, 0, 2*(hw+side_wall), 6.6, cavity_top-0.6)
    # Traverse arrière dans la moitié basse du téléphone, loin des blocs photo
    # habituels en haut ; vérifier malgré tout selon le modèle exact.
    mid_y = -p.phone_length*0.20
    back_bridge = bar(-hw-side_wall, mid_y-5.0, 0, 2*(hw+side_wall), 10.0, floor_h)
    pieces = [left_floor,right_floor,left_wall,right_wall,left_lip,right_lip,
              bottom_stop,back_bridge]

    # Triangle de rigidification à droite : aucun profilé métallique.
    edge_x = hw + side_wall - 1.5
    lx = hw + side_wall + p.laser_offset
    ly = p.laser_y
    pieces += [
        strut((edge_x, y0 + 26), (lx-3, ly), 11.5, 6.2),
        strut((edge_x, y1 - 20), (lx-2, ly), 11.5, 6.2),
        cq.Solid.makeCylinder(p.laser_diameter/2 + 4.0, 6.2, cq.Vector(lx,ly,0))
    ]

    # Clip C intégré incliné vers le champ de la caméra.
    # Le diamètre du trou laisse 0,1 mm de jeu pour un module nominal 12 mm.
    inner_r = (p.laser_diameter + 0.10)/2
    outer_r = inner_r + 3.7
    base_z = 5.0
    clip_height = 26.0
    pivot = cq.Vector(lx,ly,base_z)
    axis_y = cq.Vector(lx,ly+1,base_z)
    outer = cq.Solid.makeCylinder(outer_r,clip_height,pivot)
    outer = outer.rotate(pivot,axis_y,p.laser_tilt_deg)
    pieces.append(outer)

    # Union AVANT perçage afin que rien n'obstrue le passage du laser.
    body = cq.Workplane(obj=pieces[0])
    for part in pieces[1:]:
        body = body.union(cq.Workplane(obj=part))
    shape = body.val()

    bore = cq.Solid.makeCylinder(inner_r,clip_height+12,
                                  cq.Vector(lx,ly,base_z-6))
    bore = bore.rotate(pivot,axis_y,p.laser_tilt_deg)
    shape = shape.cut(bore)
    split = bar(lx+inner_r-1.0,ly-1.3,base_z-6,
                outer_r-inner_r+6,2.6,clip_height+12)
    split = split.rotate(pivot,axis_y,p.laser_tilt_deg)
    shape = shape.cut(split).clean()
    if not shape.isValid():
        raise ValueError('La géométrie CAO est invalide')
    if len(shape.Solids()) != 1:
        raise ValueError('Le modèle comporte plusieurs solides : ' + str(len(shape.Solids())))
    return shape


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--largeur', type=float, default=76, help='Largeur téléphone en mm, coque incluse')
    parser.add_argument('--longueur', type=float, default=160, help='Longueur téléphone en mm')
    parser.add_argument('--epaisseur', type=float, default=10, help='Épaisseur téléphone en mm')
    parser.add_argument('--laser', type=float, default=12, help='Diamètre laser en mm')
    parser.add_argument('--inclinaison', type=float, default=15, help='Angle du laser vers le centre, degrés')
    parser.add_argument('--decalage', type=float, default=42, help='Déport latéral du laser en mm')
    parser.add_argument('--sortie', type=Path, default=Path('.'))
    args = parser.parse_args()
    dims = Dimensions(phone_width=args.largeur,phone_length=args.longueur,
                      phone_thickness=args.epaisseur,laser_diameter=args.laser,
                      laser_tilt_deg=args.inclinaison,laser_offset=args.decalage)
    shape = build(dims)
    args.sortie.mkdir(parents=True,exist_ok=True)
    stl = args.sortie/'EasyScanner_Evolution_support_monobloc_prototype.stl'
    step = args.sortie/'EasyScanner_Evolution_support_monobloc_prototype.step'
    shape.exportStl(str(stl),0.10,0.1)
    cq.exporters.export(shape,str(step))
    bb = shape.BoundingBox()
    print(f'Solide unique : {len(shape.Solids())}; valide : {shape.isValid()}')
    print(f'Encombrement : {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm')
    print(f'Volume matière : {shape.Volume()/1000:.1f} cm³')
    print(f'STL : {stl}\nSTEP : {step}')

if __name__ == '__main__':
    main()
