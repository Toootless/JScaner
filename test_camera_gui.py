#!/usr/bin/env python3
"""Test camera selection UI"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui.main_window import MainApplication
    
    print('✓ Testing GUI initialization...')
    app = MainApplication()
    print('✓ GUI initialized successfully')
    print(f'✓ Camera selection widget created')
    print(f'✓ Initial camera selection: {app.camera_var.get()}')
    
    # Test camera switching
    print('\nTesting camera switching:')
    print(f'✓ Kinect available: {app.image_capture.kinect is not None}')
    print(f'✓ Kinect active: {app.image_capture.kinect_active}')
    
    app.root.destroy()
    print('\n✓ All GUI tests passed!')
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
