/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: [
    '@study-abroad/shared-config',
    '@study-abroad/shared-feature-flags',
    '@study-abroad/shared-database',
    '@study-abroad/shared-logging',
  ],
  serverExternalPackages: ['@supabase/supabase-js', 'winston', 'winston-daily-rotate-file'],
};

module.exports = nextConfig;
