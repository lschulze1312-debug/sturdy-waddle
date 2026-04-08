"""
Build script for FPS Optimization Toolkit
Creates a standalone .exe file with administrator privileges
"""

import PyInstaller.__main__
import os
import shutil
import sys


MANIFEST = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>'''

def create_manifest():
    """Create admin manifest file"""
    with open('admin.manifest', 'w') as f:
        f.write(MANIFEST)
    return 'admin.manifest'


def clean_build_dirs():
    """Remove old build directories"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for d in dirs_to_remove:
        if os.path.exists(d):
            print(f"Removing {d}/...")
            shutil.rmtree(d, ignore_errors=True)
    
    # Remove .spec files
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            os.remove(f)


def build_exe():
    """Build the executable with PyInstaller"""
    print("Building FPS Optimization Toolkit...")
    print("This may take a few minutes...\n")
    
    # Create admin manifest
    manifest_path = create_manifest()
    
    args = [
        'fps_toolkit.py',
        '--name=FPS_Optimization_Toolkit',
        '--onefile',
        '--noconsole',
        '--clean',
        '--noconfirm',
        # Admin manifest
        f'--manifest={manifest_path}',
        # Hidden imports
        '--hidden-import=wmi',
        '--hidden-import=psutil',
        '--hidden-import=pywin32',
        '--hidden-import=win32com',
        '--hidden-import=win32com.client',
    ]
    
    PyInstaller.__main__.run(args)
    
    # Cleanup
    if os.path.exists(manifest_path):
        os.remove(manifest_path)
    
    print("\n" + "="*50)
    print("BUILD COMPLETE!")
    print("="*50)
    print(f"\nYour executable is located at:")
    print(f"  dist/FPS_Optimization_Toolkit.exe")
    print("\nThe app will request administrator privileges on start.")
    print("="*50)


def main():
    try:
        # Clean old builds
        clean_build_dirs()
        
        # Build
        build_exe()
        
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
