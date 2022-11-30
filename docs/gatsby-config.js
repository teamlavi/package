module.exports = {
  siteMetadata: {
    title: `LAVI Documentation`,
    description: `Lavi`,
    author: `@gatsbyjs`,
    siteUrl: `https://gatsbystarterdefaultsource.gatsbyjs.io/`,
  },
  plugins: [
    `gatsby-plugin-material-ui`,
    `gatsby-plugin-top-layout`,
    `gatsby-plugin-image`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `content`,
        path: `${__dirname}/content`,
      },
    },
    {
      resolve: 'gatsby-transformer-remark',
      options: {
        plugins: [
          'gatsby-remark-header-custom-ids',
          'gatsby-remark-definitions',
          'gatsby-remark-custom-components',
          'gatsby-remark-external-links',
          {
            resolve: 'gatsby-remark-images',
            options: {
              maxWidth: 840,
            },
          },
          {
            resolve: 'gatsby-remark-prismjs',
            options: {
              classPrefix: 'gatsby-code-',
            },
          },
          `gatsby-remark-copy-linked-files`,
          'gatsby-remark-smartypants'
        ],
      },
    },
    `gatsby-plugin-sharp`,
    `gatsby-transformer-sharp`,
  ],
}
