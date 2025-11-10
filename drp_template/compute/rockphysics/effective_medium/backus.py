"""
Backus Averaging for VTI Media

Model Type: Analytical
Assumptions: 
    - Finely layered medium (layer thickness << wavelength)
    - Long wavelength limit (λ >> layer thickness)
    - Layers are isotropic
    - Perfect bonding between layers
    - Vertical axis of symmetry
Applicable to:
    - Dry: Yes
    - Saturated: Yes (with effective layer properties)
    - Frequency dependent: No (quasi-static limit)
Input Requirements:
    - Layer elastic properties (Vp, Vs, density)
    - Layer thicknesses
Output:
    - Effective elastic constants for VTI medium (A, C, D, F, M, B)
    - Effective velocities at specified propagation angles
    - Thomsen anisotropy parameters (via thomsen_params)
References:
    - Backus, G. E. (1962): Long-wave elastic anisotropy produced by 
      horizontal layering, J. Geophys. Res., 67(11), 4427-4440
    - Thomsen, L. (1986): Weak elastic anisotropy, Geophysics, 51(10), 1954-1966
    - Mavko, G., Mukerji, T., & Dvorkin, J. (2009). The Rock Physics Handbook,
      2nd edition, Page 212
"""

import numpy as np
from drp_template.default_params.styling import print_style
from drp_template.compute.conversions import Pa2GPa

__all__ = ['backus_average', 'thomsen_params', 'vti_velocity_vs_angle']


