## Find

The Find function is available to generate targeted manifests that can be used as a basis for creating your own. All manifests created with Find will be placed in the `./manifests` directory with the prefix `generated_`. If you choose to use a generated file, be sure to change the name to something else so that it is not overwritten by a subsequent run of the function.

### Command Line Arguments

#### Airport Commands

`--airport` is available to select an airport to generate a manifest for it, with the following manifest type options:

| Switch          | Map Type                        |
| --------------- | ------------------------------- |
| `--sid`         | [SID](./SIDSTAR.md#sid)         |
| `--star`        | [STAR](./SIDSTAR.md#star)       |
| `--iap`         | [IAP](./IAP.md)                 |
| `--centerlines` | [CENTERLINES](./CENTERLINES.md) |

An additional `--select` switch is available when using `--centerlines`, which tries to find an appropriate IAP for the runway, and adds it to the manifest if found.

```bash
python3 main.py --airport {airport_id} {--optional switches}
```

#### Other Commands

`--controlled` is available to generate a manifest for [CONTROLLED](./CONTROLLED.md) map types. It will select all controlled airspace that has a point within the defining box between the `min_lat, min_lon` (bottom left corner) and `max_lat, max_lon` (top right corner). Since controlled airspace maps are individual, and several can exist within a specific area, an optional `--composite` switch is available to generate an additional composite map type.

```bash
python3 main.py --controlled {min_lat,min_lon,max_lat,max_lon} {--optional composite switch}
```

`--restrictive` is available to generate a manifest for [RESTRICTIVE](./RESTRICTIVE.md) map types. It will select all restrictive airspace that has a point within the defining box between the `min_lat, min_lon` (bottom left corner) and `max_lat, max_lon` (top right corner). Since restrictive airspace maps are individual, and several can exist within a specific area, an optional `--composite` switch is available to generate an additional composite map type.

```bash
python3 main.py --restrictive {min_lat,min_lon,max_lat,max_lon} {--optional composite switch}
```

`--runways` is available to generate a manifest for a [RUNWAYS](./RUNWAYS.md) map type. It will select all airports by defining a box between the `min_lat, min_lon` (bottom left corner) and `max_lat, max_lon` (top right corner).

```bash
python3 main.py --runways {min_lat,min_lon,max_lat,max_lon}
```
