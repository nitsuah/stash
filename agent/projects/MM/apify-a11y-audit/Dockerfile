FROM apify/actor-node-playwright-chrome:24-1.60.0-slim

COPY --chown=myuser:myuser package*.json ./
RUN npm --quiet set progress=false \
    && npm install --omit=dev --omit=optional \
    && npm cache clean --force

COPY --chown=myuser:myuser . ./

CMD npm start --silent
