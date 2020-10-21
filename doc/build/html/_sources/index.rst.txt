rpVisualiser's Documentation
============================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _RetroRules: https://retrorules.org/
.. _RetroPath2.0: https://github.com/Galaxy-SynBioCAD/RetroPath2
.. _rp2paths: https://github.com/Galaxy-SynBioCAD/rp2paths
.. _rpSBML: https://github.com/Galaxy-SynBioCAD/rpBase
.. _rpBase: https://github.com/Galaxy-SynBioCAD/rpBase
.. _rpCache: https://github.com/Galaxy-SynBioCAD/rpCache
.. _rpVisualiser: https://github.com/brsynth/rpVisualiser

Welcome rpVisualiser's documentation. This tool provides a docker wrapper for the rpVisualiser_ project.

.. code-block:: bash

   docker build -t brsynth/rpvisualiser-standalone:v2 .

You can run the docker using the following command:

.. code-block:: bash

   python run.py -input /path/to/file -input_format tar -output /path/to/file


API
###

.. currentmodule:: run

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:
