#practicing with CO first
# from pydft import MoleculeBuilder, DFT

# CO = MoleculeBuilder().from_name("CO")

# dft=DFT(CO, basis='sto3g')

# res=dft.scf(tol=1e-4)

# print("Total Electronic energy: %.6f Ht"%res['energy'])

#now on alkane - C2H6
# from pyqint import Molecule
# from pydft import DFT

# filename="/Users/seri/avogadro/c2h6.xyz"

# with open(filename,'r') as f:
#     lines=f.readlines()
    
# num_atoms=int(lines[0].strip())

# mol=Molecule('ethane')

# for i in range(num_atoms):
#     parts=lines[2+i].split()
#     element=parts[0]
#     x,y,z=float(parts[1]), float(parts[2]), float(parts[3])
#     mol.add_atom(element, x, y, z, unit='angstrom')
    
# print(f"your molecule has {mol.get_atoms()} atoms.")

# dft=DFT(mol, basis='sto3g')
# res=dft.scf(tol=1e-4)

# print("All keys in resultL:", res.keys())
# print("Full result: ", res)
# if res['converged']:
#     print(f"Total Electronic energy: {res['energy']:.6f} Hartrees")
# else:
#     print("The calculatoin did not converge")

#solving the keyword issue   
# import os
# from pyqint import Molecule
# from pydft import DFT

# filename="/Users/seri/avogadro/c2h6.xyz"
# with open(filename,'r') as f:
#     lines=f.readlines()
    
# print('===reading file contents---')
# for i, line in enumerate(lines[:10]):
#     print(f"Line {i}: {repr(line)}")
    
# num_atoms=int(lines[0].strip())
# print(f"\nNumber of atoms: {num_atoms}")

# mol=Molecule('ethane')

# print("\nParsed atoms:")
# for i in range(num_atoms):
#     parts=lines[2+i].split()
#     element=parts[0]
#     x,y,z=float(parts[1]), float(parts[2]), float(parts[3])
#     mol.add_atom(element, x, y, z, unit='angstrom')
#     print(f"Atom {i+1}: {element}, Coordinates=({x:.6f}, {y:.6f}, {z:.6f})")

# print(f"\nYour molecule has {mol.get_atoms()} atoms.")

# print("\nVerifying bond lengths")
# coords=[]
# for i in range(num_atoms):
#     parts=lines[2+i].split()
#     x,y,z=float(parts[1]), float(parts[2]), float(parts[3])
#     coords.append((x,y,z))
    
# cc_dist = ((coords[0][0] - coords[1][0])**2 + 
#            (coords[0][1] - coords[1][1])**2 + 
#            (coords[0][2] - coords[1][2])**2)**0.5
# print(f"C-C bond length: {cc_dist:.4f}Angstrom")

# ch_distance=((coords[0][0] - coords[2][0])**2 + 
#            (coords[0][1] - coords[2][1])**2 + 
#            (coords[0][2] - coords[2][2])**2)**0.5
# print(f"C-H bond length: {ch_distance:.4f}Angstrom")

# print("\nRunning DFT calculation...")
# dft = DFT(mol, basis='sto3g')
# res = dft.scf(tol=1e-4)

# # print(f"\nResult keys: {res.keys()}")
# # if 'energy' in res:
# #     print(f"Total Electronic energy: {res['energy']:.6f} Ht")
# #     print(f"Number of iterations: {res.get('iterations', 'N/A')}")
# # else:
# #     print("Calculation didn't return energy. Full result:")
# #     print(res)

#attempting to plot the energy 
# """this failed because the energy calculation did not converge for some bond lengths that were too long for PyPDF to cover."""
# import numpy as np
# import matplotlib.pyplot as plt
# from pyqint import Molecule
# from pydft import DFT
# import math

# def build_ethane(cc_bond_length):
#     """Build ethane with one H on each carbon along the z-axis"""
#     mol = Molecule('ethane')
#     ch_bond = 1.09  # C-H bond length in Å
    
