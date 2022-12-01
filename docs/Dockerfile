FROM node:16.13.0 as build

WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]

RUN npm install
COPY . .
RUN npm run build

FROM nginx as host

COPY --from=build /app/public /usr/share/nginx/html
