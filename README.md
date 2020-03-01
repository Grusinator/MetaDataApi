[![Codacy Badge](https://api.codacy.com/project/badge/Grade/18b599f8a9594f39b0e109f1bc7a349d)](https://www.codacy.com/app/Grusinator/MetaDataApi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Grusinator/MetaDataApi&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/18b599f8a9594f39b0e109f1bc7a349d)](https://www.codacy.com/app/Grusinator/MetaDataApi?utm_source=github.com&utm_medium=referral&utm_content=Grusinator/MetaDataApi&utm_campaign=Badge_Coverage)
[![CircleCI](https://circleci.com/gh/Grusinator/MetaDataApi.svg?style=svg)](https://circleci.com/gh/Grusinator/MetaDataApi)

# MetaDataApi
## Introduction

This project aims to deliver a service where people interested in their personal lifes seen from a data perspective, can explore and gain insight in their own lifes. 
The idea for this project started out as an idea inspired by the biohacking community and my personal interest in data.    
This version is still work in progress and i still have a lot of ideas for improvement. 


if you would like to try it out follow this link:
[http://metadataapi.grusinator.com][Platform]

## Guideline 
Currently you can create a user and connect to different services that offer either Oauth authentication or open Rest Apis. 
If there are some services that you would like me to add is is fairly easy for me, just open an issue with a link to 
their website, preferably to their developer documentation.
To authenticate a specific provider, go to providers, select the one relevant and click on the Oauth button, 
from there you have to go though the login flow of that specific provider.

As soon as you have authenticated with oauth, the server should fetch a new version of your data.
If you have some data in a zip file of csvs or json files, that can be uploaded as well though the upload page. 

There might still be some bugs around. but feel free to create an issue if you experience problems here: [https://github.com/Grusinator/MetaDataApi/issues][Github Issue Tracking]

currently the best feature is that you can search in all text fields in your data, but hopefully more will come in the future.

Be aware that the page does not use https, and that since i am the administrator of the page, that i have access to the data that you upload, but i will of course not use or sell it. Though i cant access your profile on connected services ie. spotify, the system only stores a token that gives access to fetch the data from that service.

## Guideline for advanced users
if you know a bit of python i can recommend to try out the client lib that i have made. It is good for writing queries into the GraphQL endpoint
[grusinator/meta-data-client](https://github.com/Grusinator/meta-data-client)
i find it quite nice to use in a jupyter notebook, to visualize the data. 
You can also just try to query some data using the filter methods in the iGraphQL page on the platform. It is also good to explore the datamodel of your data a bit.

## Details on the implementation
It is build in Python Django, and uses Celery to handle background tasks such as processing of data. All the data is transformed to Json and being transformed 
into tables with relations to the nested objects using the django Mutant project to build the django objects dynamically.
Based on those models a graphql schema is being created so that these models can be queried.
I have made a fairly generic way of creating dataproviders, so that is is easy to add endpoints or add new providers. It can be done through the django admin panel.
But for that you need admin rights.

## Future vision
I am hoping to implement some further data analysis tools in the platform and visualization. I think it would be nice with a pivot table with graphs.
Later i would really like to do some automatic identifiction of attributes an label them semantically.
Of cource at some point i need to try to do some deep learning predictive analysis using LSTM or similar.
I hope that this could develop into a platform where users can build and share their own algorithms for analysing data 
from specific sources that others can then just activate on their on profile if they have data of the same type.

## Contribution
Let me know if you like the project, or would like to contribute. That would be nice.

[Platform]: http://metadataapi.grusinator.com

[Github Issue Tracking]: https://github.com/Grusinator/MetaDataApi/issues