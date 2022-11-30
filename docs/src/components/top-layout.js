import React from "react";
import { ThemeProvider } from '@mui/material/styles';
import GlobalStyle from "../prism-theme";

export default function TopLayout({ children, theme }) {

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle>{children}</GlobalStyle>
    </ThemeProvider>
  );
}