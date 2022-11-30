 'use strict';

 const {resolve} = require('path');
 const webpack = require('webpack');
 
 module.exports = ({stage, actions}) => {
   actions.setWebpackConfig({
     resolve: {
       modules: [
         resolve(__dirname, '../src'),
         resolve(__dirname, '../node_modules'),
       ],
     },
   });
 };