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
# #Scan bond lengths from 1.0 to 2.0 Angstrom 
# print("\n=== Scanning PES from 1.0 to 2.0 Angstrom ===")
# bond_lengths = np.linspace(1.0, 2.0, 11)
# energies = []

# for r in bond_lengths:
#     print(f"  r = {r:.3f} Angstrom", end='', flush=True)
#     mol = build_ethane(r)  
#     e = calculate_energy_safe(mol)
#     energies.append(e)
#     if not np.isnan(e):
#         print(f" -> {e:.6f} Ht")
#     else:
#         print(" -> FAILED")
# min_idx = np.argmin(energies)
# min_r = bond_lengths[min_idx]
# min_e = energies[min_idx]

# print("Minimum index:", min_idx)
# print("Equilibrium bond length:", min_r)
# print("Minimum energy:", min_e)

# #Scan bond lengths from 1.45 to 1.60 Angstrom 
# print("\n=== Scanning PES from 1.45 to 1.60 Angstrom ===")
# bond_lengths = np.linspace(1.45, 1.60, 16)
# energies = []

# for r in bond_lengths:
#     print(f"  r = {r:.3f} Angstrom", end='', flush=True)
#     mol = build_ethane(r)  
#     e = calculate_energy_safe(mol)
#     energies.append(e)
#     if not np.isnan(e):
#         print(f" -> {e:.6f} Ht")
#     else:
#         print(" -> FAILED")
# min_idx = np.argmin(energies)
# min_r = bond_lengths[min_idx]
# min_e = energies[min_idx]

# print("Minimum index:", min_idx)
# print("Equilibrium bond length:", min_r)
# print("Minimum energy:", min_e)

#Scan bond lengths from 1.48 to 1.55 Angstrom 
print("\n=== Scanning PES from 1.48 to 1.55 Angstrom ===")
bond_lengths = np.linspace(1.48, 1.55, 15)
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
min_idx = np.argmin(energies)
min_r = bond_lengths[min_idx]
min_e = energies[min_idx]

print("Minimum index:", min_idx)
print("Equilibrium bond length:", min_r)
print("Minimum energy:", min_e)

# index=(min1+min2+min3)/3
# print(index)

# valid = ~np.isnan(energies)
# if np.sum(valid) > 3:
#     plt.figure(figsize=(10, 6))
#     plt.plot(bond_lengths[valid], np.array(energies)[valid], 'bo-', linewidth=2, markersize=8)
#     plt.xlabel('C-C Bond Length (Angstrom)', fontsize=12)
#     plt.ylabel('Total Energy (Hartrees)', fontsize=12)
#     plt.title('Potential Energy Surface for Ethane (STO-3G)', fontsize=14)
#     plt.grid(True, alpha=0.3)
    
#     # Find minimum
#     min_idx = np.argmin(np.array(energies)[valid])
#     min_r = bond_lengths[valid][min_idx]
#     min_e = np.array(energies)[valid][min_idx]
    
#     plt.axvline(min_r, color='red', linestyle='--', linewidth=2,
#                 label=f'Equilibrium: {min_r:.3f} Angstrom')
#     plt.axhline(min_e, color='red', linestyle=':', alpha=0.5)
#     plt.legend(fontsize=11)
#     plt.tight_layout()
#     plt.show()
    
#     print(f"\n=== Results ===")
#     print(f"Equilibrium C-C bond length: {min_r:.3f} Angstrom")
#     print(f"Minimum energy: {min_e:.6f} Ht")
#     print(f"Expected: 1.525 Angstrom (from NIST database)")
    
#     if abs(min_r - 1.525) < 0.05:
#         print("Your geometrcorrect!")
#     else:
#         print(" The minimum is still off. Check the hydrogen directions.")
# else:
#     print(f"Only {np.sum(valid)} valid points. Check the builder function.")

# h_values = [0.1, 0.05, 0.02, 0.01, 0.005]
# R_e = min_r
# for h in h_values:
#     R_minus = R_e - h
#     R_plus = R_e + h        

#     E_minus = calculate_energy_safe(build_ethane(R_minus))
#     E_0 = calculate_energy_safe(build_ethane(R_e))
#     E_plus = calculate_energy_safe(build_ethane(R_plus))

#     k = (E_plus - 2*E_0 + E_minus) / h**2

#fitting the local minimum region to quadratic function
bond_lengths = np.array(bond_lengths)
energies = np.array(energies)

mask = (bond_lengths >= 1.49) & (bond_lengths <= 1.55)

R_fit = bond_lengths[mask]
E_fit = energies[mask]

a, b, c = np.polyfit(R_fit - 1.525, E_fit, 2)

print("a =", a)
print("b =", b)
print("c =", c)

Re_fit = 1.525 - b/(2*a)

print("Fitted equilibrium bond length:", Re_fit, "Å")

k = 2*a

print("Force constant:", k, "Hartree/Å²")

k_SI = k * 4.3597447222071e-18 / (1e-10)**2
print("Force constant in SI units:", k_SI, "N/m")

u=12.001*12.001/(12.001*2) #reduced mass calculation
u_kg=u*1.66053906660e-27 #reduced mass in kg
print("Reduced mass:", u_kg, "kg")

v=math.sqrt(k_SI/u_kg)/(2*math.pi)
print("Vibrational frequency:", v, "Hz")
wavenumber=v/(2.99792458e10)
print("Vibrational frequency:", wavenumber, "cm⁻¹")
