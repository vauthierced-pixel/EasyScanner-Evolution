#!/usr/bin/env python3
"""EasyScanner Evolution — cadre monobloc RENFORCE pour Redmi Note 14 Pro.

Modele PARAMETRIQUE d'essai, pas de dimensions d'encombrement de coque ou de
bloc photo verifiees. Deux variantes Xiaomi officielles (4G, 5G) sans coque.
La tenue du telephone n'est PAS securisee : inserer un gabarit pour essais.
Unite : millimetres. Dependance : cadquery.

Orientation: ecran du smartphone vers +Z, objectifs vers -Z, laser a droite
avec lentille vers -Z. La camera reste degagee en haut de la face arriere.

La rigidite est recherchee avec:
  * rails en C a paroi 6.0 mm et semelle 5.6 mm;
  * trois traverses inferieures fermees, loin de l'ensemble photo;
  * platine triangulee de 6 mm + nervures de 14 mm sous le laser;
  * bague laser de 4.8 mm d'epaisseur autour d'un bore de diametre parametrable;
  * contreventements rejoints en un SEUL solide.

Cela ne vaut ni calcul de resistance certifie, ni test d'impression reelle.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import math
import cadquery as cq

MODELES = {
    '4g': (74.92, 162.16, 8.24),
    '5g': (74.42, 162.33, 8.40),
}


@dataclass(frozen=True)
class Dimensions:
    variant: str = '4g'
    phone_width: float = 74.92
    phone_length: float = 162.16
    phone_thickness: float = 8.24
    case_width_extra: float = 0.0
    case_length_extra: float = 0.0
    case_thickness_extra: float = 0.0
    laser_diameter: float = 12.0
    laser_tilt_deg: float = 15.0
    laser_offset: float = 38.0
    width_clearance: float = 0.75
    depth_clearance: float = 0.95


def box(x0, y0, z0, dx, dy, dz):
    return cq.Solid.makeBox(dx, dy, dz, cq.Vector(x0, y0, z0))


def beam(a, b, width, height):
    """Nervure a section rectangulaire verticale, extremites arrondies."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy)
    if dist <= 1:
        raise ValueError('Nervure trop courte')
    midx, midy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    theta = math.degrees(math.atan2(dy, dx))
    return cq.Workplane('XY').center(midx, midy).slot2D(dist + width, width, theta).extrude(height).val()