def backus_average(Vp_layers, Vs_layers, rho_layers, d_layers, angle_deg=0, verbose=False):
    """
    Calculate Backus averaging for an arbitrary number of layers.
    
    Computes effective elastic constants and velocities for a finely layered VTI 
    (Vertically Transversely Isotropic) medium with N layers using Backus (1962) 
    averaging theory.
    
    Parameters
    ----------
    Vp_layers : array-like
        P-wave velocities for each layer (m/s). Length N.
    Vs_layers : array-like
        S-wave velocities for each layer (m/s). Length N.
    rho_layers : array-like
        Densities for each layer (kg/m³). Length N.
    d_layers : array-like
        Thicknesses for each layer (m). Length N.
    angle_deg : float, optional
        Propagation angle in degrees (0 = vertical, 90 = horizontal). Default is 0.
    verbose : bool, optional
        If True, print detailed results to console. Default is False.
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'M' : Horizontal shear modulus (Pa)
        - 'A' : Horizontal P-wave modulus (Pa)
        - 'D' : Vertical shear modulus (Pa)
        - 'C' : Vertical P-wave modulus (Pa)
        - 'B' : Backus B modulus (Pa)
        - 'F' : Anisotropic coupling parameter (Pa)
        - 'Vp' : P-wave velocity at specified angle (m/s)
        - 'Vsv' : SV-wave velocity at specified angle (m/s)
        - 'Vsh' : SH-wave velocity at specified angle (m/s)
        - 'rho_eq' : Average density (kg/m³)
        - 'Vp_0' : Vertical P-wave velocity at 0° (m/s)
        - 'Vp_90' : Horizontal P-wave velocity at 90° (m/s)
        - 'Vsv_0' : Vertical SV-wave velocity at 0° (m/s)
        - 'Vsh_90' : Horizontal SH-wave velocity at 90° (m/s)
    
    Raises
    ------
    ValueError
        If arrays have different lengths, any parameter is non-positive,
        or if Vp <= Vs for any layer.
    
    Notes
    -----
    The effective elastic constants for a VTI medium are computed using the
    Backus (1962) averaging formulas. The model assumes:
    
    - Layer thickness << seismic wavelength (long wavelength limit)
    - Layers are perfectly bonded
    - Each layer is isotropic
    - Vertical axis of symmetry
    
    The five independent elastic constants (A, C, D, F, M) fully characterize
    the VTI medium. An additional parameter B is also computed.
    
    The Backus averaging formulas use:
    - Arithmetic (Voigt) averaging for some parameters
    - Harmonic (Reuss) averaging for others
    - Mixed averaging for anisotropic coupling terms
    
    Velocity calculations use the Christoffel equation for VTI media.
    
    Examples
    --------
    >>> # Two-layer medium: Calcite + Shale
    >>> Vp = [5200, 2900]
    >>> Vs = [2700, 1400]
    >>> rho = [2450, 2340]
    >>> d = [0.75, 0.5]
    >>> results = backus_average(Vp, Vs, rho, d, angle_deg=90, verbose=True)
    >>> print(f"Effective Vp at 90°: {results['Vp']:.2f} m/s")
    >>> print(f"P-wave modulus A: {results['A']/1e9:.2f} GPa")
    
    >>> # Five alternating layers: Sandstone - Shale - Sandstone - Shale - Sandstone
    >>> Vp_5 = [4500, 2900, 4500, 2900, 4500]
    >>> Vs_5 = [2800, 1400, 2800, 1400, 2800]
    >>> rho_5 = [2500, 2340, 2500, 2340, 2500]
    >>> d_5 = [0.8, 0.4, 0.8, 0.4, 0.8]
    >>> results_5 = backus_average(Vp_5, Vs_5, rho_5, d_5, angle_deg=0)
    >>> 
    >>> # Calculate Thomsen parameters from Backus results
    >>> thomsen = thomsen_params(
    ...     A=results['A'], C=results['C'], F=results['F'],
    ...     D=results['D'], M=results['M']
    ... )
    >>> print(f"ε (epsilon) = {thomsen['epsilon']:.4f}")
    >>> print(f"γ (gamma)   = {thomsen['gamma']:.4f}")
    >>> print(f"δ (delta)   = {thomsen['delta']:.4f}")
    
    >>> # Single layer (trivial case)
    >>> results_1 = backus_average([4500], [2800], [2500], [1.0])
    >>> # Returns isotropic properties: A=C, M=D
    
    References
    ----------
    - Backus, G. E. (1962): Long-wave elastic anisotropy produced by 
      horizontal layering, J. Geophys. Res., 67(11), 4427-4440
    - Thomsen, L. (1986): Weak elastic anisotropy, Geophysics, 51(10), 1954-1966
    - Mavko, G., Mukerji, T., & Dvorkin, J. (2009): The Rock Physics Handbook,
      2nd edition, Page 212
    """
    # Convert to numpy arrays
    Vp_layers = np.asarray(Vp_layers, dtype=float)
    Vs_layers = np.asarray(Vs_layers, dtype=float)
    rho_layers = np.asarray(rho_layers, dtype=float)
    d_layers = np.asarray(d_layers, dtype=float)
    
    # Validation: Check array lengths
    n_layers = len(Vp_layers)
    if not (len(Vs_layers) == len(rho_layers) == len(d_layers) == n_layers):
        raise ValueError(
            f"All input arrays must have the same length. Got: "
            f"Vp({len(Vp_layers)}), Vs({len(Vs_layers)}), "
            f"rho({len(rho_layers)}), d({len(d_layers)})"
        )
    
    if n_layers < 1:
        raise ValueError("At least one layer is required.")
    
    # Validation: Check positive values
    if np.any(Vp_layers <= 0):
        raise ValueError(f"All Vp values must be positive. Got: {Vp_layers}")
    if np.any(Vs_layers <= 0):
        raise ValueError(f"All Vs values must be positive. Got: {Vs_layers}")
    if np.any(rho_layers <= 0):
        raise ValueError(f"All rho values must be positive. Got: {rho_layers}")
    if np.any(d_layers <= 0):
        raise ValueError(f"All thickness values must be positive. Got: {d_layers}")
    
    # Validation: Check Vp > Vs for all layers
    if np.any(Vp_layers <= Vs_layers):
        invalid_idx = np.where(Vp_layers <= Vs_layers)[0]
        raise ValueError(
            f"Vp must be greater than Vs for all layers. "
            f"Violation at layer(s): {invalid_idx.tolist()}"
        )
    
    # Calculate layer fractions
    total_thickness = np.sum(d_layers)
    f_layers = d_layers / total_thickness
    
    # Average density - weighted by thickness
    rho_eq = np.sum(f_layers * rho_layers)
    
    # Calculate shear moduli for each layer
    M_layers = rho_layers * Vs_layers**2
    
    # Calculate auxiliary parameters for each layer
    # Lambda (Lamé parameter): λ = ρVp² - 2μ = ρVp² - 2ρVs²
    lambda_layers = rho_layers * Vp_layers**2 - 2 * M_layers
    
    # Poisson-like ratio: (1 - 2Vs²/Vp²)
    poisson_term = 1 - 2 * Vs_layers**2 / Vp_layers**2
    
    # Backus averaging formulas (Backus 1962, Mavko et al. 2009)
    
    # M: Horizontal shear modulus - arithmetic (Voigt) average
    M_ = np.sum(f_layers * M_layers)
    
    # D: Vertical shear modulus - harmonic (Reuss) average
    D_ = 1.0 / np.sum(f_layers / M_layers)
    
    # C: Vertical P-wave modulus - harmonic average
    C_ = 1.0 / np.sum(f_layers / (rho_layers * Vp_layers**2))
    
    # Intermediate sums for A, B, F
    sum_poisson = np.sum(f_layers * poisson_term)
    sum_inv_rhoVp2 = np.sum(f_layers / (rho_layers * Vp_layers**2))
    
    # A: Horizontal P-wave modulus
    A_ = np.sum(f_layers * 4 * rho_layers * Vs_layers**2 * (1 - Vs_layers**2 / Vp_layers**2)) + \
         (sum_poisson**2) / sum_inv_rhoVp2
    
    # B: Backus B modulus
    B_ = np.sum(f_layers * 2 * rho_layers * Vs_layers**2 * (1 - 2 * Vs_layers**2 / Vp_layers**2)) + \
         (sum_poisson**2) / sum_inv_rhoVp2
    
    # F: Anisotropic coupling parameter
    F_ = sum_poisson / sum_inv_rhoVp2
    
    # Calculate velocities at specified angle using Christoffel equation
    i = np.radians(angle_deg)
    
    # Intermediate parameter
    m_inc = ((((A_ - D_) * (np.sin(i))**2) - ((C_ - D_) * (np.cos(i))**2))**2) + \
            (((F_ + D_)**2) * ((np.sin(2 * i))**2))
    
    # Phase velocities at angle i
    Vp_ = np.sqrt((A_ * (np.sin(i))**2) + (C_ * (np.cos(i))**2) + D_ + (np.sqrt(m_inc))) / np.sqrt(2 * rho_eq)
    Vsv_ = np.sqrt((A_ * (np.sin(i))**2) + (C_ * (np.cos(i))**2) + D_ - (np.sqrt(m_inc))) / np.sqrt(2 * rho_eq)
    Vsh_ = np.sqrt(((M_ * (np.sin(i)**2)) + (D_ * (np.cos(i)**2))) / rho_eq)
    
    # Reference velocities at principal directions
    Vp_0 = np.sqrt(C_ / rho_eq)
    Vp_90 = np.sqrt(A_ / rho_eq)
    Vsv_0 = np.sqrt(D_ / rho_eq)
    Vsh_90 = np.sqrt(M_ / rho_eq)
    
    # Print results if verbose
    if verbose:
        header = f"BACKUS AVERAGING RESULTS FOR {n_layers} LAYERS AT {angle_deg}°"
        print_style(header, style='section')
        
        layer_info = f"\nLayer configuration ({n_layers} layers):\n"
        for i in range(n_layers):
            layer_info += f"  Layer {i+1}: Vp={Vp_layers[i]:.0f} m/s, Vs={Vs_layers[i]:.0f} m/s, "
            layer_info += f"ρ={rho_layers[i]:.0f} kg/m³, d={d_layers[i]:.2f} m ({f_layers[i]*100:.1f}%)\n"
        print(layer_info)
        
        elastic_constants = (
            "Effective Elastic Constants (GPa):\n"
            f"A = C11 = C22 = {Pa2GPa(A_):.2f} (Horizontal P-wave modulus)\n"
            f"C = C33 = {Pa2GPa(C_):.2f} (Vertical P-wave modulus)\n"
            f"F = C13 = C23 = {Pa2GPa(F_):.2f} (Anisotropic coupling)\n"
            f"D = C44 = C55 = {Pa2GPa(D_):.2f} (Vertical shear modulus)\n"
            f"M = C66 = {Pa2GPa(M_):.2f} (Horizontal shear modulus)\n"
            f"B = {Pa2GPa(B_):.2f} (Backus B modulus)"
        )
        print(elastic_constants)
        
        # VTI Stiffness Tensor (6x6 Voigt notation)
        C11 = Pa2GPa(A_)
        C33 = Pa2GPa(C_)
        C13 = Pa2GPa(F_)
        C44 = Pa2GPa(D_)
        C66 = Pa2GPa(M_)
        C12 = Pa2GPa(A_ - 2*M_)  # For VTI: C12 = C11 - 2*C66
        
        tensor_display = (
            "\nVTI Stiffness Tensor Cij (GPa):\n"
            f"       ┌                                             ┐\n"
            f"       │ {C11:6.2f}  {C12:6.2f}  {C13:6.2f}   0.00   0.00   0.00 │\n"
            f"       │ {C12:6.2f}  {C11:6.2f}  {C13:6.2f}   0.00   0.00   0.00 │\n"
            f"  Cij= │ {C13:6.2f}  {C13:6.2f}  {C33:6.2f}   0.00   0.00   0.00 │\n"
            f"       │   0.00   0.00   0.00  {C44:6.2f}   0.00   0.00  │\n"
            f"       │   0.00   0.00   0.00   0.00  {C44:6.2f}   0.00  │\n"
            f"       │   0.00   0.00   0.00   0.00   0.00  {C66:6.2f}  │\n"
            f"       └                                             ┘\n"
            f"       (Symmetry axis: vertical x₃-direction)"
        )
        print(tensor_display)
        
        velocities = (
            f"\nVelocities at {angle_deg}° (m/s):\n"
            f"Vp  = {Vp_:.2f}\n"
            f"Vsv = {Vsv_:.2f}\n"
            f"Vsh = {Vsh_:.2f}"
        )
        print(velocities)
        
        reference_velocities = (
            "\nReference velocities (m/s):\n"
            f"Vp(0°)  = {Vp_0:.2f}   Vp(90°)  = {Vp_90:.2f}   P-wave anisotropy = {((Vp_90-Vp_0)/Vp_0)*100:.3f}%\n"
            f"Vs(0°)  = {Vsv_0:.2f}   Vsh(90°) = {Vsh_90:.2f}   S-wave anisotropy = {((Vsh_90 - Vsv_0)/Vsv_0)*100:.3f}%\n"
            f"\nAverage density = {rho_eq:.2f} kg/m³"
        )
        print(reference_velocities)
        print("=" * 50)
    
    return {
        'M': M_,
        'A': A_,
        'D': D_,
        'C': C_,
        'B': B_,
        'F': F_,
        'Vp': Vp_,
        'Vsv': Vsv_,
        'Vsh': Vsh_,
        'rho_eq': rho_eq,
        'Vp_0': Vp_0,
        'Vp_90': Vp_90,
        'Vsv_0': Vsv_0,
        'Vsh_90': Vsh_90
    }


