import { graphql } from "gatsby";
import * as React from "react";
import ReactDOM from "react-dom"
import MarkdownPage from "../components/MarkdownPage/MarkdownPage";
import PropTypes from 'prop-types';
import Layout from "../components/Layout/Layout";
import { sectionListPublicDocs } from '../utils/sectionLists';
import { createLinkDocs } from '../utils/createLink';
import { Tooltip } from "@mui/material"
import definitionTooltip from "../components/Definition/Definition";

const Docs = ({ data, location }) => {
    let sectionList = sectionListPublicDocs;
    React.useEffect(() => {
      const elements = Array.from(document.getElementsByClassName('term-definition'))
      elements.forEach(e => definitionTooltip(e))
    }, [])
    return <Layout>
        <MarkdownPage {...data} createLink={createLinkDocs} location={location} sectionList={sectionList} />
    </Layout>
}

Docs.propTypes = {
    data: PropTypes.object.isRequired,
};

export const pageQuery = graphql`
    query TemplateDocsMarkdown($slug: String!) {
      markdownRemark(fields: {slug: {eq: $slug}}) {
        html
        frontmatter {
          id
          title
          permalink
        }
        fields {
          path
          slug
        }
      }
    }
  `;

export default Docs