"""Package the manual and non-secret deployment metadata for offline handover."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
files = sorted((root / 'documentation/manual-build').glob('*'))
files += [root / path for path in (
    'documentation/Process-Stepper-Component.md',
    'documentation/PowerApps-Screen-Plan.md',
    'documentation/STATUS.md',
    'provisioning/environment.json',
    'provisioning/deployment-result.json',
    'tools/Build-ManualGuide.py',
    'tools/Test-ManualGuide.py',
)]
destination = root / 'documentation/NominationApp-Manual-Build.zip'
with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
    for path in files:
        if path.is_file():
            archive.write(path, path.relative_to(root).as_posix())
    archive.writestr('START-HERE.txt',
        'Open documentation/manual-build/README.md.\n'
        'This package contains manual instructions, not an importable or tested Canvas app.\n'
        'Keep the folder structure when extracting so links resolve.\n')
with ZipFile(destination) as archive:
    assert archive.testzip() is None
    print(f'Created and verified {destination.name}: {len(archive.namelist())} entries, {destination.stat().st_size:,} bytes')