def thomsen_params(A, C, F, D, M):
    """
    Calculate Thomsen parameters for weak elastic anisotropy in VTI media.
    
    Computes the three Thomsen (1986) dimensionless anisotropy parameters
    (epsilon, gamma, delta) from the five elastic constants of a VTI medium.
    
    Parameters
    ----------
    A : float
        Horizontal P-wave modulus (Pa).
    C : float
        Vertical P-wave modulus (Pa).
    F : float
        Anisotropic coupling parameter (Pa).
    D : float
        Vertical shear modulus (Pa).
    M : float
        Horizontal shear modulus (Pa).
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'epsilon' : P-wave anisotropy parameter (dimensionless)
        - 'gamma' : S-wave anisotropy parameter (dimensionless)
        - 'delta' : Anellipticity parameter (dimensionless)
    
    Notes
    -----
    The Thomsen parameters are defined as:
    
    - epsilon: P-wave velocity anisotropy, ε = (A - C) / (2C)
      Fractional difference between horizontal and vertical P-wave velocities
      
    - gamma: S-wave velocity anisotropy, γ = (M - D) / (2D)
      Fractional difference between horizontal and vertical S-wave velocities
      
    - delta: Anellipticity parameter, δ = ((F+D)² - (C-D)²) / (2C(C-D))
      Controls near-vertical P-wave velocity behavior
    
    These parameters are most meaningful for weak anisotropy (|ε|, |γ|, |δ| << 1),
    but can be computed for arbitrary anisotropy strength.
    
    References
    ----------
    Thomsen, L. (1986): Weak elastic anisotropy, Geophysics, 51(10), 1954-1966
    
    Examples
    --------
    >>> # From Backus averaging results
    >>> results = backus_average(5200, 2700, 2450, 0.75, 2900, 1400, 2340, 0.5)
    >>> thomsen = thomsen_params(
    ...     A=results['A'], C=results['C'], F=results['F'],
    ...     D=results['D'], M=results['M']
    ... )
    >>> print(f"ε = {thomsen['epsilon']:.4f}")
    >>> print(f"γ = {thomsen['gamma']:.4f}")
    >>> print(f"δ = {thomsen['delta']:.4f}")
    
    >>> # Interpretation
    >>> if abs(thomsen['epsilon']) < 0.1:
    ...     print("Weak P-wave anisotropy")
    """
    epsilon = (A - C) / (2 * C)
    gamma = (M - D) / (2 * D)
    delta = ((F + D)**2 - (C - D)**2) / (2 * C * (C - D))
    
    return {
        'epsilon': epsilon,
        'gamma': gamma,
        'delta': delta
    }


