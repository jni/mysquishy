from _squish import squish


def main():
    """Recompress array at sys.argv[1]."""
    import sys
    squish(sys.argv[1])
