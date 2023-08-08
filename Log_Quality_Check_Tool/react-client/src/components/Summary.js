import React, { useState, useEffect } from 'react'
import "./Summary.css"

const Summary = ({ rows }) => {
  const [subjects, setSubjects] = useState(0)
  const [images, setImages] = useState(0)

  useEffect(() => {
    const new_subjects = rows.reduce((partialSum, a) => partialSum + a['values']['subject_number'], 0);
    setSubjects(new_subjects)
    const new_images = rows.reduce((partialSum, a) => partialSum + a['values']['image_collection_number'], 0);
    setImages(new_images)
  }, [rows])

  return (
    <div className="summary">
      <div>Summary:</div>
      <div>
        Total subject number: {subjects}
      </div>
      <div>
        Total image collection number: {images}
      </div>
    </div>

  )
}

export default Summary