FROM reg.douwa.io/hsbs/node:8-dw

ENV LANG C.UTF-8
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone

RUN mkdir -p /app
COPY dist /app/dist
COPY server /app
WORKDIR /app

RUN ls -l

RUN npm --registry https://registry.npm.taobao.org install
# RUN npm install

EXPOSE 80
CMD [ "npm", "start" ]
