FROM fxdgear/ipython:3

RUN pip install lorem click snowballstemmer
ENV PYTHONBREAKPOINT=ipdb.set_trace
