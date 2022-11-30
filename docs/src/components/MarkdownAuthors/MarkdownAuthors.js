import React from 'react'
import { fonts, colors, media } from "../../theme"
import Flex from '../Flex/Flex'
import toCommaSeparatedList from "../../utils/toCommaSeparatedList"


export default function MarkdownAuthors({ authors }) {
  return <Flex type="header" halign="space-between" valign="baseline">
    <h1
      style={{
        color: colors.dark,
        marginBottom: 0,
        ...fonts.small,
      }}>
      By {toCommaSeparatedList(authors, author => (
                        author
                    ))}
    </h1>
  </Flex>
}