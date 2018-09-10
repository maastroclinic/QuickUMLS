# QuickUMLS DOCKER IMAGE


### Create a QuickUMLS database (from an UMLS installation)

QuickUMLS needs a database which is not included in the docker image (because of the UMLS licensing model). 
To create a QuickUMLS datase execute the following steps.

1. Install UMLS. <umls_installation_path>
2. Create a destination path for quickumls database. <local_quickumls_installation_path>
3. Share the created paths with docker, using docker filesharing [see here](https://stackoverflow.com/questions/45122459/docker-mounts-denied-the-paths-are-not-shared-from-os-x-and-are-not-known
)
4. Run a docker container for the installation, where you mount the umls installation and quickumlsdb destination paths.

        $ docker run --rm -v "<umls_installation_path>:/data/umls" -v "<local_quickumls_installation_path>:/data/quickumlsdb" -it --entrypoint /bin/bash maastrodocker/quickumls-en 

5. Install the quickumls database (e.g. for Dutch)

        bash-4.4# python install.py /data/umls /data/quickumlsdb -E DUT

6. Exit the container

        bash-4.4# exit
        
    
### Run 

Running the image as described below will result in a listing TCP connection on the specified port.

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


#### Volume bind (recommended)

    $ docker run --rm -v <umls_installation_path>:/data/quickumlsdb -p 9999:9999 maastrodocker/quickumls-en
    
             
#### Run data image (Windows)

Under Windows a volume bind will result in the following leveldb [error](https://github.com/google/leveldb/issues/281)

Solutions:
1. Use the [Windows 10 linux subsystem](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (recommended)
2. Add Quick UMLS installation files to the image
3. Use a DataVolume (not available in intellij)
 
##### Add an existing QuickUMLS installation to the image
    
1. Clone this repository.
2. Relative to the Dockerfile create the directory ./data/quickumlsdb 
3. Copy an existing QuickUMLS installation to the created directory (from step 2), directory structure:

      - QuickUMLS/docker/data/quickumlsdb/cui-semtypes.db
      - QuickUMLS/docker/data/quickumlsdb/umls-simstring.db

3. The English language is set as default, if you prefer another language, edit "DockerfileDataImage" to set the correct FROM image.
4. Run
        
        $ docker build -t maastrodocker/quickumls-dataimage -f DockerfileDataImage .

The file "DockerfileDataImage" will add a current QuickUMLS installation to a new image.                

### Build your own image

The following images are available on dockerhub.

- maastrodocker/quickumls-en
- maastrodocker/quickumls-nl

If you would prefer to build your own image:

From the current folder

    docker build -t maastrodocker/quickumls-en --build-arg SPACYMODEL=<model> .
    
SPACYMODEL argument is optional, the default is "en".
I included the language of the spacy model in the imagetag. 
Be carefull UMLS uses ISO 639-2 for languages (e.g. nl vs DUT).


### Develop
    
#### IntelliJ IDEA

Pull or build quickumls container
    
Install plugins:
- Intellij Python Language
- Intellij Docker Integration
    
https://www.jetbrains.com/help/idea/configuring-available-python-sdks.html
- Add python interpreter
- Select docker and correct docker image

In run/debug configuration of your pythonscript
- Set Python interpreter to the docker interpreter
- Set working directory
- Set docker container settings
    - Set volume bindings
    - Set PYTHONPATH /opt/pythonmodules:/opt/QuickUMLS
    
    
    -v C:/git/nlp/maastro/QuickUMLS:/data/quickumlsdb -e PYTHONPATH=/opt/pythonmodules
    
    
    
- `quickumls_fp` is the directory where the QuickUMLS data files are installed. Docker default = /data/quickumlsdb
- `overlapping_criteria` (optional, default: "score") is the criteria used to deal with overlapping concepts; choose "score" if the matching score of the concepts should be consider first, "length" if the longest should be considered first instead.
- `threshold` (optional, default: 0.7) is the minimum similarity value between strings.
- `similarity_name` (optional, default: "jaccard") is the name of similarity to use. Choose between "dice", "jaccard", "cosine", or "overlap".
- `window` (optional, default: 5) is the maximum number of tokens to consider for matching.
- `accepted_semtypes` (optional, default: see `constants.py`) is the set of UMLS semantic types concepts should belong to. Semantic types are identified by the letter "T" followed by three numbers (e.g., "T131", which identifies the type *"Hazardous or Poisonous Substance"*). See [here](https://metamap.nlm.nih.gov/Docs/SemanticTypes_2013AA.txt) for the full list.

env variables are capitalized