#     # Carbon atoms along z-axis
#     mol.add_atom('C', 0.0, 0.0, -cc_bond_length/2, unit='angstrom')
#     mol.add_atom('C', 0.0, 0.0, cc_bond_length/2, unit='angstrom')
    
#     # === Carbon 1===
#     # Hydrogen 1: Points DOWN along -z (away from the other carbon)
#     mol.add_atom('H', 0.0, 0.0, -cc_bond_length/2 - ch_bond, unit='angstrom')
    
#     # Hydrogen 2 & 3
#     z_up = -cc_bond_length/2 + ch_bond/3
#     xy_dist = ch_bond * 0.9428  # = ch_bond * sqrt(8)/3
    
#     mol.add_atom('H', xy_dist, 0.0, z_up, unit='angstrom')
#     mol.add_atom('H', -xy_dist/2, xy_dist * 0.866, z_up, unit='angstrom')
#     # 0.866 = sqrt(3)/2 for 120° spacing
    
#     # === Carbon 2===
#     # Hydrogen 4: Points UP along +z (away from the other carbon)
#     mol.add_atom('H', 0.0, 0.0, cc_bond_length/2 + ch_bond, unit='angstrom')
    
#     # Hydrogen 5 & 6
#     z_down = cc_bond_length/2 - ch_bond/3
    
#     mol.add_atom('H', -xy_dist/2, xy_dist * 0.866, z_down, unit='angstrom')
#     mol.add_atom('H', -xy_dist/2, -xy_dist * 0.866, z_down, unit='angstrom')
    
#     return mol
    

# def calculate_c2h6_energy(cc_bond_length):
#     try:
#         mol = build_ethane(r)
#         dft = DFT(mol, basis='sto3g')
#         result = dft.scf(tol=1e-4)
        
#         if 'energy' in result:
#             return result['energy']
#         else:
#             print(f"  No energy for r={r:.3f} - result: {result.keys()}")
#             return np.nan
#     except Exception as e:
#         print(f"  Error at r={r:.3f}: {e}")
#         return np.nan

# bond_lengths=np.linspace(1.1, 2.8, 15) #15 steps from 1.1 to 2.8 ANgstroms
# energies=[]

# print("Now Starting PES scan...")
# for r in bond_lengths:
#     print(f"Calculating at r={r:.3f} Angstroms")
#     e = calculate_c2h6_energy(r)
#     energies.append(e)
#     if not np.isnan(e):
#         print(f"  Energy: {e:.6f} Ht")

# valid = ~np.isnan(energies)
# bond_valid = bond_lengths[valid]
# energy_valid = np.array(energies)[valid]

# # plt.figure(figsize=(10, 6))
# # plt.plot(bond_lengths, energies, 'bo-', linewidth=2)
# # plt.xlabel('C-C Bond Length (Å)', fontsize=12)
# # plt.ylabel('Total Energy (Hartrees)', fontsize=12)
# # plt.title('Potential Energy Surface for Ethane (STO-3G)', fontsize=14)
# # plt.grid(True, alpha=0.3)

# # # Mark the minimum
# # min_idx = np.argmin(energies)
# # plt.axvline(bond_lengths[min_idx], color='red', linestyle='--', 
# #             label=f'Equilibrium: {bond_lengths[min_idx]:.3f} Å')
# # plt.legend()
# # plt.show()

# # print(f"Equilibrium C-C bond length: {bond_lengths[min_idx]:.3f} Å")
# # print(f"Minimum energy: {energies[min_idx]:.6f} Ht")

# if len(energy_valid) > 0:
#     plt.figure(figsize=(10, 6))
#     plt.plot(bond_valid, energy_valid, 'bo-', linewidth=2)
#     plt.xlabel('C-C Bond Length (Å)', fontsize=12)
#     plt.ylabel('Total Energy (Hartrees)', fontsize=12)
#     plt.title('Potential Energy Surface for Ethane (STO-3G)', fontsize=14)
#     plt.grid(True, alpha=0.3)
    
