from setuptools import setup

setup(
    name='vehicle_viz',
    version='0.0.1',
    packages=['vehicle_viz'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/vehicle_viz']),
        ('share/vehicle_viz', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='your.email@example.com',
    description='Vehicle Visualization GUI',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vehicle_display = vehicle_viz.vehicle_display:main',
        ],
    },
)
