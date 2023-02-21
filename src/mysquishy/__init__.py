from ._squish import squish


def main():
    """Recompress array at sys.argv[1]."""
    import sys
    result = squish(sys.argv[1])
    mb_before, mb_after = result / 1e6
    print(f'MB before: {mb_before}, MB after: {mb_after}, '
          f'Saved: {mb_before - mb_after}, '
          f'Compression ratio: {mb_before / mb_after}')
