// import { createGlobalStyle } from 'styled-components'
import styled from 'styled-components';
import { colors } from './theme';



const prismColors = {
    char: '#D8DEE9',
    comment: '#B2B2B2',
    keyword: '#c5a5c5',
    lineHighlight: '#353b45', // colors.dark + extra lightness
    primitive: '#5a9bcf',
    string: '#8dc891',
    variable: '#d7deea',
    boolean: '#ff8b50',
    punctuation: '#88C6BE',
    tag: '#fc929e',
    function: '#79b6f2',
    className: '#FAC863',
    method: '#6699CC',
    operator: '#fc929e',
};

const GlobalStyle = styled.div`
    .gatsby-highlight {
        background: ${colors.dark};
        color: ${colors.white};
        border-radius: 10px;
        overflow: auto;
        tab-size: 1.5em;
        --webkit-overflow-scrolling: touch;
    }

    .gatsby-highlight > code[class*="gatsby-code-"],
    .gatsby-highlight > pre[class*="gatsby-code-"],
    .gatsby-highlight > pre.prism-code {
        height: auto !important;
        margin: 1rem;
        font-size: 14px;
        line-height: 20px;
        white-space: pre-wrap;
        word-break: break-word;
    }

    .gatsby-highlight + .gatsby-highlight {
        margin-top: 20px;
    }

    .gatsby-highlight-code-line {
        background-color: ${prismColors.lineHighlight};
        display: block;
        margin: -0.125rem calc(-1rem - 15px);
        padding: 0.125rem calc(1rem + 15px);
    }

    .token.attr-name {
        color: ${prismColors.keyword};
    }

    .token.comment, .token.block-comment, .token.prolog, .token.doctype, .token.cdata {
        color: ${prismColors.comment};
    }

    .token.property, .token.number, .token.function-name, .token.constant, .token.symbol, .token.deleted {
        color: ${prismColors.primitive};
    }

    .token.boolean {
        color: ${prismColors.boolean};
    }

    .token.tag {
        color: ${prismColors.tag};
    }

    .token.string {
        color: ${prismColors.string};
    }

    .token.punctuation {
        color: ${prismColors.punctuation};
    }

    .token.selector, .token.char, .token.builtin, .token.inserted {
        color: ${prismColors.char};
    }

    .token.function {
        color: ${prismColors.function};
    }

    .token.operator, .token.entity, .token.url, .token.variable {
        color: ${prismColors.variable};
    }

    .token.attr-value {
        color: ${prismColors.string};
    }

    .token.keyword {
        color: ${prismColors.keyword};
    }

    .token.atrule, .token.class-name {
        color: ${prismColors.className};
    }

    .token.important {
        font-weight: 400;
    }

    .token.bold {
        font-weight: 700;
    }

    .token.italic {
        font-style: italic;
    }

    .token.entity {
        cursor: help;
    }

    .namespace {
        opacity: 0.7;
    }
`

export default GlobalStyle