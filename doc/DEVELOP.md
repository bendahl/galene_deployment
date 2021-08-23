# Developer Documentation
This documentation is intended for everyone who would like to either contribute to the project or simply customize the solution
to fit their needs. If you're looking for general information about this project, please refer to the [README](../README.md). For
information on how to use this project to deploy your own Galène stack, please take a look at [the user documentation](USER.md).

## Prerequisites
In order to modify or extend this solution, a couple of things are needed. Make sure to have the following things set up on 
your development machine:

- [Docker 20.10+](https://www.docker.com/)
- [Python 3.8+](https://www.python.org/)
- [Pulumi 3.8.0+](https://www.pulumi.com/docs/get-started/install/)
- [Google Cloud SDK 349.0.0+](https://cloud.google.com/sdk/)
- [Git 2.25.1+](https://git-scm.com/)
- [Vagrant 2.2.6+](https://www.vagrantup.com/)

Note that depending on what you would like to do, only part of these packages need to be installed on your machine.

## Local Testing
If you would like to work on the Docker image itself and customize the Galène server, you can easily build the image
locally using Docker. There is also a Vagrantfile located in the `vagrant/` directory that can be used to spin up an
Ubuntu based Virtual Box instance for more realistic test scenarios (server running behind a firewall/NAT).

### Docker
Everything that is needed to build the Docker image is contained in the `build/` directory. Probably the best way to learn
what the image is doing is to have a look at the `entrypoint.sh` file. As the name suggests, this is the entrypoint
of the Docker image. Customizations to the image functionality will most likely require changes in this file. 

To build the image locally, simply enter:

`docker build -t galene:master .`

The build will execute a [multi-stage Docker build](https://docs.docker.com/develop/develop-images/multistage-build/). This has 
the advantage of not needing to install [Go](https://golang.org/) on the build machine and also helps to keep the target image
clean. By default, the master branch of the Galène project will be used. If you would like to try out a specific tag instead,
simply [set the build argument](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg) __ARG_VERSION__.

The image can be run using this command (omit the "--rm" if you would like to persist the container):

`docker run --rm -p 8443:8443 -p 1194:1194 -p 1194:1194/udp -e ADMIN_PASSWORD=admin -p 32000-32079:32000-32079/udp galene:master`


### Vagrant
In order to perform more realistic tests and to see how the server handles behind NAT, a Vagrant box can be used. The Vagrant file
located in the `vagrant/` directory will spawn a Virtualbox VM equipped with Ubuntu 20.04 LTS, install Docker and add the 
vagrant user to the "docker" group upon startup. The following ports are all forwarded to localhost to mimic the firewall 
settings of the cloud instance (the format used to describe the ports is the same as for Docker (host_port:vm_port)):

- TCP:
  - 443:8443 (HTTPS)
  - 1194:1194 (TURN)
- UDP:
  - 1194 (TURN)
  - 32000-32079:32000-32079 (media streams)

You may, of course use the Vagrant box as a development environment as well. In that case, you may also want to preinstall the required
prerequisites upon first boot. You can do that by either extending the currently used inline bash provisioning script within 
the Vagrant file. Another possibility would be the use of another, external provisioner (recommended). For details on
how to accomplish this, please take a look at the [Vagrant documentation on provisioning](https://www.vagrantup.com/docs/provisioning).


## Extending the deployment
Galène uses a couple of configurations files (refer to the [Galène project's README](https://galene.org/README.html) for details).
As this project aims to provide a simple out-of-the-box experience, the configuration options were intentionally limited.
For instance, there is only a single group called "meeting" set up and recording meetings is disabled. Take a look at the 
[meeting.json](../build/groups/meeting.json) to see what the settings for this group are. You may of course tweak them to suit 
your use case. To add a group, simply add a second file named after your group. **Note, however, that some changes you apply 
to the group will also have to be supported by the image and possibly the Pulumi deployment.**

_Example:_


If you would like to support more than 80 users, you will need to make changes in the following places:

- `build/groups/meeting.json` -> set "max-clients" to a value that suits your needs
- `build/docker-entrypoint.sh` -> adjust the port range for the media streams
- `build/Dockerfile` -> for documentation purposes, the `EXPOSE` directive should be adjusted to reflect the changes
- `deploy/galeneinstance.py` -> make sure to extend the instance mapping function `map_instance_type(max_user: int)`

Other possibilities include the use of __pre-__ and __post-__ deployment steps within the GitHub action workflows (take 
a look at the [GitHub actions reference](https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#sending-values-to-the-pre-and-post-actions) for more information).
This could be used to automate the setup of your DNS entry, for instance. 

Last, but not least, you may as well adjust the Pulumi deployment itself. There are various ways to do this:

- Change the global Pulumi settings in `deployment/Pulumi.yaml`
- Change the stack configuration in `deployment/stacks/Pulumi.dev.yaml`
- Create a new stack 
- Make changes to variable handling in `deploy/__main.py__`
- Make changes to the main deployment logic in `deploy/galeneinstance.py`


Hopefully this will help you to get started to make changes to this project. In case anything should be missing, please
let me know.