# KAWACH Frontend (Vite + React)

This frontend calls the KAWACH Flask backend APIs.

## Local Run

1. Install dependencies:

```bash
npm install
```

2. Copy the environment template and set your backend URL:

```bash
cp .env.example .env
```

`VITE_API_BASE_URL` should point to your backend, for example:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000
```

3. Start dev server:

```bash
npm run dev
```

## Production Build

```bash
npm run build
```

Build output is generated in `dist/`.

## Deploy (Recommended: Vercel for frontend + Render for backend)

### 1) Deploy Backend (Render)

1. Create a new **Web Service** from your repo.
2. Set root directory to `backend`.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
gunicorn app:app
```

5. After deploy, copy backend URL, for example:

```text
https://kawach-backend.onrender.com
```

### 2) Deploy Frontend (Vercel)

1. Import your repo in Vercel.
2. Set project root directory to `frontend_web`.
3. Add environment variable:

```env
VITE_API_BASE_URL=https://kawach-backend.onrender.com
```

4. Deploy.

## Alternate Static Deploy (Netlify/GitHub Pages)

You can deploy `dist/` to any static host. Just make sure `VITE_API_BASE_URL` points to your live backend before building.
