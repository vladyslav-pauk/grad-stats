import React from 'react';
import '../App.css';

function UniversityList({ universities, dropdownRef, highlightIndex, hoverIndex, setHoverIndex, handleStatistics, isDropdownHovered, setIsDropdownHovered }) {
    return (
        <div className="dropdown-container" style={{ position: 'relative' }}>
            <ul className="dropdown-list" ref={dropdownRef} onMouseEnter={() => setIsDropdownHovered(true)} onMouseLeave={() => setIsDropdownHovered(false)}>
                {universities.map((university, index) => (
                    <li
                        key={index}
                        className={`dropdown-list-item ${index === (highlightIndex >= 0 && hoverIndex === -1 ? highlightIndex : hoverIndex) ? 'active' : ''}`}
                        onClick={() => handleStatistics(university)}
                        onMouseEnter={() => setHoverIndex(index)}
                        onMouseLeave={() => setHoverIndex(-1)}
                    >
                        {university}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default UniversityList;