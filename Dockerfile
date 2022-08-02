FROM kbase/sdkpython:3.8.10
MAINTAINER KBase Developer

RUN apt-get update
RUN apt-get install pigz wget nano

RUN pip install semver \
    && ( [ $(pip show filemagic|grep -c filemagic) -eq 0 ] || pip uninstall -y filemagic ) \
    && pip install python-magic \
    && pip install ftputil \
    && pip install ipython \
    && pip install pyftpdlib==1.5.6 \
    && pip install google-api-python-client \
    && pip install bz2file 


COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
