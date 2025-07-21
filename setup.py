from setuptools import find_packages, setup

package_name = 'capacitacao'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fernanda',
    maintainer_email='fecorrea.barbosa@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'piloto = capacitacao.pilot_node:main',
            'sensor = capacitacao.sensor_node:main',
            'planner = capacitacao.planner_node:main',
        ],
    },
)
