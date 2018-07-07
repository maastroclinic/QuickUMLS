# QuickUMLS DOCKER IMAGE

### Build 

    docker build -t maastrodocker/quickumls --build-arg SPACYMODEL=<model> .
    
SPACYMODEL argument is optional, the default is "en"
    
### Run 

#### Volume bind (recommended)

    $ docker run --rm -v <local_quickumls_installation>:/data/quickumlsdb -p 9999:9999
     
     -it --entrypoint=/bin/bash maastrodocker/quickumls
        
#### Run data image (Windows)

Under Windows a volume bind will result in the following leveldb [error](https://github.com/google/leveldb/issues/281)

Solutions:
1. Use a DataVolume (not available in intellij)
2. Use the [Windows 10 linux subsystem](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. Add Quick UMLS installation files to the image


    $ docker run --rm -it --entrypoint /bin/bash maastrodocker/quickumlsdataimage
    
    $ docker run --rm -p9999:9999 -p9998:9998 -it maastrodocker/quickumlsdataimage:latest 


  
##### Add Quick UMLS installation files to the image
    
1. Clone this repository
2. relative to the Dockerfile create the directory ./data/quickumlsdb which contains your quickumls installation
3. Run
        
    
    $ docker build -t maastrodocker/quickumlsdataimage -f DockerfileDataImage .

###Develop
    
####IntelliJ IDEA

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