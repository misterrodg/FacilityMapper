# FacilityMapper

A VidMap draw tool for use with [vNAS](https://virtualnas.net). It is a spiritual successor to [VidMapper](https://github.com/misterrodg/VidMapper), but slightly more complex and aimed at managing maps and map sets.

While [VidMapper](https://github.com/misterrodg/VidMapper) is aimed at drawing ad hoc maps for smaller TRACONs, FacilityMapper is designed to build maps on the AIRAC cycle for entire ARTCCs.

## Testing Note

Prior to loading them into [vNAS Data Admin](https://data-admin.virtualnas.net/login), use [GeoJSON.io](https://geojson.io) or a similar tool to verify the output. The way certain procedures are coded varies, so the end result might not match what you might expect. In these cases, a simple change to the `manifest.json` will solve the issue. See [Manifest File Format](#manifest-file-format) for more details.

## Requirements

- Python3.8 or Later (Tested with Python 3.10.12)
- `cifparse`

# Instructions for Use

- Install `cifparse` with:

```bash
pip install cifparse
```

- Download the [FAA CIFP](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/) zip file. Copy the `FAACIFP18` file from the zip into the `./navdata` directory.
- Create a manifest file.

## Manifest File Format

Examples:

- `example_manifest.json`: Basic example manifest file showing all of the fields and their defaults, available in the root folder.
- `example_zdc_manifest.json`: Completed manifest showing the options used for a "production" build, available in the root folder.

### Manifest

The `manifest.json` file has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `maps`<span style="color:#FF0000">\*</span>: An array of [Map Objects](#map-objects).

### Map Objects

The map object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `map_type`<span style="color:#FF0000">\*</span>: A string representing the map type. Supported map types are: `"SID"` and `"STAR"`.
- `definition`<span style="color:#FF0000">\*</span>: A [Definition Object](#definition-objects).

### Definition Objects

The definition object has fields that depend on the map type being defined.

#### SID

The SID object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `airport_id`<span style="color:#FF0000">\*</span>: A string representing the ICAO identifier for the airport.
- `procedure_id`<span style="color:#FF0000">\*</span>: A string representing the computer code of the procedure, in the format `"AAAAA#"` (`"JCOBY#"`), where the `#` is the literal `#` symbol.
- `line_type` <span style="color:#FF9900">Not Yet Implemented</span>: A string representing the line type that should be drawn. Supported line types are: `"solid"` (default), `"longDashed"`, `"shortDashed"`, `"longDashShortDash"`, and `"none"`.
- `draw_symbols`: A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the CIFP, and clips the line around the point.
- `symbol_scale`: A float value representing the scale of the symbols. Defaults to `1.0` (approximately 1.0 NM tall).
- `draw_names`: A boolean value that tells the script to draw the name of the fix near the fix location.
- `x_offset`: A float value representing the lateral text offset in nautical miles (positive for East and negative for West). Defaults to `0`.
- `y_offset`: A float value representing the vertical text offset in nautical miles (positive for North and negative for South). Defaults to `0`.
- `text_scale`: A float value representing the scale of the text. Defaults to `1.0` (approximately 1.0 NM tall).
- `draw_enroute_transitions`: A boolean value that tells the script to draw the enroute transitions. Defaults to `true`.
- `draw_runway_transitions`: A boolean value that tells the script to draw the runway transitions. Defaults to `false`. NOTE: Many SID runway transitions have performance/altitude-based points. These are not currently supported, so the line draws might be odd in this segment for now.
- `file_name`: A string representing the filename that the map will be saved to (`"003_JCOBY"`). Defaults to `{airportId}_{mapType}_{procedureId}`

#### STAR

The STAR object is defined using the same properties as [SID](#sid)

#### Label

The Label object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `lines`<span style="color:#FF0000">\*</span>: An array of `line` objects.
- `file_name`<span style="color:#FF0000">\*</span>: A string representing the filename that the map will be saved to.

##### Line

The Line object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `line`<span style="color:#FF0000">\*</span>: A text line of supported characters.
- `lat`<span style="color:#FF0000">\*</span>: A float value representing the latitude.
- `lon`<span style="color:#FF0000">\*</span>: A float value representing the longitude.
- `text_scale`: A float value representing the scale of the text. Defaults to `1.0` (approximately 1.0 NM tall).

NOTE: The "origin" of the text is at the bottom left corner.

#### Supported Characters

The following characters are currently supported:

- Numeric Characters: `0` through `9`.
- Simple Alpha Characters: `A` through `Z`.
- Simple Control Characters: ` ` and `.`.

## Drawing the Facility

Run the following command:

```
python3 main.py
```

The resulting file(s) will be in `./vidmaps`

### Additional Command Line Arguments

`--nodraw` is available to skip the draw step. This is useful to run with the other command line options if you wish to run those steps only.

```bash
python3 main.py --nodraw
```

`--purge` is available to quickly clean up the vidmap directory.

```bash
python3 main.py --purge
```

`--refresh` is available to refresh the database data. By default, the script will skip parsing the CIFP to save time if it has already parsed it into a database (found at `./navdata/FAACIFP18.db`). Run this command any time you replace the `FAACIFP18` file.

```bash
python3 main.py --refresh
```