#     min_idx = np.argmin(energy_valid)
#     plt.axvline(bond_valid[min_idx], color='red', linestyle='--', 
#                 label=f'Equilibrium: {bond_valid[min_idx]:.3f} Å')
#     plt.legend()
#     plt.show()
    
#     print(f"\nEquilibrium C-C bond length: {bond_valid[min_idx]:.3f} Å")
#     print(f"Minimum energy: {energy_valid[min_idx]:.6f} Ht")
#     print(f"Dissociation energy estimate: {energy_valid[-1] - energy_valid[min_idx]:.6f} Ht")
# else:
#     print("No valid energies. Trying a single calculation at 1.525 Å...")
    
# # just a single test 
#     mol = build_ethane(1.525)
#     dft = DFT(mol, basis='sto3g')
#     result = dft.scf(tol=1e-4)
#     print(f"Single result: {result}")


#the other way around : now reducing the bond length from 2.0 to 1.0 Angstroms (chose 2.0Angstrom to stay within the range of PyDFt)
import numpy as np
import matplotlib.pyplot as plt
from pyqint import Molecule
from pydft import DFT
import math

def build_ethane(cc_bond_length):
    """Build ethane with a given C-C bond length"""
    mol = Molecule('ethane')
    ch_bond = 1.09
    
    # Carbon atoms
    mol.add_atom('C', 0.0, 0.0, -cc_bond_length/2, unit='angstrom')
    mol.add_atom('C', 0.0, 0.0, cc_bond_length/2, unit='angstrom')
    
    # H on C1 (pointing away from C2)
    z1 = -cc_bond_length/2
    mol.add_atom('H', 0.0, 0.0, z1 - ch_bond, unit='angstrom')  # H1
    
    z_offset = ch_bond / 3
    xy_offset = ch_bond * 0.9428  
    mol.add_atom('H', xy_offset, 0.0, z1 - z_offset, unit='angstrom')  # H2
    mol.add_atom('H', -xy_offset/2, xy_offset * 0.866, z1 - z_offset, unit='angstrom')  # H3
    
    # H on C2 (pointing away from C1)
    z2 = cc_bond_length/2
    mol.add_atom('H', 0.0, 0.0, z2 + ch_bond, unit='angstrom')  # H4
    mol.add_atom('H', -xy_offset/2, xy_offset * 0.866, z2 + z_offset, unit='angstrom')  # H5
    mol.add_atom('H', -xy_offset/2, -xy_offset * 0.866, z2 + z_offset, unit='angstrom')  # H6
    
    return mol

def get_atom_coords(mol):
    """
    Extract atom coordinates from Molecule object.
    Returns list of (element, x, y, z) in Angstroms.
    """
    coords = []
    
    if hasattr(mol, 'get_atoms'):
        try:
            atoms = mol.get_atoms()
            for atom in atoms:
                if len(atom) == 4:
                    element = atom[0]
                    x = atom[1] * 0.529177
                    y = atom[2] * 0.529177
                    z = atom[3] * 0.529177
                    coords.append((element, x, y, z))
                elif len(atom) == 2:
                    element = atom[0]
                    x = atom[1][0] * 0.529177
                    y = atom[1][1] * 0.529177
                    z = atom[1][2] * 0.529177
                    coords.append((element, x, y, z))
            if coords:
                return coords
        except:
            pass

