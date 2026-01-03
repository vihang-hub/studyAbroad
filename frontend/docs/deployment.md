# Frontend Deployment Guide

This guide covers deploying the Next.js frontend to Vercel.

## Prerequisites

- Vercel account
- Vercel CLI installed (`npm i -g vercel`)
- GitHub repository connected to Vercel
- Required environment variables ready

## Environment Variables

Configure these in Vercel dashboard under Project Settings > Environment Variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk public key | Yes |
| `CLERK_SECRET_KEY` | Clerk secret key | Yes |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe public key | Yes |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key | Yes |
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |

## Deployment Options

### Option 1: Vercel Dashboard (Recommended)

1. **Connect Repository**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Select the repository root

2. **Configure Project**
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Add Environment Variables**
   - Add all required variables listed above
   - Set appropriate scopes (Production, Preview, Development)

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Vercel CLI

```bash
# Login to Vercel
vercel login

# Navigate to frontend
cd frontend

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Option 3: GitHub Actions

Create `.github/workflows/deploy-frontend.yml`:

```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'
      - 'shared/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## Build Configuration

### next.config.js

Ensure correct configuration for monorepo:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  transpilePackages: ['@study-abroad/shared'],
  experimental: {
    outputFileTracingRoot: path.join(__dirname, '../'),
  },
};

module.exports = nextConfig;
```

### vercel.json (Optional)

```json
{
  "framework": "nextjs",
  "installCommand": "npm install",
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}
```

## Domain Configuration

### Custom Domain

1. Go to Project Settings > Domains
2. Add your domain (e.g., `app.yourdomain.com`)
3. Configure DNS:
   - CNAME: `cname.vercel-dns.com`
   - Or A record: `76.76.21.21`

### SSL Certificate

Vercel automatically provisions SSL certificates via Let's Encrypt.

## Performance Optimization

### Edge Functions

For low-latency middleware:

```typescript
// middleware.ts
export const config = {
  runtime: 'edge',
};
```

### Image Optimization

Next.js Image component is optimized automatically:

```typescript
import Image from 'next/image';

<Image
  src="/hero.png"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>
```

### Analytics

Enable Vercel Analytics in project settings for Core Web Vitals monitoring.

## Preview Deployments

Every pull request creates a preview deployment:

- URL format: `https://your-project-git-branch-name.vercel.app`
- Automatic comments on PRs with preview link
- Share with team for review

## Production Checklist

Before deploying to production:

- [ ] All environment variables configured
- [ ] Clerk production keys (not test keys)
- [ ] Stripe production keys (not test keys)
- [ ] Supabase production project URL
- [ ] Backend URL points to production API
- [ ] Custom domain configured
- [ ] Analytics enabled
- [ ] Error tracking (Sentry) configured

## Monitoring

### Vercel Dashboard

- Deployments: Build logs and status
- Analytics: Performance metrics
- Functions: Serverless function logs

### View Logs

```bash
vercel logs production
```

### Real User Monitoring

Enable in Vercel dashboard:
- Speed Insights
- Web Analytics

## Rollback

### Via Dashboard

1. Go to Deployments
2. Find previous successful deployment
3. Click "Promote to Production"

### Via CLI

```bash
# List deployments
vercel ls

# Rollback to specific deployment
vercel rollback DEPLOYMENT_ID
```

## Troubleshooting

### Build Failures

1. Check build logs in Vercel dashboard
2. Run locally: `npm run build`
3. Verify all dependencies installed

### Environment Variable Issues

1. Verify variable names match exactly
2. Check scope (Production/Preview/Development)
3. Redeploy after changing variables

### Monorepo Issues

1. Ensure root directory set to `frontend`
2. Check `transpilePackages` includes shared package
3. Verify `outputFileTracingRoot` for standalone output

### Clerk Authentication Errors

1. Verify CLERK_SECRET_KEY is set
2. Check Clerk dashboard for allowed domains
3. Ensure redirect URLs are configured

### API Connection Errors

1. Verify NEXT_PUBLIC_API_URL is correct
2. Check CORS configuration on backend
3. Ensure backend is running and accessible

## Security

### Headers

Next.js security headers are configured in `next.config.js`:

```javascript
const securityHeaders = [
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
];
```

### Environment Variable Protection

- Never commit `.env` files
- Use Vercel's encrypted environment variables
- Rotate secrets regularly

## Cost Optimization

- Vercel Free tier: 100GB bandwidth/month
- Pro tier for teams: $20/member/month
- Enterprise: Custom pricing

Tips:
- Use `next/image` for automatic optimization
- Enable ISR for static pages
- Cache API responses where possible
