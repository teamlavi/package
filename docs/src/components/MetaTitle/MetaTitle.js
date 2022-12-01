import React from 'react';
import {colors} from '../../theme';

const MetaTitle = ({children, title, style = {}, onDark = false}) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      color: onDark ? colors.subtleOnDark : colors.subtle,
      fontSize: 14,
      fontWeight: 700,
      lineHeight: 3,
      textTransform: 'uppercase',
      textAlign: 'start',
      letterSpacing: '0.08em',
      ...style,
    }}>
    {children}
  </div>
);

export default MetaTitle