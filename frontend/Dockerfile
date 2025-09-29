FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci || npm i

COPY . .

EXPOSE 5173

ENV VITE_API_BASE=http://localhost:5000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
