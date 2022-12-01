import React from 'react'
import { Button } from '@mui/material'
import { styled } from '@mui/material/styles'
import { Link } from "gatsby"

/**
 * Item for navigation bar.
 * @author Brandon Kwintner
 * @param {string} title
 * @param {string} route
 */

 const NavOptionButton = styled(Button)(({theme}) => ({
    color: 'white!important',
    fontFamily: 'Open Sans, sans-serif!important',
    fontSize: '15px!important',
    marginLeft: '20px!important',
}))


const NavigationBarItem = ({ title, route, gatsby }) => {
    if (gatsby) {
        return <NavOptionButton component={Link} to={route}> {title} </NavOptionButton>
    }
    return (
        <NavOptionButton href={route}> {title} </NavOptionButton>
    )
}

export default NavigationBarItem
