// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   async redirects() {
//     return [
//       {
//         source: "/",
//         destination: "/dashboard",
//         permanent: true,
//       },
//     ];
//   },
//   images: {
//     remotePatterns: [
//       {
//         protocol: "https",
//         hostname: "img.clerk.com",
//       },
//     ],
//   },
//   webpack: (webpackConfig, { webpack }) => {
//     webpackConfig.plugins.push(
//       // Remove node: from import specifiers, because Next.js does not yet support node: scheme
//       // https://github.com/vercel/next.js/issues/28774
//       new webpack.NormalModuleReplacementPlugin(/^node:/, (resource) => {
//         resource.request = resource.request.replace(/^node:/, "");
//       }),
//     );

//     return webpackConfig;
//   },
// };

// module.exports = nextConfig;
/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: "/",
        destination: "/dashboard",
        permanent: true,
      },
    ];
  },

  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://127.0.0.1:5328/api/:path*'
            : '/api/',
      },
    ];
  },

  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "img.clerk.com",
      },
    ],
  },

  webpack: (webpackConfig, { webpack }) => {
    webpackConfig.plugins.push(
      new webpack.NormalModuleReplacementPlugin(/^node:/, (resource) => {
        resource.request = resource.request.replace(/^node:/, "");
      }),
    );
    return webpackConfig;
  },
};

module.exports = nextConfig;

