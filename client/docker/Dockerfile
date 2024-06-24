FROM docker.io/node:latest as base

FROM base as node-build-stage

# RUN apk add --no-cache libc6-compat

COPY ../package.json ../package-lock.json* ./

RUN npm ci

RUN npm install -g @angular/cli

FROM base as node-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY --from=node-build-stage /node_modules ./node_modules

COPY . ${APP_HOME}

CMD [ "npm","start" ]