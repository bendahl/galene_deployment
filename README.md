# Galène Deployment
This project automates the deployment of the [Galène video conference server](https://galene.org/). The main goals of this
project are simplicity and cost efficiency, offering a quick to set up and easy to operate video conferencing solution for
personal use.

The setup currently
only supports [Google Cloud](https://cloud.google.com/) at this point, but is meant to be extensible. Feel free to fork this project and make improvements. If you 
would like to contribute to this project directly, simply open a pull request. This is usually a good first step to start a 
discussion about possible changes / improvements before committing significant time implementing something.

## Project Structure
There are various parts to this project. Below you will find an annotated directory tree outlining the basic structure.

```
galene_deployment/                                      
├── build                               Docker related files needed to build the actual container image
│   ├── docker-entrypoint.sh      Start script that is executed upon start of the container.
│   ├── Dockerfile                Dockerfile describing the contents of the container image.
│   └── groups                    Group configuration of the Galène server.
│       └── meeting.json          Standard group that is used as the default (name: "meeting").
├── README.md                           This document.
└── vagrant                             Vagrant related configuration used for local testing in a VM
    └── Vagrantfile                     Vagrantfile to set up a single VM, including Ubuntu 20 and Docker
```

## Usage

### Prerequisites

## Development

### Prerequisites

## Related Projects
This project incorporates different parts from other Open Source projects, without which this solution would not have been possible:

- [Galène video conferencing server](https://galene.org/)
- [Docker Galène](https://gitlab.com/andic/docker-galene)
- [Pulumi](https://www.pulumi.com/)
- [Vagrant](https://www.vagrantup.com/)

