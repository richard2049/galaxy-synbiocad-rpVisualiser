# Docker file that installs docker container for Selprom
#
# build with: "sudo docker build -t Dockerfile ."

# Install basic image
FROM continuumio/miniconda3
#FROM continuumio/anaconda3:4.4.0

#### update
RUN apt-get update && apt-get upgrade -y
RUN apt-get install --yes wget
RUN conda update -n base -c defaults conda

#RUN pip install networkx cirpy pubchempy beautifulsoup4
RUN pip install cirpy pubchempy

# Install additional tools
RUN conda install -c conda-forge flask-restful=0.3.6
RUN conda install -c sbmlteam python-libsbml
RUN conda install -c anaconda networkx
RUN conda install -c anaconda beautifulsoup4
RUN conda install -c conda-forge xorg-libxrender
RUN conda install -c anaconda lxml
RUN conda install -c anaconda ipython
RUN conda install -c conda-forge py2cytoscape 
RUN conda install -c rdkit rdkit

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
