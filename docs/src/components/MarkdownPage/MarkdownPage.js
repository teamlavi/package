import React from 'react'
import { Grid } from "@mui/material"
import { cssTheme, fonts, media } from "../../theme"
import MarkdownTitle from "../MarkdownTitle/MarkdownTitle"
import MarkdownAuthors from "../MarkdownAuthors/MarkdownAuthors"
import styled from 'styled-components'
import GlobalStyle from '../../prism-theme';
import findSectionForPath from '../../utils/findSectionForPath';
import toCommaSeparatedList from '../../utils/toCommaSeparatedList';
import Sidebar from '../Sidebar/Sidebar'

const Markdown = styled.div(cssTheme.markdown);
const Content = styled.div(cssTheme.layout.content);
const EditLink = styled.a(cssTheme.layout.editLink);

export default function geMarkdownPage({ markdownRemark, location, sectionList, blog, authors = [], date }) {
    const path = markdownRemark.fields.path
    const hasAuthors = authors.length > 0;
    const titlePrefix = markdownRemark.frontmatter.title || '';
    return <div style={{ display: "flex" }}>
        <Sidebar
            blog={blog}
            location={location}
            sectionList={sectionList}
            defaultActive={findSectionForPath(
                location.pathname,
                sectionList,
            )}
        />
        <Grid
            container
            direction="column"
            alignItems="center"
            justifyContent="center"
            sx={{width: "100%"}}
        >
            <Grid item sx={{width: "100%"}}>
                <MarkdownTitle title={titlePrefix} path={path} />
                {(date || hasAuthors) && (
                    <div styles={{ marginTop: 15 }}>
                        {date}{' '}
                        {hasAuthors && (
                            <span styles={{ lineHeight: 1.75 }}>
                                By{' '}
                                {toCommaSeparatedList(authors, author => (
                                    author
                                ))}
                            </span>
                        )}
                    </div>
                )}
                <Content style={{ padding: "0px 20px" }}>
                    <GlobalStyle>
                        <Markdown
                            dangerouslySetInnerHTML={{ __html: markdownRemark.html }}
                        />
                    </GlobalStyle>
                </Content>
            </Grid>
        </Grid>
    </div>

}