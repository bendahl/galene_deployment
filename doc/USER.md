# User Manual
## Preface
This document contains information about the installation and usage of the [Galène Server](https://galene.org/) automation. The goal of this document
is to enable a user of the software to create a working Galène instance in the Google Cloud. It also outlines the process of how 
to clean up all previously created resources when they are no longer required. This is not an extensive reference manual explaining the 
inner workings of Galène or the tools used as part of the automation solution. Where appropriate, references to third party documentation will be included, however.
Prior knowledge of cloud software or automation solutions is not required to follow through this document. Some of the processes described here are fairly technical, however,
and should be read carefully.

## Terminology
The following list contains a few keywords that are used throughout the document in order to prevent confusion.

- _Automation Solution / IaC Tool_
  
    This project automates the creation of a conference server (Galène) in the Google Cloud. To do so, a specialized tool called 
    "Pulumi" is used. This tool helps to automate the creation of servers and other resources in the cloud using code.
    Such software is commonly referred to as an IaC (Infrastructure as Code) tool. 


- _Deployment_

    A deployment refers to a software or a bundle of components that are installed on some remote location (in this case
    the Galène Server and its components).
  
  
- _Shell_ 
  
    A shell typically refers to a textual environment that allows the user to interact with the system using commands. Depending on 
    the context (especially depending on the operating system used) this is sometimes also referred to as a terminal or command line.
    Throughout this document the term shell is used.


## Structure
There are three main parts to this document:

- _General Information_
    
    Some general information about this project, as well as possible caveats and things to look out for. Read this first.
    

- _Web Based Deployment_

    To use the web based deployment method, only a web browser is required. The creation of a few (free) online accounts 
    might be necessary to complete the necessary steps, though. The guide aims to be fairly detailed in description in order to ease
    the process.
  

- _Deployment from Local Machine_
    
    This type of deployment requires some prerequisites to be installed on the machine that's running the deployment and 
    a certain familiarity with a shell environment. The steps involved in the deployment are described as step-by-step instructions.
    References to third party documentation are given where appropriate. Instructions on shell basics, like setting environment
    variables, are not part of this guide. 


## General Information

Todo: admin user, meeting room, user numbers, instances, SSL, ....

## Web Based Deployment

### Prerequisites

### Step-By-Step Guide


## Deployment from Local Machine
Note that the local installation will require the use of a shell (or, in other words, console) environment. If you're not familiar
using such environments, please refer to the web based installation instead. Also, the following setup was tested on Linux.
The shell available on MacOS should behave similarly, but deviations are possible. Using Windows is also possible, but was not
tested either.

### Prerequisites
The following software will need to be installed on your local machine:

- [Python 3.8+](https://www.python.org/)
- [Pulumi 3.8.0+](https://www.pulumi.com/docs/get-started/install/)
- [Google Cloud SDK 349.0.0+](https://cloud.google.com/sdk/)
- [Git 2.25.1+](https://git-scm.com/)

### Step-By-Step Guide

**IMPORTANT NOTE**

In order to successfully carry out a deployment via Pulumi as described below, you will need to create a Pulumi account and log in to this account
in your shell. To do so, simply enter `pulumi login`. Alternatively, if you do not wish to use the Pulumi online service, you may use a local
state file. State files contain meta data about a deployment (or "stack" in Pulumi terms) and are vital to correctly deploy and destroy resources.
Using a local state file can be accomplished by "logging in" to Pulumi locally. Simply enter `pulumi login --local` in your shell and all state 
information will be kept locally. 

#### Deployment
- If you do not currently own a Google Cloud account, sign up for a free [Google Cloud account](https://cloud.google.com/).
- Sign in to your Google Cloud account and set up a project on named "galene-deployment". Detailed instructions
on how to create a project in Google Cloud can be found in the [reference documentation](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
- Now that the basic cloud setup is completed, follow the [instructions on how to set up Pulumi for Google Cloud](https://www.pulumi.com/docs/get-started/gcp/begin/).
Make sure to pick your operating system according to your needs and "Python" as a language runtime.
- Once you've completed the basic setup, it's time to clone the [galene_deployment repository from GitHub](https://github.com/bendahl/galene_deployment). You can
either use a graphical Git frontend to do so, or simply use a shell and enter `git clone https://github.com/bendahl/galene_deployment.git`. Alternatively,
  if you've configured an SSH key on GitHub, you may use `git@github.com:bendahl/galene_deployment.git`.
- Navigate to the now locally available `galene_deployment` directory.
- Within the project main directory navigate to the subdirectory `deploy`.
- If you haven't yet opened a shell, it's now time to open a shell within the current directory.
- Make sure to set the following environment variables:
  - _ADMIN_PASSWORD:_ The password for the Galène admin user.
  - _MAX_USER:_  Maximum number of users. Default: 10. This should not exceed 100. The number is used to decide which instance size is needed 
    (more users = more hardware = higher costs). A number less than 10 does not make sense, as it doesn't affect the sizing decision.
- To deploy Galène to Google Cloud enter `pulumi up`. A short summary outlining the planned changes will appear. Confirm this dialog by 
  selecting "yes" to go through with the deployment.
- After a short while the deployment should be complete and you will be presented with some basic information such as:
    - _Container Instance Name:_ The name of your server within Google Cloud.
    - _External IP:_ The address at which your server may be contacted from the outside (via Browser, etc...)
    - _Meeting URL:_ This is the link to your online meeting room. Use this to enter the meeting. Make sure to send this link to all participants.

#### Cleaning Up
When you don't need the meeting room anymore, you should clean up all resources running in the Cloud to reduce cost. To do so, follow these steps:
- In a shell, navigate back to the `galene_deployment/deploy` directory.
- Enter `pulumi destroy -f`
- Wait until the process finishes. **Do not interrupt this process or you might end up with an inconsistent system state.** This can be cleanup up by
Pulumi, but will require extra steps.