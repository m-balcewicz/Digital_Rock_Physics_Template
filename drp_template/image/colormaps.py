"""Unified phase colormap helper utilities.

This module centralizes analysis of labeled (integer) volumetric data and
construction of consistent discrete color resources (ListedColormap + BoundaryNorm
+ mapping dict) so that 2D orthogonal views and 3D volume rendering share the
exact same phase -> color assignments.

Primary entry points
--------------------
get_phase_color_resources(data, cmap_name='batlow', brightness=1.0)
    Analyze `data` (3D np.ndarray or any ndarray) and build color resources.

Returned dictionary keys
------------------------
'is_integer' : bool
'unique_ids' : np.ndarray of sorted unique phase IDs (integers)
'n_phases'   : int number of phases
'cmap'       : ListedColormap (discrete) or base continuous colormap
'norm'       : BoundaryNorm for discrete mapping, else None
'mapping'    : {phase_id: (r,g,b)} color tuples in 0..1 range
'boundaries' : array of boundaries used for norm (if discrete)

Notes
-----
- Integer detection: all values equal to their rounded form.
- For non-integer or too many unique IDs (>256), falls back to continuous colormap.
- Colors sampled evenly from perceptually uniform cmcrameri colormap when available.
- brightness parameter scales RGB (clamped) for optional global lightening/darkening.
- Stable ordering: ascending unique phase IDs.

Future extensions could incorporate user supplied phase ordering or explicit
palette overrides.
"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
try:  # Prefer cmcrameri
    from cmcrameri import cm as cmc
except Exception:  # pragma: no cover - fallback when cmcrameri unavailable
    cmc = None

__all__ = [
    'analyze_phase_data',
    'build_phase_colormap',
    'get_phase_color_resources'
]

def analyze_phase_data(data: np.ndarray) -> dict:
    """Analyze data to determine if discrete integer phases are present.

    Returns dict with keys: is_integer, unique_ids (np.ndarray), n_phases.
    """
    if not isinstance(data, np.ndarray):
        data = np.asarray(data)
    # Integer check: all values equal to their rounded representation
    try:
        is_integer = np.all(np.equal(data, np.round(data)))
    except Exception:
        is_integer = False
    unique_ids = np.unique(data.astype(int)) if is_integer else np.array([])
    return {
        'is_integer': bool(is_integer),
        'unique_ids': unique_ids,
        'n_phases': int(unique_ids.size) if is_integer else 0
    }

def _resolve_base_colormap(name: str):
    """Resolve a base colormap name trying cmcrameri first then matplotlib.
    Accepts names like 'batlow' or 'cm.batlow'. Falls back to viridis.
    """
    if name is None:
        return plt.cm.get_cmap('viridis')
    name = str(name)
    try:
        if name.startswith('cm.'):
            raw = name.split('.', 1)[1]
        else:
            raw = name
        if cmc is not None and hasattr(cmc, raw):
            return getattr(cmc, raw)
        return plt.cm.get_cmap(raw)
    except Exception:
        return plt.cm.get_cmap('viridis')

def build_phase_colormap(unique_ids: np.ndarray, cmap_name: str = 'batlow', brightness: float = 1.0):
    """Build discrete ListedColormap, BoundaryNorm, and mapping dict for given unique phase IDs.

    Parameters
    ----------
    unique_ids : array-like of ints (sorted unique phase IDs)
    cmap_name  : base perceptually uniform colormap name
    brightness : scale factor applied to RGB (clamped to [0,1])

    Returns
    -------
    cmap : ListedColormap
    norm : BoundaryNorm
    mapping : dict {phase_id: (r,g,b)}
    boundaries : np.ndarray boundaries used for norm
    """
    if unique_ids.size == 0:
        # Single fallback color
        base = _resolve_base_colormap(cmap_name)
        rgba = base(0.5)
        rgb = tuple(np.clip(np.array(rgba[:3]) * brightness, 0, 1))
        listed = ListedColormap([rgb])
        boundaries = np.array([-0.5, 0.5])
        norm = BoundaryNorm(boundaries, ncolors=1, clip=True)
        return listed, norm, {0: rgb}, boundaries

    base = _resolve_base_colormap(cmap_name)
    n = unique_ids.size
    if n == 1:
        t_values = [0.5]
    else:
        t_values = [i / (n - 1) for i in range(n)]
    colors = []
    mapping = {}
    for pid, t in zip(unique_ids, t_values):
        rgba = base(t)
        rgb = tuple(np.clip(np.array(rgba[:3]) * brightness, 0, 1))
        colors.append(rgb)
        mapping[int(pid)] = rgb
    listed = ListedColormap(colors)
    # Boundary construction: midpoints between successive integer IDs with +/-0.5 on ends
    # Assumes phase IDs are integers (enforced upstream)
    boundaries = np.concatenate(([unique_ids[0] - 0.5], (unique_ids[:-1] + unique_ids[1:]) / 2.0, [unique_ids[-1] + 0.5]))
    norm = BoundaryNorm(boundaries, ncolors=n, clip=True)
    return listed, norm, mapping, boundaries

def get_phase_color_resources(data: np.ndarray, cmap_name: str = 'batlow', brightness: float = 1.0) -> dict:
    """Return unified color resources for a labeled volume.

    For integer-labeled data with <=256 unique phases returns discrete resources.
    Otherwise returns continuous base colormap and norm=None while still supplying
    a mapping for discovered integer IDs (or empty mapping).
    """
    analysis = analyze_phase_data(data)
    is_integer = analysis['is_integer']
    unique_ids = analysis['unique_ids']

    # Guard for excessive number of classes: fallback to continuous
    if not is_integer or unique_ids.size == 0 or unique_ids.size > 256:
        base = _resolve_base_colormap(cmap_name)
        # Sample mapping anyway for present unique ids if integer
        mapping = {}
        if is_integer and unique_ids.size > 0:
            n = unique_ids.size
            t_values = [0.5] if n == 1 else [i / (n - 1) for i in range(n)]
            for pid, t in zip(unique_ids, t_values):
                rgb = tuple(np.clip(np.array(base(t)[:3]) * brightness, 0, 1))
                mapping[int(pid)] = rgb
        return {
            'is_integer': is_integer,
            'unique_ids': unique_ids,
            'n_phases': unique_ids.size if is_integer else 0,
            'cmap': base,
            'norm': None,
            'mapping': mapping,
            'boundaries': None
        }

    # Discrete case
    listed, norm, mapping, boundaries = build_phase_colormap(unique_ids, cmap_name=cmap_name, brightness=brightness)
    return {
        'is_integer': True,
        'unique_ids': unique_ids,
        'n_phases': unique_ids.size,
        'cmap': listed,
        'norm': norm,
        'mapping': mapping,
        'boundaries': boundaries
    }