def debug_geometry(mol):
    """Print the geometry to verify hydrogens point correctly"""
    coords = get_atom_coords(mol)
    
    if not coords:
        print("  Could not extract coordinates!")
        return False
    
    print("\n=== Geometry Debug ===")
    print(f"Found {len(coords)} atoms")
    
    # Get C pos.
    if len(coords) >= 2 and coords[0][0] == 'C' and coords[1][0] == 'C':
        c1_z = coords[0][3]
        c2_z = coords[1][3]
        print(f"\nCarbon 1 z: {c1_z:.4f} Å")
        print(f"Carbon 2 z: {c2_z:.4f} Å")
        print(f"C-C distance: {c2_z - c1_z:.4f} Å")
    else:
        print("\n  Could not find carbon atoms at expected positions!")
        return False
    
    # Check H2, H3, H4
    print("\nHydrogens on Carbon 1 (should have z < c1_z, pointing AWAY from C2):")
    hydrogen_count = 0
    for i in range(2, min(5, len(coords))):
        if coords[i][0] == 'H':
            z = coords[i][3]
            direction = "AWAY" if z < c1_z else "TOWARD"
            print(f"  H{i-1}: z = {z:.4f} Å {direction}")
            hydrogen_count += 1
    
    # Check H5, H6, H7
    print("\nHydrogens on Carbon 2 (should have z > c2_z, pointing AWAY from C1):")
    for i in range(5, min(8, len(coords))):
        if coords[i][0] == 'H':
            z = coords[i][3]
            direction = "AWAY" if z > c2_z else "TOWARD"
            print(f"  H{i-1}: z = {z:.4f} Å {direction}")
            hydrogen_count += 1
    
    if hydrogen_count == 6:
        print("\nAll 6 hydrogens found!")
        return True
    else:
        print(f"\nOnly {hydrogen_count} hydrogens found (expected 6)")
        return False

def calculate_energy_safe(mol):
    """Run DFT and return energy, or np.nan if it fails"""
    try:
        dft = DFT(mol, basis='sto3g')
        result = dft.scf(tol=1e-4)
        if 'energy' in result:
            return result['energy']
        else:
            return np.nan
    except Exception as e:
        print(f"  Error: {e}")
        return np.nan

# Test the corrected geometry at 1.525
print("Testing corrected ethane at 1.525 Angstrom...")
mol_test = build_ethane(1.525)
debug_geometry(mol_test)

# Test energy at 1.525 Å
energy_test = calculate_energy_safe(mol_test)
if not np.isnan(energy_test):
    print(f"\nEnergy at 1.525 Angstrom: {energy_test:.6f} Ht")
    print("Calculation converged!")
else:
    print("\nCalculation failed")
#Scan bond lengths from 1.0 to 2.0 Angstrom
print("\n=== Scanning PES from 1.0 to 2.0 Angstrom ===")
bond_lengths = np.linspace(1.0, 2.0, 11)
energies = []

for r in bond_lengths:
    print(f"  r = {r:.3f} Angstrom", end='', flush=True)
    mol = build_ethane(r)  
    e = calculate_energy_safe(mol)
    energies.append(e)
    if not np.isnan(e):
        print(f" -> {e:.6f} Ht")
    else:
        print(" -> FAILED")


valid = ~np.isnan(energies)
if np.sum(valid) > 3:
    plt.figure(figsize=(10, 6))
    plt.plot(bond_lengths[valid], np.array(energies)[valid], 'bo-', linewidth=2, markersize=8)
    plt.xlabel('C-C Bond Length (Angstrom)', fontsize=12)
    plt.ylabel('Total Energy (Hartrees)', fontsize=12)
    plt.title('Potential Energy Surface for Ethane (STO-3G)', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Find minimum
    min_idx = np.argmin(np.array(energies)[valid])
    min_r = bond_lengths[valid][min_idx]
    min_e = np.array(energies)[valid][min_idx]
    
    plt.axvline(min_r, color='red', linestyle='--', linewidth=2,
                label=f'Equilibrium: {min_r:.3f} Angstrom')
    plt.axhline(min_e, color='red', linestyle=':', alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()
    
    print(f"\n=== Results ===")
    print(f"Equilibrium C-C bond length: {min_r:.3f} Angstrom")
    print(f"Minimum energy: {min_e:.6f} Ht")
    print(f"Expected: 1.525 Angstrom (from NIST database)")
    
    if abs(min_r - 1.525) < 0.05:
        print("Your geometrcorrect!")
    else:
        print(" The minimum is still off. Check the hydrogen directions.")
else:
    print(f"Only {np.sum(valid)} valid points. Check the builder function.")