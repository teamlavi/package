import React from "react";
import * as PIXI from "pixi.js";
import { PixiComponent, useApp } from "@inlet/react-pixi";
import { Viewport as PixiViewport } from "pixi-viewport";

const PixiComponentViewport = PixiComponent("Viewport", {
    create: ({ app, width, height, children }) => {
        const viewport = new PixiViewport({
            screenWidth: width,
            screenHeight: height,
            worldWidth: width * 2,
            worldHeight: height * 2,
            ticker: app.ticker,
            interaction: app.renderer.plugins.interaction
        });
        viewport.drag().pinch().wheel().clampZoom();

        return viewport;
    }
});

const Viewport = ({ width, height, children }) => {
    const app = useApp();
    return <PixiComponentViewport app={app} width={width} height={height} children={children} />
};

export default Viewport;
