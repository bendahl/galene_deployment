# Galène Deployment
This project automates the deployment of the [Galène video conference server](https://galene.org/). The main goals of this
project are simplicity and cost efficiency, offering a quick to set up and easy to operate video conferencing solution for
personal use.

The setup currently
only supports [Google Cloud](https://cloud.google.com/) at this point, but is meant to be extensible. Feel free to fork this project and make improvements. If you 
would like to contribute to this project directly, simply open a pull request. This is usually a good first step to start a 
discussion about possible changes / improvements before committing significant time implementing something.

## Project Structure
There are various parts to this project. In order to ease navigation the different parts of this project are split over
several subdirectories. Below you will find a list of the different directories and their contents.

- __.github/__
  
    Contains the GitHub Actions workflow definitions. There are currently two workflows available:
    - The workflow defined in `up.yml` will deploy the  communication solution to the cloud
    - The workflow defined in `destroy.yml` will clean up all resources.


- __build/__

    Contains the sources of the Galène Server Docker image. If you wish to customize the server itself or build a different
    version of it, this is the place to look.
  

- __deploy/__
  
    The deploy directory contains the actual deployment definition. The deployment is based on [Pulumi](https://www.pulumi.com/), 
    a modern infrastructure as code tool. The code is written in Python.
  

- __doc/__ 

    The doc directory contains further documentation. There is a user documentation as well as a developer documentation.



- __vagrant/__
    
    Throughout the development process of the Galène Server Docker image [Vagrant](https://www.vagrantup.com/) proved to be a great
    tool to build a test environment that comes close to an actual Galène deployment behind NAT. You will need [Virtualbox](https://www.virtualbox.org/) and Vagrant
    installed on your machine if you would like ot use the environment for testing purposes.
    

## Usage
The basic usage and configuration is described in the [user manual](doc/USER.md). Please consult this document for furhter
instructions.

## Development
If you would like to extend or customize any part of this project, feel free to do so. The [developer documentation](doc/DEVELOP.md)
will provide some basic information about the required prerequisites and how to get started. 

## Related Projects
This project incorporates different parts from other Open Source projects, without which this solution would not have been possible:

- [Galène video conferencing server](https://galene.org/)
- [Docker Galène](https://gitlab.com/andic/docker-galene)
- [Pulumi](https://www.pulumi.com/)
- [Vagrant](https://www.vagrantup.com/)
- [Virtualbox](https://www.virtualbox.org/)

A special thanks goes out to the Galène project for providing an easy to deploy and fairly lightweight WebRTC solution. In addition,
I would very much like to thank the Docker Galène project, which provided the basic building blocks for the final Docker image.

## License 
For the purpose of this project the MIT License was chosen, as it is compatible with many other licensing schemes and 
provides the user with maximum freedom. For details see [LICENSE.md](LICENSE.md)