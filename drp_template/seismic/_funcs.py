import numpy as np

from drp_template.default_params import print_style

__all__ = [
    'calculate_wavelength',
    'calculate_frequency',
    'calculate_velocity'
]

def calculate_wavelength(velocity, frequency):
    """
    Calculate wavelength based on velocity and frequency.
    
    The wavelength is calculated using the fundamental wave equation:
    λ = v / f
    
    Where:
    - λ (lambda) is the wavelength
    - v is the wave velocity
    - f is the frequency
    
    Args:
        velocity (float or numpy.ndarray): Wave velocity in m/s.
        frequency (float or numpy.ndarray): Frequency in Hz.
        
    Returns:
        float or numpy.ndarray: Wavelength in meters.
        
    Raises:
        ValueError: If frequency is zero or negative.
        ValueError: If velocity is negative.
        
    Examples:
        Calculate wavelength for P-wave:
        ```python
        velocity = 3000  # m/s
        frequency = 100  # Hz
        wavelength = calculate_wavelength(velocity, frequency)
        # Result: 30.0 meters
        ```
        
        Calculate wavelength for multiple frequencies:
        ```python
        velocity = 2500  # m/s
        frequencies = np.array([50, 100, 200])  # Hz
        wavelengths = calculate_wavelength(velocity, frequencies)
        # Result: [50.0, 25.0, 12.5] meters
        ```
    """
    # Convert inputs to numpy arrays for consistent handling
    velocity = np.asarray(velocity)
    frequency = np.asarray(frequency)
    
    # Validate inputs
    if np.any(frequency <= 0):
        raise ValueError("Frequency must be positive and non-zero.")
    
    if np.any(velocity < 0):
        raise ValueError("Velocity must be non-negative.")
    
    # Calculate wavelength using the wave equation λ = v / f
    wavelength = velocity / frequency
    
    print_style(f'Wavelength calculation completed:\n'
                f'Velocity: {velocity} m/s\n'
                f'Frequency: {frequency} Hz\n'
                f'Wavelength: {wavelength} m')
    
    return wavelength


def calculate_frequency(velocity, wavelength):
    """
    Calculate frequency based on velocity and wavelength.
    
    The frequency is calculated using the fundamental wave equation:
    f = v / λ
    
    Where:
    - f is the frequency
    - v is the wave velocity
    - λ (lambda) is the wavelength
    
    Args:
        velocity (float or numpy.ndarray): Wave velocity in m/s.
        wavelength (float or numpy.ndarray): Wavelength in meters.
        
    Returns:
        float or numpy.ndarray: Frequency in Hz.
        
    Raises:
        ValueError: If wavelength is zero or negative.
        ValueError: If velocity is negative.
        
    Examples:
        Calculate frequency for P-wave:
        ```python
        velocity = 3000  # m/s
        wavelength = 30  # m
        frequency = calculate_frequency(velocity, wavelength)
        # Result: 100.0 Hz
        ```
        
        Calculate frequency for multiple wavelengths:
        ```python
        velocity = 2500  # m/s
        wavelengths = np.array([50, 25, 12.5])  # m
        frequencies = calculate_frequency(velocity, wavelengths)
        # Result: [50.0, 100.0, 200.0] Hz
        ```
    """
    # Convert inputs to numpy arrays for consistent handling
    velocity = np.asarray(velocity)
    wavelength = np.asarray(wavelength)
    
    # Validate inputs
    if np.any(wavelength <= 0):
        raise ValueError("Wavelength must be positive and non-zero.")
    
    if np.any(velocity < 0):
        raise ValueError("Velocity must be non-negative.")
    
    # Calculate frequency using the wave equation f = v / λ
    frequency = velocity / wavelength
    
    print_style(f'Frequency calculation completed:\n'
                f'Velocity: {velocity} m/s\n'
                f'Wavelength: {wavelength} m\n'
                f'Frequency: {frequency} Hz')
    
    return frequency


def calculate_velocity(frequency, wavelength):
    """
    Calculate velocity based on frequency and wavelength.
    
    The velocity is calculated using the fundamental wave equation:
    v = f × λ
    
    Where:
    - v is the wave velocity
    - f is the frequency
    - λ (lambda) is the wavelength
    
    Args:
        frequency (float or numpy.ndarray): Frequency in Hz.
        wavelength (float or numpy.ndarray): Wavelength in meters.
        
    Returns:
        float or numpy.ndarray: Wave velocity in m/s.
        
    Raises:
        ValueError: If frequency is zero or negative.
        ValueError: If wavelength is zero or negative.
        
    Examples:
        Calculate velocity for seismic wave:
        ```python
        frequency = 100  # Hz
        wavelength = 30  # m
        velocity = calculate_velocity(frequency, wavelength)
        # Result: 3000.0 m/s
        ```
        
        Calculate velocity for multiple frequencies:
        ```python
        frequencies = np.array([50, 100, 200])  # Hz
        wavelength = 25  # m
        velocities = calculate_velocity(frequencies, wavelength)
        # Result: [1250.0, 2500.0, 5000.0] m/s
        ```
    """
    # Convert inputs to numpy arrays for consistent handling
    frequency = np.asarray(frequency)
    wavelength = np.asarray(wavelength)
    
    # Validate inputs
    if np.any(frequency <= 0):
        raise ValueError("Frequency must be positive and non-zero.")
    
    if np.any(wavelength <= 0):
        raise ValueError("Wavelength must be positive and non-zero.")
    
    # Calculate velocity using the wave equation v = f × λ
    velocity = frequency * wavelength
    
    print_style(f'Velocity calculation completed:\n'
                f'Frequency: {frequency} Hz\n'
                f'Wavelength: {wavelength} m\n'
                f'Velocity: {velocity} m/s')
    
    return velocity
