from setuptools import setup

setup(
    name='vehicle_options_gui',
    version='0.0.1',
    packages=['vehicle_options_gui'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/vehicle_options_gui']),
        ('share/vehicle_options_gui', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='your.email@example.com',
    description='Vehicle Options GUI',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'options_panel = vehicle_options_gui.options_panel:main',
        ],
    },
)
