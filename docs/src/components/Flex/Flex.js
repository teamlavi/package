import React from 'react'

const Flex = ({
    basis = 'auto',
    children,
    direction = 'row',
    grow = 0,
    halign = 'flex-start',
    shrink = 1,
    type = 'div',
    valign = 'flex-start',
    ...rest
}) =>
    React.createElement(
        type,
        {
            style: {
                display: 'flex',
                flexDirection: direction,
                flexGrow: grow,
                flexShrink: shrink,
                flexBasis: basis,
                justifyContent: direction === 'row' ? halign : valign,
                alignItems: direction === 'row' ? valign : halign,
            },
            ...rest,
        },
        children,
    );

export default Flex;