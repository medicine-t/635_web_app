
FROM continuumio/miniconda3

ARG env_name=env

COPY ./requirement.yml /etc/requirement.yml
COPY app /app

# conda create
ENV CONDA_DEFAULT_ENV ${env_name}
RUN conda env create --file /etc/requirement.yml

# install conda package
#SHELL ["conda", "run", "-n","${env_name}", "/bin/bash", "-c"]

RUN echo "conda activate ${env_name}" >> ~/.bashrc
ENV PATH /opt/conda/envs/${env_name}/bin:$PATH
