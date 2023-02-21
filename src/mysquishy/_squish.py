import numpy as np
from dask.distributed import Client, as_completed
from numcodecs import get_codec
from numcodecs.abc import Codec
from numcodecs.compat import ndarray_copy
from ome_zarr.io import parse_url
import zarr
from zarr.util import json_loads, json_dumps
from zarr.indexing import BasicIndexer
from tqdm import tqdm
import toolz as tz


def get_chunk_keys(path):
    array = zarr.open(path, mode='r')
    region = slice(None)
    indexer = BasicIndexer(region, array)
    chunk_coords = (idx.chunk_coords for idx in indexer)
    keys = (array._chunk_key(cc) for cc in chunk_coords)
    return keys


class NullCompressor(Codec):
    codec_id = None

    def encode(self, buf):
        return buf

    def decode(self, buf, out=None):
        return ndarray_copy(buf, out)

    def get_config(self):
        return {'id': None}


@tz.curry
def recompress(store, key, source_codec=NullCompressor(),
        dest_codec=zarr.storage.default_compressor):
    in_bytes = store[key]
    out_bytes = dest_codec.encode(source_codec.decode(in_bytes))
    store[key] = out_bytes
    return len(in_bytes), len(out_bytes)


def squish(path):
    """Compress the chunks in a zarr array.

    `path` should be a zarr array, not a dataset or group or any such thing.
    """
    chunk_keys = list(get_chunk_keys(path))
    store = parse_url(path, mode='r+').store
    meta = json_loads(store['.zarray'])
    output_meta = meta.copy()
    compressor = meta.get('compressor', None)
    if compressor is not None:
        source_codec = get_codec(compressor)
    else:
        source_codec = NullCompressor()
    # TODO: configure dest compressor
    dest_codec = zarr.storage.default_compressor
    output_meta['compressor'] = dest_codec.get_config()
    total = np.zeros(2)
    with Client(processes=False) as client:
        futures = client.map(
                recompress(
                        store, source_codec=source_codec, dest_codec=dest_codec
                        ),
                chunk_keys
                )
        for future, result in tqdm(
                as_completed(futures, with_results=True), total=len(chunk_keys)
                ):
            total += result
    store['.zarray'] = json_dumps(output_meta)
    return total
