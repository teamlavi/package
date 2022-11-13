import React, { useCallback } from 'react';
import { Graphics, Text } from '@inlet/react-pixi';
import { TextStyle } from "pixi.js"

const Circle = ({ x, y, radius, stats }) => {
    const draw = useCallback((g) => {
        g.clear();
        g.beginFill(0xff3300);
        g.drawCircle(x, y, radius)
        g.endFill();
    }, [x, y, radius]);
    console.log(stats)
    return <>
        <Graphics draw={draw}>
            <Text
                text={stats.name}
                anchor={0.5}
                zIndex={1000}
                x={x}
                y={y}
                style={
                    new TextStyle({
                        align: 'center',
                        fontFamily: '"Source Sans Pro", Helvetica, sans-serif',
                        fontSize: 15,
                        fill: ['#000000'],
                        wordWrap: true,
                        wordWrapWidth: 440,
                    })
                }
            />
        </Graphics>

    </>
}

export default Circle