import React from 'react';
import '../App.css';

function SearchBar({ query, handleSearchChange, handleKeyDown, logo, searchInputRef }) {
    return (
        <div className="form-group">
            <label>
                <input
                    type="text"
                    name="notASearchField"
                    className="form-control"
                    placeholder="Enter program name or press enter for all programs"
                    value={query}
                    onChange={handleSearchChange}
                    onKeyDown={handleKeyDown}
                    ref={searchInputRef}
                />
            </label>
            <span className="powered-by-ai">
                Powered by GPT &nbsp;
                <img src={logo} alt="Powered by AI" />
            </span>
        </div>
    );
}

export default SearchBar;