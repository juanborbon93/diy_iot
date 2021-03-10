FROM continuumio/miniconda
RUN apt-get update
COPY conda-environment.yml ./
RUN conda env create -f conda-environment.yml
RUN echo "source activate diy_iot" > ~/.bashrc
ENV PATH /opt/conda/envs/diy_iot/bin:$PATH
EXPOSE 5000
COPY . ./
ENTRYPOINT ["uvicorn"]
CMD ["diy_iot:server --port 5000 --host 0.0.0.0"]