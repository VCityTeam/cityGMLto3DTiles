Build the ad-hoc images manually by using
```bash
docker build -t vcity/collect_lyon_data Collect-DockerContext
docker build -t vcity/3duse 3DUse-DockerContext
docker build -t vcity/citygml2stripper CityGML2Stripper-DockerContext
docker build -t vcity/citytiler CityTiler-DockerContext
```
