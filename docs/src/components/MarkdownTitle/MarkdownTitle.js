import React from 'react'
import { fonts, colors, media } from "../../theme"
import Flex from '../Flex/Flex'


export default function MarkdownTitle({ title }) {
  return <Flex type="header" halign="space-between" valign="baseline">
    <h1
      style={{
        color: colors.dark,
        marginBottom: 0,
        marginTop: 60,
        ...fonts.header,

        [media.size('medium')]: {
          marginTop: 60,
        },

        [media.lessThan('small')]: {
          marginTop: 40,
        },
      }}>
      {title}
    </h1>
  </Flex>
}