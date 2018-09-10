# QuickUMLS DOCKER IMAGE

UMLS concept extracting using QuickUMLS

### Create a QuickUMLS database (from an UMLS installation)

QuickUMLS needs a database which is not included in the docker image (because of the UMLS licensing model). 
To create a QuickUMLS datase execute the following steps.

1. [Get](https://www.nlm.nih.gov/research/umls/) and install UMLS. <umls_installation_path>
2. Create a destination path for quickumls database. <local_quickumls_installation_path>
3. Share the created paths with docker, using docker filesharing [see here](https://stackoverflow.com/questions/45122459/docker-mounts-denied-the-paths-are-not-shared-from-os-x-and-are-not-known
)
4. Run a docker container for the installation, where you mount the UMLS installation and quickumlsdb destination paths.

        $ docker run --rm -v "<umls_installation_path>:/data/umls" -v "<local_quickumls_installation_path>:/data/quickumlsdb" -it --entrypoint /bin/bash maastrodocker/quickumls-en 

5. Install the quickumls database, as decribed in the ["How To get the System Initialized (step 2)"](https://github.com/Georgetown-IR-Lab/QuickUMLS#how-to-get-the-system-initialized). Be carefull UMLS uses ISO 639-2 for languages). Example for the Dutch language.

        bash-4.4# python install.py /data/umls /data/quickumlsdb -E DUT

6. Exit the container

        bash-4.4# exit
        
    
## Run     

### Volume bind (recommended)

    $ docker run --rm -v <umls_installation_path>:/data/quickumlsdb -p 9999:9999 maastrodocker/quickumls-en
    
             
### Windows

Under Windows a volume bind will result in the following leveldb [error](https://github.com/google/leveldb/issues/281)

Solutions:
1. Use the [Windows 10 linux subsystem](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (recommended)
2. Add an existing QuickUMLS installation files to an image
3. Use a DataVolume (not supported by IntelliJ)
 
#### Add an existing QuickUMLS installation to an image
    
1. Create a docker file "Dockerfile" with the following content:

        FROM maastrodocker/quickumls-en:latest
        ADD quickumls-path /data/quickumlsdb

2. Edit the "Dockerfile":
    - The english image "maastrodocker/quickumls-en:latest" is used as default, change if needed.
    - Locate this Dockerfile **relative** to an existing docker installation (e.g. quickumls-path), and set the correct quickumls-path.
    
3. Build        
        
        $ docker build -t maastrodocker/quickumls-dataimage -f DockerfileDataImage .

4. The created docker image will contain your quickumls installation and is runnable from windows.               




## Usage 

Running the image as described in the RUN section will result in a listing TCP connection on the specified port.

Request format is the folling JSON format ("text" is used as a key).
    
    {"text": "This is a lung.\nDit is een long."}
    
    
Talk to the TCP application from:    
- Python [example](../tests/test_quickumls-service.py)
- NetCat


#### NetCat

Connect to the application.

    nc localhost 9999

The following request:    
 
    {"text": "This is a lung.\nDit is een long."}

Results in the following response (for Dutch QuickUMLS installation):

    [[{"start": 27, "end": 31, "ngram": "long", "term": "long", "cui": "C0024109", "similarity": 1.0, "semtypes": ["T023"], "preferred": 1}, {"start": 27, "end": 31, "ngram": "long", "term": "long", "cui": "C1278908", "similarity": 1.0, "semtypes": ["T023"], "preferred": 1}]]


## Development using Docker
    
### IntelliJ IDEA

1. Pull or build quickumls container
2. Install plugins:
    - Intellij Python Language
    - Intellij Docker Integration
3. Install [Python interpreter](https://www.jetbrains.com/help/idea/configuring-available-python-sdks.html)
4. Select docker and correct docker image
5. Edit run/debug configuration of your pythonscript
    - Set Python interpreter to the docker interpreter
    - Set working directory
    - Set docker container settings
        - Set volume bindings
        - Set PYTHONPATH /opt/pythonmodules:/opt/QuickUMLS
    
                -v C:/git/nlp/maastro/QuickUMLS:/data/quickumlsdb -e PYTHONPATH=/opt/pythonmodules
    
6. QuickUMLS parameters can be set as env variables (capitalized)


## Build your own image

Prebuild images can be found on [dockerhub](https://hub.docker.com/u/maastrodocker/), if you prefer to build your own image:

From the current folder

    docker build -t maastrodocker/quickumls-en --build-arg SPACYMODEL=<model> .
    
SPACYMODEL argument is optional, the default is "en".
It is recommended to include the spacy language model in the image tag. 