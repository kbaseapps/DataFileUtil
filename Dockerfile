FROM kbase/sdkpython:3.8.10
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

RUN apt update

RUN apt install -y nano pigz wget libmagic-dev

RUN pip uninstall -y filemagic

# bz2file hasn't been updated in 10 years
RUN pip install \
    requests==2.31.0 \
    requests_toolbelt==1.0.0 \
    semver==3.0.2 \
    python-magic==0.4.27 \
    ftputil==5.1.0 \
    ipython==5.3.0 \
    bz2file==0.98 \
    pyftpdlib==1.5.6

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
