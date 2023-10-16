# [[file:test.org::+BEGIN_SRC dockerfile :tangle Dockerfile][No heading:3]]
FROM python:3.7
RUN pip install pygments
RUN pip install jupyter
RUN pip install jupyterlab
RUN pip install jupyter_contrib_nbextensions


RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable codefolding/main
# No heading:3 ends here
