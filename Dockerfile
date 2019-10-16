# Docker file that installs docker container for Selprom
#
# build with: "sudo docker build -t <image_name> ."

# Install basic image
FROM continuumio/miniconda3
#FROM continuumio/anaconda3:4.4.0

#### update
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install --yes wget \
 && conda update -n base -c defaults conda

#RUN pip install networkx cirpy pubchempy beautifulsoup4
RUN pip install cirpy pubchempy

# Install additional tools
RUN conda install -c \
    conda-forge flask-restful=0.3.6 \
    sbmlteam python-libsbml \
    anaconda networkx \
    anaconda beautifulsoup4 \
    conda-forge xorg-libxrender \
    anaconda lxml \
    anaconda ipython \
    conda-forge py2cytoscape \
    rdkit rdkit

WORKDIR /home

#RUN git clone https://github.com/pablocarb/rpviz.git
COPY rpviz.tar.xz .
COPY rpVisualiserServe.py .

RUN tar xf rpviz.tar.xz 

RUN wget https://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_prop.tsv -P rpviz/

# Start the server
ENTRYPOINT ["python"] 
CMD ["/home/rpVisualiserServe.py"]

# Open server port
EXPOSE 8998
