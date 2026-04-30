from setuptools import setup

setup(
    name='vehicle_control_gui',
    version='0.0.1',
    packages=['vehicle_control_gui'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/vehicle_control_gui']),
        ('share/vehicle_control_gui', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='your.email@example.com',
    description='Vehicle Control GUI',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'control_panel = vehicle_control_gui.control_panel:main',
        ],
    },
)