def vti_velocity_vs_angle(A, C, D, F, M, rho_eq, angles=None):
    """
    Calculate phase velocities for VTI media as a function of propagation angle.
    
    Generic VTI velocity calculation using the Christoffel equation for 
    Vertically Transversely Isotropic media. Works with ANY source of VTI 
    elastic constants.
    
    Parameters
    ----------
    A : float
        Horizontal P-wave modulus C11 = C22 (Pa).
    C : float
        Vertical P-wave modulus C33 (Pa).
    D : float
        Vertical shear modulus C44 = C55 (Pa).
    F : float
        Anisotropic coupling parameter C13 (Pa).
    M : float
        Horizontal shear modulus C66 (Pa).
    rho_eq : float
        Effective density (kg/m³).
    angles : array-like, optional
        Propagation angles in degrees from vertical (0° = vertical, 90° = horizontal).
        Default is np.linspace(0, 90, 91).
    
    Returns
    -------
    tuple of (angles, Vp, Vsv, Vsh)
        angles : ndarray
            Propagation angles in degrees.
        Vp : ndarray
            Quasi-P-wave phase velocities (m/s).
        Vsv : ndarray
            Quasi-SV-wave phase velocities (m/s).
        Vsh : ndarray
            SH-wave phase velocities (m/s).
    
    Notes
    -----
    This function implements the exact phase velocity solution for VTI media
    using the Christoffel equation. The three wave modes are:
    
    - **qP (Vp)**: Quasi-P-wave (predominantly compressional)
    - **qSV (Vsv)**: Quasi-SV-wave (shear in vertical plane)
    - **SH (Vsh)**: Pure SH-wave (shear perpendicular to vertical plane)
    
    The velocities are calculated from the eigenvalues of the Christoffel matrix
    for VTI symmetry.
    
    **Can be used with:**
    
    1. Backus averaging results
    2. Measured VTI elastic constants
    3. Thomsen parameters converted to stiffnesses
    4. Any other VTI model (Hudson cracks, etc.)
    
    **VTI Elastic Constants:**
    
    The five independent elastic constants for VTI media are related to the
    stiffness tensor components:
    
    - A = C11 = C22 (horizontal P-wave)
    - C = C33 (vertical P-wave)
    - D = C44 = C55 (vertical shear)
    - F = C13 (coupling, note: F = C13, not C13 + 2C44)
    - M = C66 (horizontal shear)
    
    References
    ----------
    - Thomsen, L. (1986): Weak elastic anisotropy, Geophysics, 51(10), 1954-1966
    - Tsvankin, I. (2012): Seismic Signatures and Analysis of Reflection Data 
      in Anisotropic Media, 3rd edition
    - Mavko, G., Mukerji, T., & Dvorkin, J. (2009): The Rock Physics Handbook
    
    Examples
    --------
    >>> # From Backus averaging
    >>> backus_results = backus_average(5200, 2700, 2450, 0.75, 2900, 1400, 2340, 0.5)
    >>> angles, Vp, Vsv, Vsh = vti_velocity_vs_angle(
    ...     A=backus_results['A'],
    ...     C=backus_results['C'],
    ...     D=backus_results['D'],
    ...     F=backus_results['F'],
    ...     M=backus_results['M'],
    ...     rho_eq=backus_results['rho_eq']
    ... )
    
    >>> # Custom angle range
    >>> angles_custom = np.array([0, 15, 30, 45, 60, 75, 90])
    >>> angles, Vp, Vsv, Vsh = vti_velocity_vs_angle(
    ...     A=45e9, C=34e9, D=8e9, F=17e9, M=12e9, rho_eq=2400,
    ...     angles=angles_custom
    ... )
    
    >>> # Check velocity at vertical and horizontal
    >>> print(f"Vp at 0° (vertical): {Vp[0]:.2f} m/s")
    >>> print(f"Vp at 90° (horizontal): {Vp[-1]:.2f} m/s")
    """
    # Set default angle range if not provided
    if angles is None:
        angles = np.linspace(0, 90, 91)  # 0 to 90 degrees in 1-degree increments
    
    # Ensure angles is a numpy array
    angles = np.asarray(angles)
    
    # Initialize velocity arrays
    Vp = np.zeros_like(angles, dtype=float)
    Vsv = np.zeros_like(angles, dtype=float)
    Vsh = np.zeros_like(angles, dtype=float)
    
    # Calculate velocities for each angle using Christoffel equation for VTI
    for i, angle_deg in enumerate(angles):
        # Convert angle to radians
        theta = np.radians(angle_deg)
        
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        sin_theta_sq = sin_theta**2
        cos_theta_sq = cos_theta**2
        
        # Christoffel equation intermediate parameter
        # This comes from solving the eigenvalue problem for VTI media
        m_inc = (((A - D) * sin_theta_sq) - ((C - D) * cos_theta_sq))**2 + \
                ((F + D)**2) * (np.sin(2 * theta))**2
        
        # Phase velocities from Christoffel equation eigenvalues
        # qP-wave (fast quasi-longitudinal)
        Vp[i] = np.sqrt((A * sin_theta_sq + C * cos_theta_sq + D + np.sqrt(m_inc)) / (2 * rho_eq))
        
        # qSV-wave (slow quasi-shear in vertical plane)
        Vsv[i] = np.sqrt((A * sin_theta_sq + C * cos_theta_sq + D - np.sqrt(m_inc)) / (2 * rho_eq))
        
        # SH-wave (pure shear perpendicular to vertical plane)
        Vsh[i] = np.sqrt((M * sin_theta_sq + D * cos_theta_sq) / rho_eq)
    
    return angles, Vp, Vsv, Vsh

