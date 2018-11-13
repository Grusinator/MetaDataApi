# MetaDataApi
tags: Quantified Self, Biohacking, RDF, OWL, Oauth, graphql, JSONSchema, OpenMHealth
## Description
This project aims to gather relevant data from a lot of services an analyse on top. You might call it HumanIntelligence 
It is based on the semantic web idea, so json data can just be loaded in from Api endpoints, that you create.  
First a datamodel from that json file is created, and thereafter instances of objects and attributes are added.
You can also upload RDF schemas defined in OWL, and thereafter upload your rdf data to it. The goal is to standardize the incoming data by comparing with other models, and mapping it onto a more covering model within the field. My initial approach has been to take the OpenMHealth data model which is defined in JSONSchema, i have converted it to OWL. 

the platform can connect to different oauth2 rest apis, by adding the endpoints, and authorizing first. different parameters can be added as well as url-encoded parameters 

if the parameter value has to be something specific, it can be added by replacing the value with a tag insted. currently the tags that are supported is: 
* StartDateTime
* EndDateTime
* AuthToken

each value will then be substituted with the relevant variable converted to the desired format. 

AuthToken is just as is, no formatting.
The DateTime parameters can be formatted as the following:
* UTCSEC
* Y-M-d

More should be added, so that any api datetime format is supported.

Example:
https://brainscan.io/api?key={AuthToken:}&startdate={StartDateTime:UTCSEC}&eyesclosed=true  

I have made a small client in python to request some of the data from the server, but it is not complete, have a look at:
https://github.com/Grusinator/meta-data-client



## TODO:
- [ ] implement logging and better error handling
- [ ] compare metaobjects using word2vec or similar
- [ ] make a data encoder that can model a full human (requires more data)
- [ ] Add image attribute type
- [ ] make a front-end 
- [ ] write documentation
- [ ] make tests of all services
- [ ] refactor the ThirdpartyDataprovider to exclude api endpoints
- [ ] Generate Attribute objects from metaclass instead
- [ ] Add CI
- [ ] Create Cron functionallity to fetch data each day
- [ ] create dev branch
- [ ] 