def build(p: Dimensions):
    width = p.phone_width + p.case_width_extra
    length = p.phone_length + p.case_length_extra
    depth = p.phone_thickness + p.case_thickness_extra
    if not (65 <= width <= 92 and 140 <= length <= 185 and 7 <= depth <= 17):
        raise ValueError('Dimensions du telephone hors plage : verifier les mesures')
    if not (9 <= p.laser_diameter <= 16 and 0 <= p.laser_tilt_deg <= 25 and 25 <= p.laser_offset <= 62):
        raise ValueError('Parametres du laser hors plage de ce prototype')

    hw = width / 2 + p.width_clearance
    y0 = -length / 2 + 1.0
    y1 = +length / 2 + 1.0
    rail_len = y1 - y0
    sole = 5.6
    wall = 6.0
    under = 7.0
    lip = 2.5
    lip_h = 2.4
    cavity_top = sole + depth + p.depth_clearance
    total_h = cavity_top + lip_h
    pieces = [
        box(-hw-wall, y0, 0, wall+under, rail_len, sole),
        box(hw-under, y0, 0, wall+under, rail_len, sole),
        box(-hw-wall, y0, sole, wall, rail_len, total_h-sole),
        box(hw, y0, sole, wall, rail_len, total_h-sole),
        box(-hw, y0, cavity_top, lip, rail_len, lip_h),
        box(hw-lip, y0, cavity_top, lip, rail_len, lip_h),
    ]
    pieces.append(box(-hw-wall, y0-8.0, 0, 2*(hw+wall), 8.2, cavity_top-0.8))

    # Traverses sur la face arriere, loin de la camera situee en haut.
    for cy, thickness in ((-length*0.31, 13.0), (-length*0.12, 11.0), (length*0.055, 10.0)):
        pieces.append(box(-hw-wall, cy-thickness/2, 0, 2*(hw+wall), thickness, sole))

    # Peau de contreventement et nervures hautes : maintien du plan laser.
    xr = hw+wall-1.8
    xl = hw+wall+p.laser_offset
    yl = length*0.22
    anchor_lo = y0+19.0
    anchor_hi = y1-20.0
    skin = (cq.Workplane('XY')
            .polyline([(xr-3.4, anchor_lo), (xr-3.4, anchor_hi),
                       (xl+5.0, yl+10), (xl+9.0, yl), (xl+5.0, yl-10)])
            .close().extrude(6.2).val())
    pieces.append(skin)
    pieces.extend([
        beam((xr,anchor_lo+3), (xl-1,yl-1), 15.0, 14.2),
        beam((xr,anchor_hi-3), (xl-1,yl+1), 15.0, 14.2),
        beam((xr,yl-8), (xl-1,yl), 13.0, 13.0),
        cq.Solid.makeCylinder(p.laser_diameter/2+6.5, 14.2, cq.Vector(xl,yl,0)),
    ])

    inner_r = p.laser_diameter/2 + 0.10
    outer_r = inner_r + 4.8
    base_z = 4.6
    clip_h = 29.0
    pivot = cq.Vector(xl,yl,base_z)
    rot_axis = cq.Vector(xl,yl+1.0,base_z)
    sleeve = cq.Solid.makeCylinder(outer_r,clip_h,pivot)
    sleeve = sleeve.rotate(pivot,rot_axis,p.laser_tilt_deg)
    pieces.append(sleeve)

    shape = cq.Workplane(obj=pieces[0])
    for part in pieces[1:]:
        shape = shape.union(cq.Workplane(obj=part))
    solid = shape.val()

    cutter = cq.Solid.makeCylinder(inner_r,clip_h+18,
                                   cq.Vector(xl,yl,base_z-9))
    cutter = cutter.rotate(pivot,rot_axis,p.laser_tilt_deg)
    solid = solid.cut(cutter)
    cut_slot = box(xl+inner_r-0.8, yl-1.4, base_z-9,
                   outer_r-inner_r+8, 2.8, clip_h+18)
    cut_slot = cut_slot.rotate(pivot,rot_axis,p.laser_tilt_deg)
    solid = solid.cut(cut_slot).clean()
    if not solid.isValid() or len(solid.Solids()) != 1:
        raise ValueError('Geometrie non valide ou plusieurs solides')
    return solid


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--modele',choices=['4g','5g'],default='4g')
    ap.add_argument('--coque-largeur',type=float,default=0.0,help='Surcote totale de coque en largeur (mm)')
    ap.add_argument('--coque-longueur',type=float,default=0.0,help='Surcote totale de coque en longueur (mm)')
    ap.add_argument('--coque-epaisseur',type=float,default=0.0,help='Surcote de coque en epaisseur (mm)')
    ap.add_argument('--diametre-laser',type=float,default=12.0)
    ap.add_argument('--angle-laser',type=float,default=15.0)
    ap.add_argument('--sortie',type=Path,default=Path('cad/monobloc-output'))
    args = ap.parse_args()
    w,l,t = MODELES[args.modele]
    p = Dimensions(variant=args.modele,phone_width=w,phone_length=l,
                   phone_thickness=t,case_width_extra=args.coque_largeur,
                   case_length_extra=args.coque_longueur,
                   case_thickness_extra=args.coque_epaisseur,
                   laser_diameter=args.diametre_laser,laser_tilt_deg=args.angle_laser)
    s=build(p)
    args.sortie.mkdir(parents=True,exist_ok=True)
    prefix=f'EasyScanner_Redmi_Note14Pro_{args.modele}_RENFORCE'
    out_stl = args.sortie/(prefix+'.stl')
    out_step= args.sortie/(prefix+'.step')
    s.exportStl(str(out_stl),0.08,0.12)
    cq.exporters.export(s,str(out_step))
    bb=s.BoundingBox()
    print(f'Modele {args.modele}: {w} x {l} x {t} mm (sans coque)')
    print(f'Volume: {s.Volume()/1000:.1f} cm³ ; poids theorique PETG plein: {s.Volume()/1000*1.27:.0f} g')
    print(f'Encombrement: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm')
    print(f'Solides: {len(s.Solids())} ; Valide: {s.isValid()}')
    print('ATTENTION: pas de verrouillage du telephone ; essai avec gabarit seulement.')
    print(out_stl)
    print(out_step)


if __name__ == '__main__':
    main()
