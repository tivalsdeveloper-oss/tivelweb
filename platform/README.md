# tivalsdeveloper Store Builder Platform

A business-facing service platform for ordering website stores.

## Customer flow

1. Public landing page
2. View Starter, Business and Pro pricing
3. Create an account with username, email and password
4. Verify email using a 6-digit code
5. Sign in
6. Open the client dashboard
7. Choose a store package and submit business requirements
8. Track project and payment status

## Database

Uses PostgreSQL tables in the `store_builder` schema on WoWSQL: `users`, `packages`, and `orders`.

## Required server environment variables

- `DATABASE_URL` — WoWSQL PostgreSQL connection string
- `JWT_SECRET` — long random signing secret
- `GMAIL_USER` — Gmail account used for verification emails
- `GMAIL_APP_PASSWORD` — Gmail app password

Never commit these values to GitHub.

## Run

From this directory:

```bash
npm install
npx netlify dev
```

The publish directory is `public` and functions are in `netlify/functions`.
