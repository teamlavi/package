
import slugify from './slugify';

const toAnchor = (href = '') => {
  const index = href.indexOf('#');
  return index >= 0 ? href.substr(index) : '';
};


const isItemActive = (location, item) => {
  if (item.path === location.pathname || location.pathname.includes(item.path)) {
    return true
  } else if (location.hash) {
    if (item.href) {
      return location.hash === toAnchor(item.href);
    }
  } else if (item.id.includes('html')) {
    return location.pathname.includes(item.id);
  } 
  const slugId = location.pathname.split('/').slice(-1)[0];
  return slugId === item.id;
};

export default isItemActive;