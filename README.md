# FacilityMapper

A VidMap draw tool for use with [vNAS](https://virtualnas.net). It is a spiritual successor to [VidMapper](https://github.com/misterrodg/VidMapper), but slightly more complex and aimed at managing maps and map sets.

While VidMapper is aimed at drawing ad hoc maps for smaller TRACONs, FacilityMapper is designed to build maps on the AIRAC cycle for entire ARTCCs. It is based on a `manifest.json` file, which is effectively a list of "recipes" for your facility maps, making it easy to issue updates on the cycle no matter what changes.

All maps are run through optimization prior to being written to file. Depending on the procedure, map type, and options, the way the source data defines the paths can cause several duplicate segments. Removing any segments that have already been drawn can save anywhere between a few and several thousand lines. For [Composite](#composite) maps, this optimization is run again after the two maps are combined.

## Testing Note

Prior to loading them into [vNAS Data Admin](https://data-admin.virtualnas.net/login), use [GeoJSON.io](https://geojson.io) or a similar tool to verify the output so that you can adjust the `manifest.json` as necessary. The way certain procedures are coded varies, so the end result might not match what you might expect. In these cases, a simple change to the `manifest.json` will solve the issue. For example, certain SIDs and STARs do not have a `core` section, and are made completely of runway and enroute transitions around a single point. In these cases, the procedure will not look correct unless `draw_runway_transitions` is set to `true`.

See [Manifest File Format](#manifest-file-format) for more details.

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
- Run the script (see [Drawing the Facility](#drawing-the-facility) for more detail).

## Manifest File Format

Examples:

- `example_manifest.json`: Basic example manifest file showing all of the fields and their defaults, available in the root folder.
- `example_zdc_manifest.json`: Completed manifest showing the options used for a "production" build, available in the root folder.

More detail, and images of the various settings is available in [EXAMPLES](./examples/EXAMPLES.md).

### Manifest

The `manifest.json` file has the following properties:

| Property | Required | Type    | Default | Description                             |
| -------- | -------- | ------- | ------- | --------------------------------------- |
| `maps`   | \*       | `array` |         | An array of [Map Objects](#map-objects) |

### Map Objects

The map object has the following properties:

| Property     | Required | Type     | Default | Description                                                                                                          |
| ------------ | -------- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------- |
| `map_type`   | \*       | `string` |         | A string representing the map type. Supported map types are: `"IAP"`,`"SID"`, `"STAR"`, `"LABEL"` and `"COMPOSITE"`. |
| `definition` | \*       | `object` |         | A [Definition Object](#definition-objects).                                                                          |

### Definition Objects

The definition object has fields that depend on the map type being defined.

#### SID

The SID object has the following properties:

| Property                   | Required | Type     | Default                               | Description                                                                                                                                                                                                                                |
| -------------------------- | -------- | -------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `airport_id`               | \*       | `string` |                                       | A string representing the ICAO identifier for the airport.                                                                                                                                                                                 |
| `procedure_id`             | \*       | `string` |                                       | A string representing the computer code of the procedure, in the format `"AAA#"` or `"AAAAA#"` (`"JCOBY#"`), where the `#` is the literal `#` symbol.                                                                                      |
| `line_type`                |          | `string` | `"solid"`                             | A string representing the line type that should be drawn. Supported line types are: `"solid"`, `"longDashed"`, `"shortDashed"`, `"longDashShortDash"`, `"arrows"`, and `"none"`.                                                           |
| `draw_symbols`             |          | `bool`   | `false`                               | A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the CIFP, and clips the line around the point.                                                                             |
| `symbol_scale`             |          | `float`  | `1.0`                                 | A float value representing the scale of the symbols.                                                                                                                                                                                       |
| `draw_altitudes`           |          | `bool`   | `false`                               | A boolean value that tells the script to draw the speed restriction (if present) for the fix near the fix location.                                                                                                                        |
| `draw_speeds`              |          | `bool`   | `false`                               | A boolean value that tells the script to draw the altitude restriction(s) (if present) for the fix near the fix location.                                                                                                                  |
| `draw_names`               |          | `bool`   | `false`                               | A boolean value that tells the script to draw the name of the fix near the fix location.                                                                                                                                                   |
| `x_offset`                 |          | `float`  | `0`                                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).                                                                                                                            |
| `y_offset`                 |          | `float`  | `0`                                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South).                                                                                                                         |
| `text_scale`               |          | `float`  | `1.0`                                 | A float value representing the scale of the text.                                                                                                                                                                                          |
| `line_buffer`              |          | `float`  | `1.5` \* `text_scale`                 | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.                                                                                                                                 |
| `draw_enroute_transitions` |          | `bool`   | `true`                                | A boolean value that tells the script to draw the enroute transitions.                                                                                                                                                                     |
| `draw_runway_transitions`  |          | `bool`   | `false`                               | A boolean value that tells the script to draw the runway transitions. NOTE: Many SID runway transitions have performance/altitude-based points. These are not currently supported, so the line draws might be odd in this segment for now. |
| `file_name`                |          | `string` | `{airportId}_{mapType}_{procedureId}` | A string representing the filename that the map will be saved to (`"003_JCOBY"`).                                                                                                                                                          |

#### STAR

The STAR object is defined using the same properties as [SID](#sid).

#### IAP

The interpretation of the paths is still relatively limited. As such, more advanced draws like those on RTF legs are not yet supported.

The IAP object has the following properties:

| Property         | Required | Type     | Default                               | Description                                                                                                                                                          |
| ---------------- | -------- | -------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `airport_id`     | \*       | `string` |                                       | A string representing the ICAO identifier for the airport.                                                                                                           |
| `procedure_id`   | \*       | `string` |                                       | A string representing the computer code of the procedure. These aren't always straightforward. See [ICAO IAP Codes](#icao-iap-codes) for more detail.                |
| `line_type`      |          | `string` | `"solid"`                             | A string representing the line type that should be drawn. Supported line types are: `"solid"`, `"longDashed"`, `"shortDashed"`, `"longDashShortDash"`, and `"none"`. |
| `draw_symbols`   |          | `bool`   | `false`                               | A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the CIFP, and clips the line around the point.       |
| `symbol_scale`   |          | `float`  | `1.0`                                 | A float value representing the scale of the symbols.                                                                                                                 |
| `draw_altitudes` |          | `bool`   | `false`                               | A boolean value that tells the script to draw the speed restriction (if present) for the fix near the fix location.                                                  |
| `draw_speeds`    |          | `bool`   | `false`                               | A boolean value that tells the script to draw the altitude restriction(s) (if present) for the fix near the fix location.                                            |
| `draw_names`     |          | `bool`   | `false`                               | A boolean value that tells the script to draw the name of the fix near the fix location.                                                                             |
| `x_offset`       |          | `float`  | `0`                                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).                                                      |
| `y_offset`       |          | `float`  | `0`                                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South).                                                   |
| `text_scale`     |          | `float`  | `1.0`                                 | A float value representing the scale of the text.                                                                                                                    |
| `line_buffer`    |          | `float`  | `1.5` \* `text_scale`                 | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.                                                           |
| `transition_ids` |          | `array`  |                                       | An array of strings representing the names of the transitions to include.                                                                                            |
| `draw_missed`    |          | `bool`   | `false`                               | A boolean value that tells the script to draw the missed approach. (Generally functional but not recommended for use.)                                               |
| `file_name`      |          | `string` | `{airportId}_{mapType}_{procedureId}` | A string representing the filename that the map will be saved to (`"003_KOKV_VDMA"`).                                                                                |

##### ICAO IAP Codes

| Prefix | Type    | Example      |
| ------ | ------- | ------------ |
| B      | LOC/BC  | `B30L`       |
| D      | VOR/DME | `D25`        |
| F      | FMS     | _Deprecated_ |
| G      | IGS     | _Deprecated_ |
| H      | RNP     | `H21-Y`      |
| I      | ILS     | `I01R`       |
| J      | GNSS    | _Deprecated_ |
| L      | LOC     | `L17`        |
| M      | MLS     | _Deprecated_ |
| N      | NDB     | `N34`        |
| P      | GPS     | `P04`        |
| Q      | NDB/DME | `Q06R`       |
| R      | RNAV    | `R14`        |
| S      | VORTAC  | `S13`        |
| T      | TACAN   | _Deprecated_ |
| U      | SDF     | _Deprecated_ |
| V      | VOR     | `V22`        |
| W      | MLS-A   | _Deprecated_ |
| X      | LDA     | `X19-Y`      |
| Y      | MLS-B/C | _Deprecated_ |

...and because the CIFP is an FAA product, these additional oddities that seem to be specific to procedures not tied to a specific runway:

| Prefix | Type    | Example |
| ------ | ------- | ------- |
| GPS    | GPS     | `GPS-A` |
| LBC    | LOC/BC  | `LBC-A` |
| LDA    | LDA     | `LDA-A` |
| LOC    | LOC     | `LOC-A` |
| NDB    | NDB     | `NDB-A` |
| RNV    | RNAV    | `RNV-A` |
| VDM    | VOR/DME | `VDM-A` |
| VOR    | VOR     | `VOR-A` |

#### Label

The Label object has the following properties:

| Property    | Required | Type     | Default | Description                                                       |
| ----------- | -------- | -------- | ------- | ----------------------------------------------------------------- |
| `lines`     | \*       | `array`  |         | An array of [Label Line](#label-line) objects.                    |
| `file_name` | \*       | `string` |         | A string representing the filename that the map will be saved to. |

##### Label Line

The Label Line object has the following properties:

| Property     | Required | Type     | Default | Description                                                   |
| ------------ | -------- | -------- | ------- | ------------------------------------------------------------- |
| `line`       | \*       | `string` |         | A text line of [supported characters](#supported-characters). |
| `lat`        | \*       | `float`  |         | A float value representing the latitude.                      |
| `lon`        | \*       | `float`  |         | A float value representing the longitude.                     |
| `text_scale` |          | `float`  | `1.0`   | A float value representing the scale of the text.             |

NOTE: The "origin" of the text is at the bottom left corner.

#### Composite

A Composite Map is a map made up of other maps. This is useful in cases where you would like to show several SIDs on a single map. As best practice, all Composites should be listed at the end of the manifest to ensure that the relevant maps are generated before trying to combine them.

The Composite object has the following properties:

| Property           | Required | Type     | Default | Description                                                                             |
| ------------------ | -------- | -------- | ------- | --------------------------------------------------------------------------------------- |
| `file_names`       | \*       | `string` |         | A string representing the filenames to combine into a single map.                       |
| `file_name`        | \*       | `string` |         | A string representing the filename that the map will be saved to.                       |
| `delete_originals` |          | `bool`   | `false` | A boolean value that tells the script to delete the original maps after combining them. |

#### Supported Characters

The following characters are currently supported:

| Type    | Supported                                                                                               |
| ------- | ------------------------------------------------------------------------------------------------------- |
| Numeric | `0`,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`                                                                 |
| Alpha   | `A`,`B`,`C`,`D`,`E`,`F`,`G`,`H`,`I`,`J`,`K`,`L`,`M`,`N`,`O`,`P`,`Q`,`R`,`S`,`T`,`U`,`V`,`W`,`X`,`Y`,`Z` |
| Other   | `+`,`-`,`.`,`⎵` (space)                                                                                 |

What the characters look like is shown in [EXAMPLES](./examples/EXAMPLES.md#label-supported-characters).

## Drawing the Facility

Run the following command:

```
python3 main.py
```

The resulting file(s) will be in `./vidmaps`.

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
