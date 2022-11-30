import React from 'react'
import Layout from '../../../components/Layout/Layout'
import Sidebar from '../../../components/Sidebar/Sidebar';
import { Card, Grid } from "@mui/material"
import MarkdownTitle from '../../../components/MarkdownTitle/MarkdownTitle';
import TasksTable from '../../../components/TasksTable/TasksTable';
import { cssTheme } from '../../../theme';
import styled from 'styled-components'
import { sectionListPublicDocs } from '../../../utils/sectionLists';
import findSectionForPath from '../../../utils/findSectionForPath';
import GlobalStyle from '../../../prism-theme';
import NotFoundPage from "../../404";

const Content = styled.div(cssTheme.layout.content);

export default function Tasks({ location }) {
    if (!process.env.GATSBY_ALLOW_INTERNAL_CONTENT) {
        return <NotFoundPage />
    }
    let sectionList = sectionListPublicDocs;
    return <Layout>
        <div style={{ display: "flex" }}>
            <Sidebar
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
                sx={{ width: "100%" }}
            >
                <Grid item sx={{ width: "100%" }}>
                    <MarkdownTitle title="2023 Tasks" />
                    <Content style={{ padding: "0px 5px" }}>
                        <GlobalStyle>
                            <Card>
                                <TasksTable />
                            </Card>
                        </GlobalStyle>
                    </Content>
                </Grid>
            </Grid>
        </div>
    </Layout>
}