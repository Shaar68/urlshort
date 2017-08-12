# urlshort
My little url shortener

[DockerHub](https://hub.docker.com/r/aetea/urlshort/)

## Recommendations
I strongly recommend that you make a volume for for the URL database (`/app/urls.db`). See the [docker-compose.sample.yml](https://github.com/aetea/urlshort/blob/master/docker-compose.sample.yml) file for example usage.

## Environment Variables
- APP_PORT the port to run the HTTP web server on.
- APP_DEBUG set to 'true' (without quotes) if you want to enable debug mode.

## To install and run.
### With docker and docker-compose
1. Install docker and docker-compose.
2. Customize the [docker-compose.sample.yml](https://github.com/aetea/urlshort/blob/master/docker-compose.sample.yml) file to your needs and rename it to `docker-compose.yml`.
3. Run `docker-compose up -d` in the directory where you placed the `docker-compose.yml`.
4. Done!
