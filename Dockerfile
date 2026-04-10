FROM node:18-slim
WORKDIR /app
RUN npm install -g serve
COPY index.html .
COPY css/ css/
COPY js/ js/
EXPOSE 8080
CMD ["serve", "-s", ".", "-l", "8080"]
