from pathlib import Path


print(Path("random.nc").is_symlink())
print(Path("random.nc").readlink())
