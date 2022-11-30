

import slugify from './slugify';


const findSectionForPath = (
    pathname,
    sections,
) => {
    let activeSection;

    sections.forEach(section => {
        const match = section.items.some(
            item =>
                pathname === item.path || pathname.includes(item.path) || 
                (item.subitems &&
                    item.subitems.some(subitem => pathname === subitem.path || pathname.includes(subitem.path))),
        );
        if (match) {
            activeSection = section;
        }
    });
    return activeSection;
};

export default findSectionForPath;