import React, { useEffect, useRef, useState } from 'react'
// import { Link } from 'react-router-dom'
import {
    Button,
    ClickAwayListener,
    Grow,
    MenuItem,
    MenuList,
    Paper,
    Popper,
} from '@mui/material'
import { ExpandMore } from '@mui/icons-material'
import { styled } from '@mui/material/styles'

/**
 * Menu Item that expands into a drop down menu with more options.
 * @param {string} title
 * @param {string[]} options
 */

const NavOptionButton = styled(Button)(({theme}) => ({
    color: '#484848!important',
    fontFamily: 'Open Sans, sans-serif!important',
    fontSize: '15px!important',
    marginLeft: '20px!important',
}))

const NavOptionButtonTransparent = styled(NavOptionButton)(({theme}) => ({
    '&:hover': {
        backgroundColor: 'transparent!important',
    },
}))

const DropDownMenu = ({ title, options }) => {
    const [open, setOpen] = useState(false)
    const anchorRef = useRef(null)

    const handleOpen = () => {
        setOpen(true)
    }

    const handleClose = (event) => {
        if (anchorRef.current && anchorRef.current.contains(event.target)) {
            return
        }
        setOpen(false)
    }

    const handleListKeyDown = (event) => {
        if (event.key === 'Tab') {
            event.preventDefault()
            setOpen(false)
        }
    }

    const prevOpen = useRef(open)
    useEffect(() => {
        if (prevOpen.current === true && open === false) {
            //anchorRef.current.focus();
        }
        prevOpen.current = open
    }, [open])

    return (
        <div style={{display: 'flex!important'}}>
            <NavOptionButton
                ref={anchorRef}
                aria-controls={open ? 'menu-list-grow' : undefined}
                aria-haspopup="true"
                onClick={handleOpen}
                onMouseOver={handleOpen}
                onMouseLeave={handleClose}
                endIcon={<ExpandMore />}
            >
                {title}
            </NavOptionButton>
            <Popper
                open={open}
                anchorEl={anchorRef.current}
                role={undefined}
                transition
                disablePortal
            >
                {({ TransitionProps, placement }) => (
                    <Grow
                        {...TransitionProps}
                        style={{
                            transformOrigin:
                                placement === 'bottom' ? 'center top' : 'center bottom',
                        }}
                    >
                        <Paper>
                            <ClickAwayListener onClickAway={handleClose}>
                                <MenuList
                                    autoFocusItem={open}
                                    id="menu-list-grow"
                                    onKeyDown={handleListKeyDown}
                                    onMouseLeave={handleClose}
                                >
                                    {options && options.map((item) => {
                                        const { title, route, icon } = item
                                        return (
                                            <MenuItem key={title} onClick={handleClose}>
                                                    <NavOptionButtonTransparent
                                                        href={route}
                                                        startIcon={icon}
                                                    >
                                                        {title}
                                                    </NavOptionButtonTransparent>
                                            </MenuItem>
                                        )
                                    })}
                                </MenuList>
                            </ClickAwayListener>
                        </Paper>
                    </Grow>
                )}
            </Popper>
        </div>
    )
}

export default DropDownMenu
