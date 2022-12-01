
import React from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import isItemActive from '../../utils/isItemActive';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import { Link } from 'gatsby';
import slugify from '../../utils/slugify';


export default function SidebarSection({ section, isActive, setActive, location, blog }) {

  const deg = isActive ? 0 : 180;

  return <>
    <ListItem key={section.title} disablePadding>
      <ListItemButton sx={{height: "35px"}} onClick={() => {
        if (isActive) {
          setActive(null)
        } else {
          setActive(section)
        }
      }}>
        <ListItemIcon>
          <ExpandMoreIcon style={{
            transform: `rotateX(${deg}deg)`,
            transition: "-webkit-transform 0.2s"
          }} />
        </ListItemIcon>
        <ListItemText primary={section.title} />
      </ListItemButton>
    </ListItem>
    <Collapse in={isActive} timeout="auto" unmountOnExit>
      <List component="div" disablePadding>
        {section.items.map((item, idx) => 
          <>
            <ListItem key={section.title + "-" + item.id} disablePadding>
              <ListItemButton component={Link} to={blog ? item.id : item.path} sx={{ height: "35px", pl: 4, borderRight: isItemActive(location, item) ? "5px solid #2196f3" : undefined }}>
                <ListItemText primary={section.isOrdered ? `${(idx + 1)}. ${item.title}` : item.title} />
              </ListItemButton>
            </ListItem>
            {item.subitems && item.subitems.map((subitem) => 
              <ListItem key={section.title + "-" + item.id + "-" + subitem.id} disablePadding>
                <ListItemButton component={Link} to={subitem.path} sx={{ height: "35px", pl: 8, borderRight: isItemActive(location, subitem) ? "5px solid #2196f3" : undefined }}>
                  <ListItemText primary={subitem.title} />
                </ListItemButton>
              </ListItem>
            )
            
            }
          </>
        )}
      </List>
    </Collapse>
  </>

}



