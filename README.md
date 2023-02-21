# mysquishy

"I shall call him Squishy and he shall be mine and he shall be my Squishy."
— Dory

<img width="200" alt="mysquishy" src="https://user-images.githubusercontent.com/492549/220297427-736a3628-b1aa-429b-bf0d-f921c75b3172.png">

## Change the compression of a zarr array in-place.

This works by loading the chunk bytes, decoding them, recoding them, and saving
them. At the end, the .zarray file at the root is updated.

Note that this only works for single arrays: there should be a .zarray file at
the root. It is left as an exercise for the reader to figure out how to
recompress every array in a zarr group.

Contributions are very welcome.

## ⚠️  BAD SQUISHY! ⚠️

<img width="200" alt="Bad Squishy!" src="https://user-images.githubusercontent.com/492549/220299563-744d1958-2f2f-4763-a6e1-27c3bd7967f8.png">

This is currently just a proof of concept and it will leave your zarr arrays in
an inconsistent/broken state if it is interrupted! And/or there might be bugs.
It makes no effort to account for missing keys, for example. As above,
contributions are very welcome but in the meantime be careful! Make a tiny zarr
example similar to your data and check that it works fine there before
deploying it properly.

## Usage

From Python:

```python
nbytes_before, nbytes_after = mysquishy.squish('path/to/array.zarr')
```

From the command line:

```
mysquishy path/to/array.zarr
```
