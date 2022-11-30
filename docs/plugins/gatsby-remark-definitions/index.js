/*!
 * Based on 'gatsby-remark-autolink-headers'
 * Original Author: Kyle Mathews <mathews.kyle@gmail.com>
 * Copyright (c) 2015 Gatsbyjs
 */

const toString = require('mdast-util-to-string');
const visit = require('unist-util-visit');
const slugs = require('github-slugger')();


module.exports = (
  {markdownAST},
) => {
  slugs.reset();

  visit(markdownAST, 'link', node => {

    if (node.url.startsWith("def://")) {
      const defId = node.url.replace("def://", "")
      const html = `
        <a class="term-definition" data-def-id="${defId}">${toString(node)}</a>
      `
      node.type = "html"
      node.children = undefined
      node.value = html
    }
  });

  return markdownAST;
};