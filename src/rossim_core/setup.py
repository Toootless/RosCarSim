from setuptools import setup

package_name = 'rossim_core'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Core vehicle simulation engine for RosSim',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vehicle_model = rossim_core.vehicle_model:main',
            'control_manager = rossim_core.control_manager:main',
            'adas_manager = rossim_core.adas_manager:main',
        ],
    },
)
