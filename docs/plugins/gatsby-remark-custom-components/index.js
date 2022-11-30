const toString = require('mdast-util-to-string');
const visit = require('unist-util-visit');
const slugs = require('github-slugger')();

const parseColorLink = (node) => {
  const color = node.url.replace("color://", "")
  const html = `
    <div style="display: flex; align-items: center">
      <span>${toString(node)}</span>
      <div style="margin-left: 5px; margin-right: 5px; width: 20px; height: 20px; background-color: ${color}" />
      <span>${color}</span>
    </div>
  `
  node.type = "html"
  node.children = undefined
  node.value = html
}


module.exports = (
  { markdownAST },
) => {
  slugs.reset();

  visit(markdownAST, 'link', node => {
    if (node.url.startsWith("color://")) {
      parseColorLink(node)
      //   const defId = node.url.replace("def://", "")
      //   const html = `
      //     <a class="term-definition" data-def-id="${defId}">${toString(node)}</a>
      //   `
      //   node.type = "html"
      //   node.children = undefined
      //   node.value = html
    }
  });

  return markdownAST;
};