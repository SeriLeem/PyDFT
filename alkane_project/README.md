# Drew a PES(Potential Energy Surface) of Ethane using PyDFT in following order/attempts. 
--> can be found in alkane.py

1. obtained the coordinates of Ethane from Avogadro
2. successfully read the input Avogadro file from Python
3. attempted to plot the energy curve but failed because the energy calculation did not converge for some bond lengths that were too long for PyPDF to cover
4. tried the other way around - to reduce the bond length from 2.0 Angstrom to 1.0 Angstrom (both within the range of PYDFT convergence)
5. attempted to plot the energy curve but failed because Hydrogens were facing inwards
6. fixed the Hydrogens orientation (to face outward) and successfully drew the energy curve / obtained the equilibrium length of 1.5Angstrom which matches that of the database (https://cccbdb.nist.gov/calcbondcomp3x.asp?i=6&j=6&mi=58&bi=22)

[Potential Energy Surface for Ethane (STO-3G)](Potential Energy Surface for Ethane (STO-3G).png)

# Ethane C–C Bond PES and Vibrational Analysis 
--> can be found in vibfreq calc.py

## Overview

A self-directed DFT project exploring the relationship between a molecular
potential energy surface (PES), equilibrium bond length, force constant, and
vibrational frequency.

A one-dimensional slice of ethane's PES was explored by varying the C–C bond
length while keeping the remaining geometry fixed. A harmonic approximation
was then used to estimate the C–C stretching frequency near equilibrium.

## Method

- DFT with STO-3G basis set
- C–C bond-length scan with fixed C–H geometry
- Local quadratic PES fitting
- Force constant from PES curvature
- Harmonic approximation for vibrational frequency

## Results

| Quantity | Result |
|---|---:|
| Equilibrium C–C bond length | 1.517 Å |
| Force constant | 1.12 Hartree/Å² |
| Force constant | ~488 N/m |
| Estimated C–C stretching frequency | ~1175 cm⁻¹ |
