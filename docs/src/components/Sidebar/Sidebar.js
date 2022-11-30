import React, { useState } from 'react';
import SidebarSection from "./SidebarSection"
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';

const drawerWidth = 240;

export default function Sidebar({ location, sectionList, defaultActive, blog }) {
  const [active, setActive] = useState(defaultActive)

  return <Drawer
    sx={{
      zIndex: 0,

      width: drawerWidth,
      flexShrink: 0,
      '& .MuiDrawer-paper': {
        top: 64,
        width: drawerWidth,
        boxSizing: 'border-box',
      },
    }}
    variant="permanent"
    anchor="left"
  >
    <Divider />
    <List>
      {sectionList.map((section, index) => (
        <SidebarSection
          key={section.title}
          blog={blog}
          section={section}
          isActive={active && active.title === section.title}
          setActive={setActive}
          location={location}
        />
      ))}
    </List>
  </Drawer>
}



