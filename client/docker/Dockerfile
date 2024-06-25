FROM docker.io/node:latest as base

FROM base as node-build-stage

COPY client/package.json client/package-lock.json* ./

RUN npm ci

RUN npm install -g @angular/cli

# RUN npm install @rollup/rollup-linux-x64-gnu

FROM base as node-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY --from=node-build-stage node_modules ./

COPY . ${APP_HOME}

CMD [ "npm","start" ]