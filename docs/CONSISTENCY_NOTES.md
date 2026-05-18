# Documentation Consistency Notes

This document tracks key settings and values used consistently across all documentation.

## Standard Settings

### DEMto3D Configuration

**Model Dimensions:**
- Full map: 2000mm x 1500mm (or 1500mm x 2000mm if portrait)
- Per tile (Prusa XL): 330mm x 330mm

**Model Settings:**
- **Model size spacing**: 0.2mm (standard) or 0.3mm (faster)
- **Model height (base elevation)**: -2.18 meters
- **Vertical exaggeration**: 6.0x (recommended for Prusa XL)

**Output:**
- Format: STL Binary
- Base: Add 20mm in PrusaSlicer (not in DEMto3D)

### Print Settings (Prusa XL)

**Layer Settings:**
- Layer height: 0.2mm
- Bottom solid layers: 100 (for 20mm base at 0.2mm layers)
- Top solid layers: 3-5

**Infill:**
- Density: 10-15%
- Pattern: Gyroid or Cubic

**Material:**
- PLA recommended for large prints

### Terrain Characteristics

**DEM Data:**
- Resolution: 1m horizontal
- Elevation range: -2.18m to 1523.08m
- Total range: 1525.26m
- Geographic dimensions: 73.75km x 96.31km
- Aspect ratio: 0.766:1 (portrait)

**Print Results (with 6x exaggeration):**
- Terrain height: ~186mm
- Total height with base: ~206mm
- Fits in: 360mm bed height

## Cross-Reference Standards

All documentation should:
- Use relative paths for internal links
- Reference other docs using format: `[Link Text](FILENAME.md)`
- Be consistent with terminology
- Update this file when settings change

## Known Inconsistencies to Address

1. **Print dimensions**: Some docs reference 2m x 1.5m, but DEM is portrait (1.5m x 2m would match better)
   - **Resolution**: User preference - both work, just need to crop/scale
   - **Action**: Note in docs that DEM is portrait, user can choose orientation

2. **Vertical exaggeration**: Standardized to 6.0x across all docs
   - **Status**: ✅ Updated

3. **Base addition**: Standardized to add in PrusaSlicer, not DEMto3D
   - **Status**: ✅ Updated
