# FacilityMapper

A VidMap draw tool for use with [vNAS](https://virtualnas.net). It is a spiritual successor to [VidMapper](https://github.com/misterrodg/VidMapper), but slightly more complex and aimed at managing maps and map sets.

While VidMapper is aimed at drawing ad hoc maps for smaller TRACONs, FacilityMapper is designed to build maps on the AIRAC cycle for entire ARTCCs. It is based on a `manifest.json` file, which is effectively a list of "recipes" for your facility maps, making it easy to issue updates on the cycle no matter what changes.

All maps are run through optimization prior to being written to file. Depending on the procedure, map type, and options, the way the source data defines the paths can cause several duplicate segments. Removing any segments that have already been drawn can save anywhere between a few and several thousand lines. For [Composite](./readme/COMPOSITE.md) maps, this optimization is run again after the two maps are combined.

## Testing Note

Prior to loading them into [vNAS Data Admin](https://data-admin.virtualnas.net/login), use [GeoJSON.io](https://geojson.io) or a similar tool to verify the output so that you can adjust the `manifest.json` as necessary. The way certain procedures are coded varies, so the end result might not match what you might expect. In these cases, a simple change to the `manifest.json` will solve the issue. For example, certain SIDs and STARs do not have a `core` section, and are made completely of runway and enroute transitions around a single point. In these cases, the procedure will not look correct unless `draw_runway_transitions` is set to `true`.

See [Manifest File Format](#manifest-file-format) for more details.

## Requirements

- Python3.8 or Later (Tested with Python 3.10.12)
- `cifparse` (v1-stable 1.0.1)

# Instructions for Use

- Copy this repository to your computer using:
  - `git clone https://github.com/misterrodg/FacilityMapper.git`; or
  - Download the ZIP under the Code drop down and unzip to a location of your choice.
- Install `cifparse` with `pip install cifparse==1.0.1`.

- Download the [FAA CIFP](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/) zip file. Copy the `FAACIFP18` file from the zip into the `./navdata` directory.
- Create a manifest file in the project root with the file name `manifest.json`.
  - See [Manifest File Format](#manifest-file-format) for more detail.
  - If you want to auto-generate more targeted manifests to work from, try the [Find](#find-function) function.
- Run the script (see [Drawing the Facility](#drawing-the-facility) for more detail).

## Manifest File Format

An example manifest is available in the project root. You can rename the example to `manifest.json` in the project root, or use it as a guide to creating your own. As projects become more complex, it might be helpful to have different manifests per facility. In this case, additional manifests can be placed in the `./manifests` directory and called via the `--manifest [file_name].json` switch.

More detail about Manifests can be found on the [Manifest](./readme/MANIFEST.md) page.

Examples:

- `example_manifest.json`: Basic example manifest file showing all of the fields and their defaults, available in the root folder.
- [EXAMPLES](./examples/EXAMPLES.md): More detail, and images of some of the various settings that are available.

### Find Function

A Find function is available to generate example manifests. For example, running the command `python3 find.py --airport KIAD --sid --star --iap --centerlines` will generate a manifest called `generated_kiad.json` in the `./manifests` directory containing all SIDs, STARs, IAPs, and Centerlines for `KIAD`. All defaults are included so that you can modify them if you desire, or delete lines if you are okay with the default.

For more detail, see [FIND](./readme/FIND.md).

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

`--purge` is available to quickly delete all files in the `./vidmaps` directory.

```bash
python3 main.py --purge
```

`--refresh` is available to refresh the database data (found at `./navdata/FAACIFP18.db`). Run this command any time you replace the `FAACIFP18` file. By default, the script will skip parsing the CIFP file and read from the database to save time.

```bash
python3 main.py --refresh
```

`--manifest` is available to specify different manifest files. By default, the script looks for a file named `manifest.json` in the project root, but additional manifests can be created with different file names in the `./manifests` directory, and built using `--manifest`.

```bash
python3 main.py --manifest manifest_name.json
```

`--list` is available to print a map list text file in the `./vidmaps` directory based on the [STARS Definition Objects](./readme/STARS_DEFINITION_OBJECT.md) in the manifest.

Note: The map list will only contain a list of those maps with STARS Definitions.

```bash
python3 main.py --list
```
