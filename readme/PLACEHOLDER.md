## Placeholder

The Placeholder Map Type allows you to add a reference to an existing, non-nav-data-based map that you want to include in a Map List.
For example, the base RVM and MVA map can be added as Placeholders, which won't be processed, but will appear in the Map List.

Define a Placeholder in the following manner (be sure to include the blank `definition: {}` object):

```json
{
  "map_type": "PLACEHOLDER",
  "definition": {},
  "stars_definition": {
    "map_id": 1,
    "name": "Facility RVM",
    "short_name": "RVM",
    "brightness_category": "A"
  }
},
{
  "map_type": "PLACEHOLDER",
  "definition": {},
  "stars_definition": {
    "map_id": 2,
    "name": "Facility MVA",
    "short_name": "MVA",
    "brightness_category": "B"
  }
}
```

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
