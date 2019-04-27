[![Codacy Badge](https://api.codacy.com/project/badge/Grade/18b599f8a9594f39b0e109f1bc7a349d)](https://www.codacy.com/app/Grusinator/MetaDataApi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Grusinator/MetaDataApi&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/Grusinator/MetaDataApi.svg?style=svg)](https://circleci.com/gh/Grusinator/MetaDataApi)

# MetaDataApi
tags: Quantified Self, Biohacking, RDF, OWL, Oauth, graphql, JSONSchema, OpenMHealth
## Description
This project aims to gather relevant data from a lot of services an analyse on top. You might call it HumanIntelligence 
It is based on the semantic web idea, so json data can just be loaded in from Api endpoints, that you create.  
First a datamodel from that json file is created, and thereafter instances of objects and attributes are added.
You can also upload RDF schemas defined in OWL, and thereafter upload your rdf data to it. The goal is to standardize the incoming data by comparing with other models, and mapping it onto a more covering model within the field. My initial approach has been to take the OpenMHealth [ref](http://www.openmhealth.org/) data model which is defined in JSONSchema, i have converted it to OWL. 


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
[grusinator/meta-data-client](https://github.com/Grusinator/meta-data-client)

how to test if an object instance or attribute instance allready exists. If the parrent attribute is the same, the object is too. If an object relation has the same 2 objects, then it is the same, but the objects must be tested more delicately. 

inferring some sort of uniqueness score?

or just comparing with all previously created objects, nobody with the same combination of objects and relations? its a new one then.
  
