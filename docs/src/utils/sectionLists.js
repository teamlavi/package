import navDocsPublic from '../../content/docs/nav.yml';

const sectionListPublicDocs = navDocsPublic.map((item) => ({
    ...item,
    directory: "docs"
}));

export {
    sectionListPublicDocs,
};