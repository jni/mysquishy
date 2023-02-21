# mysquishy

"I shall call him Squishy and he shall be mine and he shall be my Squishy."
— Dory

## Change the compression of a zarr array in-place.

This works by loading the chunk bytes, decoding them, recoding them, and saving
them. At the end, the .zarray file at the root is updated.

```python
mysquishy.squish('path/to/array.zarr')
```

```
mysquishy path/to/array.zarr
```
