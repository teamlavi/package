import { Typography } from '@mui/material';
import React, { useEffect, useState } from 'react'
import Tooltip, { TooltipProps, tooltipClasses } from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';
import ReactDOM from "react-dom"

const HtmlTooltip = styled(({ className, ...props }) => (
    <Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
    [`& .${tooltipClasses.tooltip}`]: {
        fontSize: theme.typography.pxToRem(12),
        backgroundColor: "rgb(255, 255, 255)",
        color: "rgba(0, 0, 0, 0.87)",
        transition: "box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms",
        borderRadius: "4px",
        boxShadow: "rgba(0, 0, 0, 0.2) 0px 2px 1px -1px, rgba(0, 0, 0, 0.14) 0px 1px 1px 0px, rgba(0, 0, 0, 0.12) 0px 1px 3px 0px",
        overflow: "hidden",
    },
}));

function DefinitionContent({ def }) {
    return <div style={{ padding: "8px" }}>
        {def &&
            <>
                <Typography variant="h5" component="div">
                    {def.term}
                </Typography>
                <Typography sx={{mt: "3px"}} variant="body2">
                    Definition: {def.definition}
                </Typography>
                <Typography sx={{mt: "3px"}} variant="body2">
                    Usage: {def.usage}
                </Typography>
                <a style={{marginTop: "3px"}} target="_blank" href={def.source}>
                    Source
                </a>
            </>
        }
    </div>
}

function Definition({ id, text }) {
    const [def, setDef] = useState(null)
    // useEffect(() => {
    //     fetch(`${process.env.GATSBY_DOCS_PATH}/terms/${id}`)
    //         .then((response) => response.json())
    //         .then((data) => setDef(data));
    // }, [])
    return <HtmlTooltip
        arrow
        title={<DefinitionContent def={def} />}
    >
        <a className="definition">
            {text}
        </a>
    </HtmlTooltip>
}


export default function definitionTooltip(element) {
    const id = element.getAttribute("data-def-id")
    const text = element.innerText
    ReactDOM.render(<Definition id={id} text={text} />, element)
}