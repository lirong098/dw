FROM reg.douwa.io/library/node:dev

COPY dist /app/dist
COPY server /app

RUN npm install

EXPOSE 8080
CMD [ "npm", "start" ]
