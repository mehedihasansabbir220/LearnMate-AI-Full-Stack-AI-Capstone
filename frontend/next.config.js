/** @type {import('next').NextConfig} */
// The app is fully client-side, so build it as static files (frontend/out) for free static hosting.
const nextConfig = { output: "export" };
module.exports = nextConfig;
