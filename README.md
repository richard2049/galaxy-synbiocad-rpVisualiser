# Galaxy rpVisualiser

REST server instance of a visualiser for the output of the RetroPath analysis pipeline

## Getting Started

This is a docker galaxy tools, and thus, the docker needs to be built locally where Galaxy is installed. 

### Build the tool

```
docker build --no-cache -t brsynth/rpvisualiser .
```

And then run the container (use tmux or -deamon):

```
docker run --network host -p 8998:8998 -e LD_LIBRARY_PATH='/opt/conda/bin/../lib' brsynth/rpvisualiser
```

### Prerequisites

TODO

### Installing galaxy tool

TODO

## Running the tests

TODO

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Galaxy](https://galaxyproject.org) - The Galaxy project

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

TODO

## Authors

* **Anaelle Badier** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson
* Melchior du Lac
