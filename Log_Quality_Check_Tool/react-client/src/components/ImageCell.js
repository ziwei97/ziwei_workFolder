import React, { useState } from 'react'
import "./ImageCell.css"

const ImageCell = ({ cell }) => {
    const [expand, setExpand] = useState(false);
    const text = cell['row']['original']['image_quality']

    const showMore = () => {
        setExpand(old => !old)
    }

    return (
        <>
            <div onClick={showMore} className="toggleShow">
                {expand ? "show less" : "show more"}
            </div>
            {expand ? <div> {text} </div> : null}
        </>
    )
}

export default ImageCell