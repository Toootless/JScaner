#!/usr/bin/env python3
"""Check for libfreenect2 Python bindings"""

import sys

try:
    import freenect2
    print('✓ Python freenect2 bindings available')
    print('Available in freenect2:')
    for attr in sorted(dir(freenect2)):
        if not attr.startswith('_'):
            print(f'  - {attr}')
except ImportError:
    print('✗ Python freenect2 not installed')
    print('Will implement using ctypes with libfreenect2 DLL')
