# Seed Collection for Fuzzing

This repo contains a lot of seeds for efficient fuzzing.

## Source
- https://github.com/strongcourage/fuzzing-corpus
- https://github.com/nimrodpar/Labeled-Elfs
- https://github.com/openpreserve/jpylyzer-test-files
- https://github.com/salmonx/seeds
- [Magma](https://github.com/HexHive/magma)
  - libtiff
  - libxml2
- Original tests in each project

## Subjects

This repo contains the following subjects.

### C

* libtiff
* libxml2
* zziplib

## Directory structures
* `original-seeds`: `exploit` and 50 initial seeds
* `new-seeds`: New seeds collected by us
* `original-seeds-log`: Dry run logs of `original-seeds` contains branch and DUG coverage
* `new-seeds-log`: Dry run logs of `new-seeds` contains branch and DUG coverage
* `meta.sbsv`: A map between `new-seeds` and original collection
* `seed-filtering.py`: A Python script to prune too large seeds
* `vulnfix.toml`: Input formats for each bugs (e.g. libtiff: tiff)

## Distance between Two Seeds

We provide a Python script to compute a distance between two seeds.

Run following command to compute:
```bash
python3 distance.py <dir1> <dir2> <subject>
```

For example, to compute `magma-seeds` and `original-seeds` for `libtiff`:
```bash
python3 distance.py magma-original-seeds original-seeds libtiff
```

The output will be:
```
magma-seeds/libtiff/tiffcp/97.tif: mean: 0.397789104606057, median: 0.2387838661904347, len: 408
magma-seeds/libtiff/tiffcp/2.tif: mean: 0.4216346194982484, median: 0.27363010715219094, len: 408
...
magma-seeds/libtiff/tiff_read_rgba_fuzzer/36.tif: mean: 0.4393050165856595, median: 0.3020515724366234, len: 408
```
Here, `magma-seeds/*/*.tif` represents the seed stored in `<dir1>`.
`mean` and `median` represents a mean and median between a seed in `<dir1>` and every seed in `<dir2>`.
`len` represents a number of seeds stored in `<dir2>`.

