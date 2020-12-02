FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

RUN pip install semver \
    && ( [ $(pip show filemagic|grep -c filemagic) -eq 0 ] || pip uninstall -y filemagic ) \
    && pip install python-magic \
    && pip install ftputil \
    && pip install ipython==5.3.0 \
    && pip install pyftpdlib==1.5.6 \
    && sudo apt-get install nano
# -----------------------------------------

RUN sudo apt-get update
RUN sudo apt-get install pigz wget
RUN pip install bz2file

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
